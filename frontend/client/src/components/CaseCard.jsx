import React from 'react';
import DownloadPDFButton from './DownloadPDFButton';

const CaseCard = ({ caseData }) => {
  const getValue = (field) => caseData[field] || 'N/A';

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-4 fade-in hover:shadow-lg transition-shadow duration-300">
      <h3 className="text-xl font-semibold text-gray-800 mb-4">Case Details</h3>

      <p className="text-gray-600"><strong>Case Type:</strong> {getValue('case_type')}</p>
      <p className="text-gray-600"><strong>Case Number:</strong> {getValue('case_number')}</p>
      <p className="text-gray-600"><strong>CNR Number:</strong> {getValue('cnr_number')}</p>
      <p className="text-gray-600"><strong>Status:</strong> {getValue('status')}</p>
      <p className="text-gray-600"><strong>Filing Year:</strong> {getValue('filing_year')}</p>
      <p className="text-gray-600"><strong>Parties:</strong> {getValue('parties')}</p>
      <p className="text-gray-600"><strong>Dealing Assistant:</strong> {getValue('dealing_assistant')}</p>
      <p className="text-gray-600"><strong>Filing Advocate:</strong> {getValue('filing_advocate')}</p>
      <p className="text-gray-600"><strong>Subject 1:</strong> {getValue('subject1')}</p>
      <p className="text-gray-600"><strong>Subject 2:</strong> {getValue('subject2')}</p>
      <p className="text-gray-600"><strong>Date of Filing:</strong> {getValue('filing_date')}</p>
      <p className="text-gray-600"><strong>Date of Registration:</strong> {getValue('registration_date')}</p>
      <p className="text-gray-600"><strong>Next Hearing Date:</strong> {getValue('next_hearing_date')}</p>
      <p className="text-gray-600"><strong>Order Date:</strong> {getValue('order_date')}</p>

      <DownloadPDFButton
        pdfLink={caseData.judgment_pdf_link}
        caseNumber={caseData.case_number}
      />
    </div>
  );
};

export default CaseCard;
