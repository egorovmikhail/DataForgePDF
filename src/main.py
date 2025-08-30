#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataForgePDF - Генератор PDF из файлов данных
Поддерживает CSV, JSON, Excel, Word и TXT файлы
"""

import os
import sys
import csv
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

try:
    import openpyxl
    from docx import Document
    from jinja2 import Template
    # Импортируем WeasyPrint для основной генерации PDF с поддержкой кириллицы
    try:
        import weasyprint
        from weasyprint import HTML
        USE_WEASYPRINT = True
        print("✅ WeasyPrint доступен для генерации PDF с поддержкой кириллицы")
    except ImportError:
        USE_WEASYPRINT = False
        print("⚠️  WeasyPrint недоступен, будет использован ReportLab")
    
    # Импортируем ReportLab в любом случае
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib import colors
        REPORTLAB_AVAILABLE = True
        
        # Пытаемся загрузить шрифт Roboto для поддержки кириллицы
        try:
            roboto_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Roboto-Regular.ttf')
            if os.path.exists(roboto_path):
                pdfmetrics.registerFont(TTFont('Roboto', roboto_path))
                ROBOTO_AVAILABLE = True
            else:
                ROBOTO_AVAILABLE = False
        except:
            ROBOTO_AVAILABLE = False
    except ImportError:
        REPORTLAB_AVAILABLE = False
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Установите зависимости: pip install -r requirements.txt")
    sys.exit(1)


class DataReader:
    """Класс для чтения различных типов файлов данных"""
    
    @staticmethod
    def read_csv(file_path: str) -> Tuple[List[str], List[List[str]]]:
        """Читает CSV файл"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)
                if not data:
                    return [], []
                return data[0], data[1:]  # заголовки, данные
        except Exception as e:
            raise Exception(f"Ошибка чтения CSV файла: {e}")
    
    @staticmethod
    def read_json(file_path: str) -> Tuple[List[str], List[List[str]]]:
        """Читает JSON файл"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            if isinstance(data, list) and data:
                # Если это список словарей
                if isinstance(data[0], dict):
                    columns = list(data[0].keys())
                    rows = [[str(row.get(col, '')) for col in columns] for row in data]
                    return columns, rows
                else:
                    # Если это список списков
                    return [f"Колонка_{i+1}" for i in range(len(data[0]))], data
            elif isinstance(data, dict):
                # Если это словарь
                columns = list(data.keys())
                rows = [[str(data[col])] for col in columns]
                return columns, rows
            else:
                raise Exception("Неподдерживаемый формат JSON")
        except Exception as e:
            raise Exception(f"Ошибка чтения JSON файла: {e}")
    
    @staticmethod
    def read_excel(file_path: str) -> Tuple[List[str], List[List[str]]]:
        """Читает Excel файл"""
        try:
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            sheet = workbook.active
            
            data = []
            for row in sheet.iter_rows(values_only=True):
                if any(cell is not None for cell in row):
                    data.append([str(cell) if cell is not None else '' for cell in row])
            
            if not data:
                return [], []
            
            return data[0], data[1:]  # заголовки, данные
        except Exception as e:
            raise Exception(f"Ошибка чтения Excel файла: {e}")
    
    @staticmethod
    def read_word(file_path: str) -> Tuple[List[str], List[List[str]]]:
        """Читает Word файл"""
        try:
            doc = Document(file_path)
            data = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    # Разделяем текст по табуляции или другим разделителям
                    row = [cell.strip() for cell in paragraph.text.split('\t')]
                    if len(row) == 1:
                        row = [paragraph.text.strip()]
                    data.append(row)
            
            if not data:
                return [], []
            
            # Определяем максимальное количество колонок
            max_cols = max(len(row) for row in data)
            
            # Нормализуем данные
            normalized_data = []
            for row in data:
                normalized_row = row + [''] * (max_cols - len(row))
                normalized_data.append(normalized_row)
            
            # Создаем заголовки
            columns = [f"Колонка_{i+1}" for i in range(max_cols)]
            
            return columns, normalized_data
        except Exception as e:
            raise Exception(f"Ошибка чтения Word файла: {e}")
    
    @staticmethod
    def read_txt(file_path: str, separator: str = '\t') -> Tuple[List[str], List[List[str]]]:
        """Читает TXT файл"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            data = []
            for line in lines:
                line = line.strip()
                if line:
                    row = [cell.strip() for cell in line.split(separator)]
                    data.append(row)
            
            if not data:
                return [], []
            
            # Определяем максимальное количество колонок
            max_cols = max(len(row) for row in data)
            
            # Нормализуем данные
            normalized_data = []
            for row in data:
                normalized_row = row + [''] * (max_cols - len(row))
                normalized_data.append(normalized_row)
            
            # Создаем заголовки
            columns = [f"Колонка_{i+1}" for i in range(max_cols)]
            
            return columns, normalized_data
        except Exception as e:
            raise Exception(f"Ошибка чтения TXT файла: {e}")


