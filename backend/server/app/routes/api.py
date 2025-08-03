from flask import Blueprint, request, jsonify, send_file
from .. import db  # Move up one level to app
from ..models.case_models import Case, ScrapingLog  # Relative import from app/models
from ..scraper.court_scraper import get_court_data
from ..utils.pdf_generator import generate_pdf
import os

bp = Blueprint('api', __name__, url_prefix='/api')

# Ensure temp directory exists
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@bp.route('/submit', methods=['POST'])
def submit_case():
    data = request.json
    court = data.get('court')
    case_type = data.get('caseType')
    case_number = data.get('caseNumber')
    filing_year = data.get('filingYear')

    # Scrape data
    scraped_data = get_court_data(court, case_type, case_number, filing_year)
    if 'error' in scraped_data:
        log = ScrapingLog(case_number=case_number, status='failed', error_message=scraped_data['error'])
        db.session.add(log)
        db.session.commit()
        return jsonify({'message': 'Error fetching data', 'error': scraped_data['error']}), 500

    # Print scraped data for debugging
    print(f"Scraped data: {scraped_data}")

    # Save to database with default 'N/A' for None values
    case = Case(
        court=court or "N/A",
        case_type=case_type or "N/A",
        case_number=case_number or "N/A",
        filing_year=filing_year or "N/A",
        parties=scraped_data.get('parties') or "N/A",
        judgment_pdf_link=scraped_data.get('judgment_pdf_link') or "N/A",
        filing_date=scraped_data.get('filing_date') or "N/A",
        order_date=scraped_data.get('order_date') or "N/A",
        next_hearing_date=scraped_data.get('next_hearing_date') or "N/A",
        cnr_number=scraped_data.get('cnr_number') or "N/A",
        status=scraped_data.get('status') or "N/A",
        dealing_assistant=scraped_data.get('dealing_assistant') or "N/A",
        filing_advocate=scraped_data.get('filing_advocate') or "N/A",
        subject1=scraped_data.get('subject1') or "N/A",
        subject2=scraped_data.get('subject2') or "N/A",
        registration_date=scraped_data.get('registration_date') or "N/A",
    )

    db.session.add(case)
    db.session.add(ScrapingLog(case_number=case_number, status='success'))
    db.session.commit()

    # Generate PDF and store path in case
    pdf_path = generate_pdf(scraped_data, os.path.join(TEMP_DIR, f'temp_{case_number}.pdf'))
    case.judgment_pdf_link = pdf_path  # Update with the generated PDF path
    db.session.commit()

    return jsonify(scraped_data)

@bp.route('/download/<case_number>', methods=['GET'])
def download_pdf(case_number):
    case = Case.query.filter_by(case_number=case_number).first_or_404()
    pdf_path = case.judgment_pdf_link or os.path.join(TEMP_DIR, f'temp_{case_number}.pdf')

    if not os.path.exists(pdf_path):
        # Regenerate PDF using case data
        case_data = {
            'court': case.court,
            'case_type': case.case_type,
            'case_number': case.case_number,
            'filing_year': case.filing_year,
            'cnr_number': case.cnr_number,
            'status': case.status,
            'parties': case.parties,
            'dealing_assistant': case.dealing_assistant,
            'filing_advocate': case.filing_advocate,
            'subject1': case.subject1,
            'subject2': case.subject2,
            'filing_date': case.filing_date,
            'registration_date': case.registration_date,
            'next_hearing_date': case.next_hearing_date,
            'order_date': case.order_date,
            'judgment_pdf_link': case.judgment_pdf_link,
        }
        pdf_path = generate_pdf(case_data, os.path.join(TEMP_DIR, f'temp_{case_number}.pdf'))
        if not os.path.exists(pdf_path):
            return jsonify({'error': 'Failed to generate PDF'}), 500

    try:
        return send_file(pdf_path, as_attachment=True, download_name=f'case_{case_number}.pdf')
    except Exception as e:
        print(f"Error sending file: {e}")
        return jsonify({'error': 'File not found or inaccessible'}), 500