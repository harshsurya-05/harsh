from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from datetime import datetime

def generate_invoice_pdf(order):
    """Generates a PDF invoice for the given order object."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.hexColor("#2e7d32"))
    p.drawString(1*inch, height - 1*inch, "AgroHub")
    
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.black)
    p.drawRightString(width - 1*inch, height - 1*inch, "Official Invoice")
    
    # Order Info
    p.setFont("Helvetica-Bold", 12)
    p.drawString(1*inch, height - 1.8*inch, f"Invoice ID: #INV-{order.id:06d}")
    p.setFont("Helvetica", 10)
    p.drawString(1*inch, height - 2.0*inch, f"Date: {order.created_at.strftime('%d %b %Y %H:%M')}")
    p.drawString(1*inch, height - 2.2*inch, f"Customer ID: {order.customer_id}")
    
    # Billing Details
    p.drawString(1*inch, height - 2.6*inch, "Billing Address:")
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(1.2*inch, height - 2.8*inch, order.delivery_address)
    
    # Table Header
    p.line(1*inch, height - 3.2*inch, width - 1*inch, height - 3.2*inch)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(1*inch, height - 3.4*inch, "Item")
    p.drawString(3.5*inch, height - 3.4*inch, "Qty")
    p.drawString(4.5*inch, height - 3.4*inch, "Price")
    p.drawString(5.5*inch, height - 3.4*inch, "Subtotal")
    p.line(1*inch, height - 3.5*inch, width - 1*inch, height - 3.5*inch)
    
    # Items
    y = height - 3.8*inch
    p.setFont("Helvetica", 10)
    for item in order.items:
        p.drawString(1*inch, y, item['name'])
        p.drawString(3.5*inch, y, str(item['qty']))
        p.drawString(4.5*inch, y, f"Rs {item['price']}")
        p.drawString(5.5*inch, y, f"Rs {item['subtotal']}")
        y -= 0.3*inch
        
    # Total
    p.line(1*inch, y + 0.1*inch, width - 1*inch, y + 0.1*inch)
    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(width - 1*inch, y - 0.2*inch, f"Grand Total: Rs {order.total_amount}")
    
    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 0.5*inch, "Thank you for supporting local farmers! - AgroHub.in")

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