class PDFGenerator:
    """Класс для генерации PDF файлов"""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.template = self._load_template()
    
    def _load_template(self) -> Template:
        """Загружает HTML шаблон"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as file:
                return Template(file.read())
        except Exception as e:
            raise Exception(f"Ошибка загрузки шаблона: {e}")
    
    def generate_pdf(self, columns: List[str], rows: List[List[str]], 
                     output_path: str, filename: str) -> str:
        """Генерирует PDF файл"""
        try:
            pdf_path = os.path.join(output_path, f"{filename}.pdf")
            
            if USE_WEASYPRINT:
                # Используем WeasyPrint
                return self._generate_weasyprint_pdf(columns, rows, pdf_path, filename)
            elif REPORTLAB_AVAILABLE:
                # Используем ReportLab
                return self._generate_reportlab_pdf(columns, rows, pdf_path, filename)
            else:
                raise Exception("Не удалось импортировать ни WeasyPrint, ни ReportLab")
        except Exception as e:
            raise Exception(f"Ошибка генерации PDF: {e}")
    
    def _generate_weasyprint_pdf(self, columns: List[str], rows: List[List[str]], 
                                 pdf_path: str, filename: str) -> str:
        """Генерирует PDF с помощью WeasyPrint с поддержкой кириллицы"""
        try:
            # Подготавливаем данные для шаблона
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            
            # Рендерим HTML
            html_content = self.template.render(
                columns=columns,
                rows=rows,
                timestamp=timestamp,
                filename=filename
            )
            
            # Создаем PDF с поддержкой кириллицы (шрифты уже в HTML шаблоне)
            html = HTML(string=html_content)
            
            # Генерируем PDF без дополнительного CSS
            html.write_pdf(pdf_path)
            
            print("✅ PDF создан с помощью WeasyPrint с поддержкой кириллицы")
            return pdf_path
        except Exception as e:
            # Если WeasyPrint не работает, используем ReportLab
            print(f"⚠️  WeasyPrint не работает: {e}")
            print("🔄 Используем ReportLab как fallback...")
            return self._generate_reportlab_pdf(columns, rows, pdf_path, filename)
    
    def _generate_reportlab_pdf(self, columns: List[str], rows: List[List[str]], 
                                pdf_path: str, filename: str) -> str:
        """Генерирует PDF с помощью ReportLab с полной поддержкой кириллицы"""
        # Создаем документ
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        # Стили
        styles = getSampleStyleSheet()
        
        # Регистрируем шрифты с поддержкой кириллицы
        try:
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase import pdfmetrics
            
            # Пытаемся загрузить шрифт DejaVu Sans (отличная поддержка кириллицы)
            try:
                pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
                font_name = 'DejaVuSans'
                print("✅ Используем шрифт DejaVu Sans с полной поддержкой кириллицы")
            except Exception as e:
                try:
                    # Fallback на системный шрифт Arial Unicode MS
                    pdfmetrics.registerFont(TTFont('ArialUnicode', 'fonts/Arial Unicode.ttf'))
                    font_name = 'ArialUnicode'
                    print("✅ Используем системный шрифт Arial Unicode MS с полной поддержкой кириллицы")
                except Exception as e2:
                    try:
                        # Fallback на Roboto Bold
                        pdfmetrics.registerFont(TTFont('RobotoBold', 'fonts/Roboto-Bold.ttf'))
                        font_name = 'RobotoBold'
                        print("✅ Используем шрифт Roboto Bold с поддержкой кириллицы")
                    except Exception as e3:
                        # Последний fallback на встроенные шрифты
                        font_name = 'Helvetica'
                        print(f"⚠️  Используем встроенный шрифт Helvetica (кириллица может не отображаться)")
                        print(f"   Ошибка DejaVu Sans: {e}")
                        print(f"   Ошибка Arial Unicode: {e2}")
                        print(f"   Ошибка Roboto Bold: {e3}")
        except Exception as e:
            font_name = 'Helvetica'
            print(f"⚠️  Ошибка импорта шрифтов: {e}")
        
        # Функция для безопасного текста (БЕЗ транслитерации)
        def safe_text(text):
            """Преобразует текст для безопасного отображения в ReportLab"""
            if isinstance(text, str):
                # Заменяем только эмодзи и специальные символы на текст
                special_chars = {
                    '📊': 'ДАННЫЕ', '📁': 'ФАЙЛ', '🏷️': 'КОЛОНКИ', '📄': 'СТРАНИЦА', 
                    '🔄': 'АВТОМАТИЧЕСКИ', '📊': 'ЗАПИСИ'
                }
                
                for special, replacement in special_chars.items():
                    text = text.replace(special, replacement)
                
                # Очищаем от невидимых символов, но сохраняем кириллицу
                result = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
                return result
            return str(text)
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Центрирование
            textColor=colors.black,
            fontName=font_name
        )
        
        # Заголовок на русском языке (БЕЗ транслитерации)
        title = Paragraph("Данные из файла", title_style)
        story.append(title)
        
        # Информация о файле
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=20,
            alignment=1,
            textColor=colors.black,
            fontName=font_name
        )
        
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        info_text = f"Файл: {safe_text(filename)}<br/>Записей: {len(rows)}<br/>Колонок: {len(columns)}<br/>Сгенерировано: {timestamp}"
        info = Paragraph(info_text, info_style)
        story.append(info)
        
        story.append(Spacer(1, 20))
        
        # Создаем таблицу с поддержкой кириллицы (БЕЗ транслитерации)
        safe_columns = [safe_text(col) for col in columns]
        safe_rows = [[safe_text(cell) for cell in row] for row in rows]
        table_data = [safe_columns] + safe_rows
        
        # Настройки таблицы
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), font_name),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        
        # Строим PDF
        doc.build(story)
        
        return pdf_path


class FileScanner:
    """Класс для сканирования директорий и поиска файлов данных"""
    
    SUPPORTED_EXTENSIONS = {
        '.csv': 'CSV файл',
        '.json': 'JSON файл',
        '.xlsx': 'Excel файл',
        '.xls': 'Excel файл',
        '.docx': 'Word файл',
        '.doc': 'Word файл',
        '.txt': 'Текстовый файл'
    }
    
    @staticmethod
    def scan_directories(directories: List[str]) -> List[Tuple[str, str, str]]:
        """Сканирует указанные директории и возвращает список файлов"""
        files = []
        
        for directory in directories:
            if not os.path.exists(directory):
                print(f"Директория не существует: {directory}")
                continue
            
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    ext = os.path.splitext(filename)[1].lower()
                    
                    if ext in FileScanner.SUPPORTED_EXTENSIONS:
                        file_type = FileScanner.SUPPORTED_EXTENSIONS[ext]
                        files.append((file_path, filename, file_type))
        
        return files


class ConsoleInterface:
    """Класс для интерактивного консольного интерфейса"""
    
    @staticmethod
    def show_file_selection(files: List[Tuple[str, str, str]]) -> int:
        """Показывает меню выбора файла"""
        if not files:
            print("Файлы данных не найдены!")
            return -1
        
        print("\nДоступные файлы данных:")
        print("-" * 80)
        
        for i, (file_path, filename, file_type) in enumerate(files, 1):
            print(f"{i:2d}. {filename:<30} ({file_type:<15}) - {file_path}")
        
        print("-" * 80)
        
        while True:
            try:
                choice = input(f"\nВыберите файл (1-{len(files)}) или 0 для выхода: ").strip()
                if choice == '0':
                    return -1
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(files):
                    return choice_num - 1
                else:
                    print(f"Введите число от 1 до {len(files)}")
            except ValueError:
                print("Введите корректное число")
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                return -1


class SystemUtils:
    """Утилиты для работы с системой"""
    
    @staticmethod
    def open_pdf(pdf_path: str):
        """Открывает PDF файл в системной программе просмотра"""
        try:
            system = platform.system().lower()
            
            if system == "darwin":  # macOS
                subprocess.run(["open", pdf_path], check=True)
            elif system == "windows":
                os.startfile(pdf_path)
            elif system == "linux":
                subprocess.run(["xdg-open", pdf_path], check=True)
            else:
                print(f"Автоматическое открытие PDF не поддерживается для {system}")
                
        except Exception as e:
            print(f"Ошибка открытия PDF: {e}")


def main():
    """Основная функция программы"""
    print("=" * 60)
    print("DataForgePDF - Генератор PDF из файлов данных")
    print("=" * 60)
    
    # Создаем необходимые директории
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Определяем директории для сканирования
    data_dirs = ["data", "."]  # Сначала ищем в папке data, затем в текущей
    
    # Сканируем файлы
    print("Сканирование директорий...")
    files = FileScanner.scan_directories(data_dirs)
    
    if not files:
        print("Файлы данных не найдены!")
        print("Создайте папку 'data' и поместите туда файлы данных")
        return
    
    # Показываем меню выбора
    choice = ConsoleInterface.show_file_selection(files)
    if choice == -1:
        print("Программа завершена")
        return
    
    selected_file = files[choice]
    file_path, filename, file_type = selected_file
    
    print(f"\nВыбран файл: {filename} ({file_type})")
    
    try:
        # Читаем данные в зависимости от типа файла
        print("Чтение данных...")
        
        if file_type == 'CSV файл':
            columns, rows = DataReader.read_csv(file_path)
        elif file_type == 'JSON файл':
            columns, rows = DataReader.read_json(file_path)
        elif file_type.startswith('Excel'):
            columns, rows = DataReader.read_excel(file_path)
        elif file_type.startswith('Word'):
            columns, rows = DataReader.read_word(file_path)
        elif file_type == 'Текстовый файл':
            separator = input("Введите разделитель колонок (по умолчанию табуляция): ").strip()
            if not separator:
                separator = '\t'
            columns, rows = DataReader.read_txt(file_path, separator)
        else:
            print(f"Неподдерживаемый тип файла: {file_type}")
            return
        
        if not columns or not rows:
            print("Файл не содержит данных")
            return
        
        print(f"Прочитано {len(rows)} строк с {len(columns)} колонками")
        
        # Генерируем PDF
        print("Генерация PDF...")
        template_path = "templates/template.html"
        
        if not os.path.exists(template_path):
            print(f"Шаблон не найден: {template_path}")
            return
        
        generator = PDFGenerator(template_path)
        
        # Создаем имя файла без расширения
        base_filename = os.path.splitext(filename)[0]
        
        # Генерируем PDF
        pdf_path = generator.generate_pdf(columns, rows, output_dir, base_filename)
        
        print(f"PDF успешно создан: {pdf_path}")
        
        # Открываем PDF
        print("Открытие PDF файла...")
        SystemUtils.open_pdf(pdf_path)
        
        print("\nПрограмма завершена успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
