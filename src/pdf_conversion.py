# src/pdf_conversion.py
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFConverter:
    def convert(self, json_file: str, pdf_file: str) -> None:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        pretty_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        styles = getSampleStyleSheet()
        json_style = ParagraphStyle(
            name='JsonStyle',
            fontName='Courier',
            fontSize=10,
            leading=12,
            textColor=colors.black,
            spaceBefore=6,
            spaceAfter=6
        )
        story = []
        story.append(Paragraph(f"JSON Output: {os.path.basename(json_file)}", styles['Title']))
        story.append(Spacer(1, 12))
        for line in pretty_json.splitlines():
            formatted_line = line.replace(' ', '&nbsp;')
            story.append(Paragraph(formatted_line, json_style))
        doc.build(story)
