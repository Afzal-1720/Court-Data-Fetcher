from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(data, filename):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    fields = [
        ("Court", data.get("court", "N/A")),
        ("Case Type", data.get("case_type", "N/A")),
        ("Case Number", data.get("case_number", "N/A")),
        ("CNR No", data.get("cnr_number", "N/A")),
        ("Status", data.get("status", "N/A")),
        ("Parties", data.get("parties", "N/A")),
        ("Dealing Assistant", data.get("dealing_assistant", "N/A")),
        ("Filing Advocate", data.get("filing_advocate", "N/A")),
        ("Subject 1", data.get("subject1", "N/A")),
        ("Subject 2", data.get("subject2", "N/A")),
        ("Date of Filing", data.get("filing_date", "N/A")),
        ("Date of Registration", data.get("registration_date", "N/A")),
        ("Judgment PDF", data.get("judgment_pdf_link", "N/A"))
    ]

    for label, value in fields:
        # Ensure value is a string and replace None explicitly
        display_value = str(value) if value is not None else "N/A"
        story.append(Paragraph(f"<b>{label}:</b> {display_value}", styles["Normal"]))
        story.append(Spacer(1, 6))

    pdf.build(story)
    if os.path.exists(filename):
        print(f"PDF generated successfully at: {filename}")
    else:
        print(f"Failed to generate PDF at: {filename}")
    return filename