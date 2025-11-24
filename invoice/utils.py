from io import BytesIO
from django.http import HttpResponse
from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'Invoice', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_invoice_pdf(invoice, invoice_details):
    pdf = InvoicePDF()
    pdf.add_page()
    
    # Invoice Details
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, f'Invoice ID: {invoice.id}', ln=True)
    pdf.cell(0, 10, f'Date: {invoice.date}', ln=True)
    pdf.cell(0, 10, f'Customer: {invoice.customer}', ln=True)
    pdf.cell(0, 10, f'Contact: {invoice.contact}', ln=True)
    pdf.cell(0, 10, f'Email: {invoice.email}', ln=True)
    pdf.ln(10)
    
    # Table Header
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(60, 10, 'Product', border=1)
    pdf.cell(40, 10, 'Price', border=1)
    pdf.cell(40, 10, 'Quantity', border=1)
    pdf.cell(40, 10, 'Total', border=1)
    pdf.ln()
    
    # Table Rows
    pdf.set_font('Helvetica', '', 12)
    for detail in invoice_details:
        # Save current position
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        # Draw Product Name (wrapping)
        pdf.multi_cell(60, 10, str(detail.product.product_name), border=0, align='L')
        
        # Get new Y position after multi_cell
        y_end = pdf.get_y()
        row_height = y_end - y_start
        
        # Draw border for product cell
        pdf.rect(x_start, y_start, 60, row_height)
        
        # Move cursor to the right of the product cell, at top_y
        pdf.set_xy(x_start + 60, y_start)
        
        # Draw other cells with the calculated row_height
        pdf.cell(40, row_height, str(detail.selling_price), border=1)
        pdf.cell(40, row_height, str(detail.amount), border=1)
        pdf.cell(40, row_height, str(detail.get_total_bill), border=1)
        
        # Move to next line (below the tallest cell)
        pdf.set_xy(x_start, y_end)
        
    pdf.ln(10)
    
    # Total
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, f'Total: {invoice.total}', align='R', ln=True)
    
    # Comments
    if invoice.comments:
        pdf.ln(10)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, 'Comments:', ln=True)
        pdf.set_font('Helvetica', '', 12)
        pdf.multi_cell(0, 10, invoice.comments)

    return pdf.output()
