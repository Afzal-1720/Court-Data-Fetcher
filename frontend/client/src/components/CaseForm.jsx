import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitCase } from '../services/api';

const CaseForm = () => {
  const [formData, setFormData] = useState({
    court: 'Delhi High Court',
    caseType: '',
    caseNumber: '',
    filingYear: '',
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await submitCase(formData);
      navigate('/dashboard', { state: response.data }); // Pass JSON to Dashboard
    } catch (error) {
      console.error('Error submitting case:', error);
      alert('Failed to fetch data. Please try again. Error: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg slide-up">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Submit Case Details</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Court</label>
          <select
            name="court"
            value={formData.court}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="Delhi High Court">Delhi High Court</option>
            <option value="Faridabad District Court">Faridabad District Court</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Case Type</label>
          <input
            type="text"
            name="caseType"
            value={formData.caseType}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Case Number</label>
          <input
            type="text"
            name="caseNumber"
            value={formData.caseNumber}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Filing Year</label>
          <input
            type="number"
            name="filingYear"
            value={formData.filingYear}
            onChange={handleChange}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition duration-300 ease-in-out disabled:bg-gray-400"
        >
          {loading ? 'Fetching...' : 'Submit'}
        </button>
      </form>
    </div>
  );
};

export default CaseForm;