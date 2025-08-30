#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def test_pdf_generation():
    """Тестирует генерацию PDF с ReportLab"""
    
    # Создаем документ
    doc = SimpleDocTemplate("test_output.pdf", pagesize=A4)
    story = []
    
    # Стили
    styles = getSampleStyleSheet()
    
    # Простой заголовок
    title_style = ParagraphStyle(
        'TestTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Центрирование
        textColor=colors.black
    )
    
    title = Paragraph("Тестовый PDF", title_style)
    story.append(title)
    
    # Простой текст
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black
    )
    
    text = Paragraph("Это тестовый текст для проверки видимости", normal_style)
    story.append(text)
    
    story.append(Spacer(1, 20))
    
    # Простая таблица
    table_data = [
        ['Имя', 'Возраст', 'Город'],
        ['Иван', '25', 'Москва'],
        ['Мария', '30', 'Санкт-Петербург']
    ]
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    story.append(table)
    
    # Строим PDF
    doc.build(story)
    print("Тестовый PDF создан: test_output.pdf")

if __name__ == "__main__":
    test_pdf_generation()
