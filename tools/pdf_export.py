from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap


def export_pdf(text):
    filename = "market_research_report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    x = 50
    y = height - 50

    max_chars_per_line = 90  # adjust if needed

    for paragraph in text.split("\n"):

        wrapped_lines = textwrap.wrap(paragraph, max_chars_per_line)

        for line in wrapped_lines:
            if y < 50:  # new page
                c.showPage()
                y = height - 50

            c.drawString(x, y, line)
            y -= 15

        y -= 10  # space between paragraphs

    c.save()

    return filename
