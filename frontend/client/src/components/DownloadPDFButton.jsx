import React from 'react';
import { downloadPDF } from '../services/api';

const DownloadPDFButton = ({ pdfLink, caseNumber }) => {
  const handleDownload = async () => {
    if (pdfLink) {
      window.open(pdfLink, '_blank');
    } else {
      try {
        const response = await downloadPDF(caseNumber);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `case_${caseNumber}.pdf`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error(error);
        alert('No PDF available or error downloading.');
      }
    }
  };

  return (
    <button
      onClick={handleDownload}
      className="mt-4 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition duration-300 ease-in-out disabled:bg-gray-400"
      disabled={!pdfLink && !caseNumber}
    >
      Download PDF
    </button>
  );
};

export default DownloadPDFButton;