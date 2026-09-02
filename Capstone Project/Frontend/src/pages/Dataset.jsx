import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Search, ChevronLeft, ChevronRight, Filter } from 'lucide-react';

export default function Dataset() {
  const [data, setData] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const limit = 20;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/meals?page=${page}&limit=${limit}&search=${search}`);
        setData(res.data.data);
        setTotal(res.data.total);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, [page, search]);

  const handleSearch = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="py-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Synthetic Meal Dataset</h1>
          <p className="text-gray-500 mt-1">Explore the {total} records used to train the Random Forest model.</p>
        </div>
        
        <div className="relative w-full md:w-72">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input 
            type="text" 
            placeholder="Search meals or cuisines..." 
            value={search}
            onChange={handleSearch}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-200 text-gray-500 text-sm uppercase tracking-wider">
                <th className="p-4 font-medium">Meal Name</th>
                <th className="p-4 font-medium">Cuisine</th>
                <th className="p-4 font-medium">Type</th>
                <th className="p-4 font-medium text-right">Calories</th>
                <th className="p-4 font-medium text-right">Protein</th>
                <th className="p-4 font-medium text-right">Cost</th>
                <th className="p-4 font-medium text-center">Veg</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data.map((meal, idx) => (
                <tr key={idx} className="hover:bg-gray-50 transition-colors">
                  <td className="p-4 font-medium text-gray-900">{meal.Meal_Name}</td>
                  <td className="p-4 text-gray-600">{meal.Cuisine}</td>
                  <td className="p-4 text-gray-600">
                    <span className="bg-gray-100 px-2 py-1 rounded-md text-xs font-bold">{meal.Meal_Type}</span>
                  </td>
                  <td className="p-4 text-gray-600 text-right">{meal.Calories} kcal</td>
                  <td className="p-4 text-gray-600 text-right">{meal.Protein}g</td>
                  <td className="p-4 text-gray-900 font-medium text-right">₹{meal.Cost}</td>
                  <td className="p-4 text-center">
                    {meal.Is_Vegetarian === 1 ? 
                      <span className="text-green-600 bg-green-50 px-2 py-1 rounded text-xs font-bold">Yes</span> : 
                      <span className="text-red-600 bg-red-50 px-2 py-1 rounded text-xs font-bold">No</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Pagination */}
        <div className="p-4 border-t border-gray-200 flex items-center justify-between bg-gray-50">
          <span className="text-sm text-gray-600">Showing {Math.min(1 + (page-1)*limit, total)} to {Math.min(page*limit, total)} of {total} entries</span>
          <div className="flex gap-2">
            <button 
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 border border-gray-300 rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button 
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages || totalPages === 0}
              className="p-2 border border-gray-300 rounded-lg hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
