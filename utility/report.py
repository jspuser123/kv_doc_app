from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame, Paragraph, Spacer
from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import xlsxwriter
import os
class Pdf_Report():
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def draw_header_footer(self, canvas, doc, header_text, footer_text):
        canvas.saveState()
        
        # Header
        header = Paragraph(header_text, self.styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        x = (doc.pagesize[0] - w) / 2
        y = doc.height + doc.topMargin - h 
        header.drawOn(canvas, x, y)

        # Footer
        footer = Paragraph(f"{footer_text} | Page {doc.page}", self.styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    def pdf_report(self, filename: str, table_data: list, header_text: str, footer_text: str):
        file=f'{os.path.expanduser("~")}/Documents/{filename}'
        doc = SimpleDocTemplate(file, pagesize=landscape(letter))
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        
        # Attach header/footer to template
        template = PageTemplate(id='header_footer',
                                frames=[frame],
                                onPage=lambda canvas, doc: self.draw_header_footer(canvas, doc, header_text, footer_text))
        doc.addPageTemplates([template])

        # num_columns = len(table_data[0])
        # available_width = doc.width
        # col_width = available_width / num_columns
        # col_widths = [col_width] * num_columns

        # Create and style table
        table = Table(table_data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])
        ])
        table.setStyle(style)

        # Build document
        story = [Spacer(1, 15), table]
        doc.build(story)
class xlsx_Report():
    def __init__(self):
        pass

    def xlsx(self, filename: str, table_data: list, header_text: str, footer_text: str):
        workbook = xlsxwriter.Workbook(f'{os.path.expanduser("~")}/Documents/{filename}')
        worksheet = workbook.add_worksheet()

        # Write some data.
        worksheet.write('A1', header_text)
        start_row = 1  # Excel row 5 (0-indexed)
        for col_index, header in enumerate(table_data[0]):
            worksheet.write(start_row, col_index, header)

        # Table rows
        for row_index, row_data in enumerate(table_data[1:], start=start_row + 1):
            for col_index, cell in enumerate(row_data):
                worksheet.write(row_index, col_index, cell)

        # Footer (optional: placed below the table)
        footer_row = start_row + len(table_data) + 2
        worksheet.write(footer_row, 0, footer_text)



        # Close the workbook.
        workbook.close()

