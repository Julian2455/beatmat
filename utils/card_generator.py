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
        self.card_height = 93 * mm
        self.margin = 2 * mm
        
    def generar_pdf_tarjetas(self, extintores_data, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tarjetas_extintores_{timestamp}.pdf"
        output_dir = "tarjetas_pdf"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) #Cuando terminemos hay que cambiar esta ruta para que la jefa encuentre los pdf
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
        for i in range(0, len(extintores_data), 6):
            batch = extintores_data[i:i+6]
            table_data = []
            for row in range(3):
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
                rowHeights=[self.card_height, self.card_height, self.card_height]
            )
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(table)
            if i + 6 < len(extintores_data):
                story.append(Spacer(1, 20))
        doc.build(story)
        return filepath
    
    def _crear_tarjeta(self, extintor_data):
        styles = getSampleStyleSheet()
        content_width = self.card_width - 6 * mm

        header_color = colors.HexColor("#2C3E50")
        banner_color = colors.HexColor("#34495E")

        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        label_style = ParagraphStyle(
            'LabelStyle',
            parent=styles['Normal'],
            fontSize=7,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold',
            textColor=colors.black
        )
        value_style = ParagraphStyle(
            'ValueStyle',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_LEFT,
            fontName='Helvetica',
            wordWrap='LTR'
        )

        card_content = [
            [Table([
                [Paragraph("LE * LO", header_style)],
                [Paragraph("MATAFUEGOS", subtitle_style)]
            ], colWidths=[content_width],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (0, 1), header_color),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))],
            [Paragraph("Bertani Sur 750 - San Rafael Mendoza", normal_style)],
            [Paragraph("2604617290 - 2604519103", normal_style)],
            [Table([
                [Paragraph("Propietario:", label_style),
                Paragraph(extintor_data.get('propietario', ''), value_style)],
                [Paragraph("Clase:", label_style),
                Paragraph(extintor_data.get('clase', ''), value_style)],
                [Paragraph("Capacidad:", label_style),
                Paragraph(f"{extintor_data.get('capacidad', '')}", value_style)],
                [Paragraph("VTO. PRUEBA<br/>HIDRAULICA:", label_style),
                Paragraph(extintor_data.get('vto_prueba_hidraulica', ''), value_style)],
            ], colWidths=[22 * mm, 52 * mm],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LINEAFTER', (0, 0), (0, -1), 0.5, colors.lightgrey),
            ]))],
            [Spacer(1, 3)],
            [Table([
                [Paragraph("PIERDE SU EFECTIVIDAD", ParagraphStyle(
                    'BannerStyle',
                    parent=styles['Normal'],
                    fontSize=7,
                    textColor=colors.white,
                    alignment=TA_CENTER,
                    fontName='Helvetica-Bold'
                ))]
            ], colWidths=[content_width],
            style=TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), banner_color),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))],
            [Paragraph(extintor_data.get('fecha_vencimiento', ''), ParagraphStyle(
                'VencimientoStyle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                textColor=header_color,
                spaceAfter=3
            ))],
            [Paragraph(f"N°: {extintor_data.get('numero', '')}", ParagraphStyle(
                'NumeroStyle',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
                textColor=header_color
            ))],
            [Spacer(1, 2)],
            [Paragraph("Recarga y mantenimiento<br/>Según Normas IRAM", normal_style)],
            [Paragraph("El propietario es responsable de la dotación de Matafuegos<br/>Decreto N° 351/79",
                ParagraphStyle(
                    'FooterStyle',
                    parent=styles['Normal'],
                    fontSize=7,
                    alignment=TA_CENTER,
                    fontName='Helvetica',
                    textColor=colors.HexColor("#7F8C8D")  # gris suave
                ))],
        ]

        card_table = Table(
            card_content,
            colWidths=[content_width],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ])
        )
        return card_table
