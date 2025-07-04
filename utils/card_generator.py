from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class CardPDFGenerator:
    def __init__(self):
        self.card_width = 80 * mm
        self.card_height = 135 * mm
        self.margin = 10 * mm

    def generar_pdf_tarjetas(self, extintores_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tarjetas_extintores_{timestamp}.pdf"
        home_dir = os.path.expanduser("~")
        output_dir = os.path.join(home_dir, "Documents", "tarjetas_pdf")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        filepath = os.path.join(output_dir, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            topMargin=self.margin,
            bottomMargin=self.margin,
            leftMargin=self.margin,
            rightMargin=self.margin
        )

        story = []
        for i in range(0, len(extintores_data), 4):
            batch = extintores_data[i:i+4]
            table_data = []
            for row in range(2):
                row_cards = []
                for col in range(2):
                    index = row * 2 + col
                    if index < len(batch):
                        card = self._crear_tarjeta(batch[index])
                        row_cards.append(card)
                    else:
                        row_cards.append("")
                table_data.append(row_cards)

            table = Table(
                table_data,
                colWidths=[self.card_width, self.card_width],
                rowHeights=[self.card_height, self.card_height]
            )
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 2, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            story.append(table)
            if i + 4 < len(extintores_data):
                story.append(Spacer(1, 10))
        doc.build(story)
        return filepath

    def _crear_tarjeta(self, extintor_data):
        styles = getSampleStyleSheet()
        content_width = self.card_width - 6 * mm

        black_color = colors.black
        white_color = colors.white
        gray_text = colors.HexColor("#555555")

        header_bg_style = ParagraphStyle(
            'HeaderBlack',
            parent=styles['Normal'],
            fontSize=16,
            textColor=white_color,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        label_style = ParagraphStyle(
            'LabelStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold',
            textColor=black_color
        )
        value_style = ParagraphStyle(
            'ValueStyle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        vencimiento_label_style = ParagraphStyle(
            'VencLabelStyle',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            textColor=white_color
        )
        vencimiento_value_style = ParagraphStyle(
            'VencValueStyle',
            parent=styles['Normal'],
            fontSize=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            textColor=black_color
        )
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            fontName='Helvetica',
            textColor=gray_text
        )

        card_content = [
            [Table([
                [Paragraph("LE * LO", header_bg_style)],
                [Paragraph("MATAFUEGOS", header_bg_style)]
            ], colWidths=[content_width],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), black_color),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))],
            [Paragraph("Bertani Sur 750 - San Rafael Mendoza", normal_style)],
            [Paragraph("2604617290 - 2604519103", normal_style)],
            [Spacer(1, 5)],
            [Table([
                [Paragraph("Propietario:", label_style),
                 Paragraph(extintor_data.get('propietario', ''), value_style)],
                [Paragraph("Clase:", label_style),
                 Paragraph(extintor_data.get('clase', ''), value_style)],
                [Paragraph("Capacidad:", label_style),
                 Paragraph(extintor_data.get('capacidad', ''), value_style)],
                [Paragraph("VTO. PRUEBA<br/>HIDRÁULICA:", label_style),
                 Paragraph(extintor_data.get('vto_prueba_hidraulica', ''), value_style)],
            ], colWidths=[28 * mm, 48 * mm],
               style=TableStyle([
                   ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                   ('LEFTPADDING', (0, 0), (-1, -1), 3),
                   ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                   ('TOPPADDING', (0, 0), (-1, -1), 3),
                   ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
               ]))],
            [Spacer(1, 6)],
            [Table([
                [Paragraph("FECHA DE VENCIMIENTO", vencimiento_label_style)]
            ], colWidths=[content_width],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), black_color),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))],
            [Paragraph(extintor_data.get('fecha_vencimiento', ''), vencimiento_value_style)],
            [Paragraph(f"N°: {extintor_data.get('numero', '')}", normal_style)],
            [Spacer(1, 4)],
            [Paragraph("Recarga y mantenimiento según Normas IRAM", normal_style)],
            [Paragraph("El propietario es responsable de la dotación de matafuegos<br/>Decreto N° 351/79", footer_style)],
        ]

        card_table = Table(
            [[content] for content in card_content],
            colWidths=[content_width],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ])
        )
        return card_table
