import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import CaseCard from '../components/CaseCard';

const Dashboard = () => {
  const location = useLocation();
  const [caseData, setCaseData] = useState(location.state || {});

  useEffect(() => {
    if (!Object.keys(caseData).length) {
      setCaseData({ case_type: 'No data', case_number: 'N/A', message: 'Please submit a case first.' });
    }
  }, [caseData]);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-gray-800 text-center mb-6 slide-up">Case Dashboard</h1>
      {Array.isArray(caseData) ? (
        caseData.map((caseItem, index) => <CaseCard key={index} caseData={caseItem} />)
      ) : (
        <CaseCard caseData={caseData} />
      )}
    </div>
  );
};

export default Dashboard;