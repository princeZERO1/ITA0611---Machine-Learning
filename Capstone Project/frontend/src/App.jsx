import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import InputForm from './pages/InputForm';
import Dashboard from './pages/Dashboard';
import MachineLearning from './pages/MachineLearning';
import Dataset from './pages/Dataset';
import Users from './pages/Users';
import { LayoutDashboard, BrainCircuit, TableProperties, Home as HomeIcon, UtensilsCrossed, Users as UsersIcon } from 'lucide-react';

function Navigation() {
  const location = useLocation();
  const path = location.pathname;

  const getLinkClass = (p) => {
    return path === p 
      ? "text-primary border-b-2 border-primary font-semibold flex items-center gap-2 py-4 px-2"
      : "text-gray-500 hover:text-gray-800 flex items-center gap-2 py-4 px-2 transition-colors";
  };

  return (
    <nav className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex gap-8 overflow-x-auto no-scrollbar">
            <Link to="/" className={getLinkClass('/')}><HomeIcon size={18}/> Home</Link>
            <Link to="/input" className={getLinkClass('/input')}><UtensilsCrossed size={18}/> Get Plan</Link>
            <Link to="/dashboard" className={getLinkClass('/dashboard')}><LayoutDashboard size={18}/> Dashboard</Link>
            <Link to="/ml" className={getLinkClass('/ml')}><BrainCircuit size={18}/> ML Model</Link>
            <Link to="/dataset" className={getLinkClass('/dataset')}><TableProperties size={18}/> Dataset</Link>
            <Link to="/users" className={getLinkClass('/users')}><UsersIcon size={18}/> Users</Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navigation />
        <main className="max-w-7xl mx-auto p-4 flex-1 w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/input" element={<InputForm />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/ml" element={<MachineLearning />} />
            <Route path="/dataset" element={<Dataset />} />
            <Route path="/users" element={<Users />} />
          </Routes>
        </main>
        <footer className="bg-white border-t border-gray-200 py-6 text-center text-gray-500 text-sm mt-auto">
          <p>NutriBudget AI - Machine Learning Capstone Project &copy; 2026</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}
