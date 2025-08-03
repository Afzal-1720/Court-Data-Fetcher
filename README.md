🏛️ Court Data Fetcher

Court Data Fetcher is a full-stack application that automates the retrieval of case history data from the [Delhi High Court](https://dhcmisc.nic.in/pcase/guiCaseWise.php) website using Playwright and Python. It allows users to submit case details and view a summary of court records, with an option to generate a PDF report.



 📌 Features

- 🔍 Automated form filling with CAPTCHA input
- 📄 Case history data extraction (case number, CNR, status, parties, filing info, etc.)
- 🧾 PDF report generation using ReportLab
- 🖥️ Interactive frontend built with React.js
- ⚙️ Backend API powered by Flask
- 🛡️ Error handling with retry logic and graceful timeouts



 🔧 Tech Stack

| Layer      | Technology               |
|------------|--------------------------|
| Frontend   | React.js, Tailwind CSS   |
| Backend    | Flask (Python)           |
| Scraper    | Playwright (async Python)|
| PDF Gen    | ReportLab                |
|  Database  |  PostgresSQL             |


🚀 Getting Started

 📁 Clone the Repository

git clone https://github.com/Afzal-1720/Court-Data-Fetcher.git
cd Court-Data-Fetcher

⚙️ Backend Setup
Navigate to Backend Directory:
cd backend
Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Install Playwright browsers:
playwright install

Run Flask API:
python app.py
API runs at http://127.0.0.1:5000

🌐 Frontend Setup
Navigate to Frontend Directory:
cd ../frontend
Install dependencies:
npm install

Run React Development Server:
npm start
App runs at http://localhost:3000

📝 Usage
Open the app in your browser.

Enter the Case Type, Case Number, and Year.

Manually enter the CAPTCHA displayed from the DHC website.

Click Submit to fetch case details.

Optionally, click Download PDF to save a report of the case.


📌 To-Do
✅ Extract all case fields from HTML reliably

✅ Fix selector timeouts and improve fallback logic

🚧 Add support for other court portals (future)

🚧 Implement CAPTCHA OCR (optional feature)

❗Known Limitations
CAPTCHA must be entered manually by the user.

Site structure changes may break the scraper — built for https://dhcmisc.nic.in/pcase/guiCaseWise.php

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📄 License
This project is licensed under the MIT License — see LICENSE file for details.

✨ Acknowledgements
Delhi High Court Portal

Microsoft Playwright

ReportLab PDF Toolkit

🧑‍💻 Developed By
Muhammad Afzal
GitHub: Afzal-1720













