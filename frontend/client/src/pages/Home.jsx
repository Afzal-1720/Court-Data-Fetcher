import React from 'react';
import CaseForm from '../components/CaseForm';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-4">
      <h1 className="text-4xl md:text-5xl font-bold text-blue-800 mb-8 text-center drop-shadow-sm">
        Court Data Fetcher
      </h1>
      <CaseForm />
    </div>
  );
};

export default Home;
