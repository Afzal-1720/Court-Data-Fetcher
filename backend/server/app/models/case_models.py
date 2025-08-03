from app import db

class Case(db.Model):
    __tablename__ = 'cases'  # Renamed to avoid SQL reserved word conflict

    id = db.Column(db.Integer, primary_key=True)
    court = db.Column(db.String(128))
    case_type = db.Column(db.String(128))
    case_number = db.Column(db.String(128))
    filing_year = db.Column(db.String(128))
    case_id = db.Column(db.String(128))
    cnr_number = db.Column(db.String(128))
    status = db.Column(db.String(128))
    parties = db.Column(db.String(256))
    dealing_assistant = db.Column(db.String(128))
    filing_advocate = db.Column(db.String(128))
    subject1 = db.Column(db.String(256))
    subject2 = db.Column(db.String(256))
    filing_date = db.Column(db.String(128))
    registration_date = db.Column(db.String(128))
    next_hearing_date = db.Column(db.String(128))
    order_date = db.Column(db.String(128))
    judgment_pdf_link = db.Column(db.String(512))


class ScrapingLog(db.Model):
    __tablename__ = 'scraping_logs'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.now())
    error_message = db.Column(db.Text)