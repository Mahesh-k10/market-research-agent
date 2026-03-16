from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_pdf(text, filename="market_research_report.pdf"):

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    y = height - 40

    for line in text.split("\n"):
        c.drawString(40, y, line[:100])
        y -= 15

        if y < 40:
            c.showPage()
            y = height - 40

    c.save()

    return filename