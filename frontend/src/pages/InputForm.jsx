import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Sparkles, Loader2 } from 'lucide-react';

export default function InputForm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    Name: '',
    Gender: 'Not Specified',
    Age: 25,
    Height: 175,
    Weight: 70,
    Fitness_Goal: 'Maintain',
    Daily_Calories: 2000,
    Daily_Protein: 100,
    Daily_Carbs: 250,
    Daily_Fat: 65,
    Daily_Fiber: 30,
    Daily_Budget: 300,
    Weekly_Budget: 2100,
    Is_Vegetarian: false,
    Cuisine_Preference: 'Any',
    Meal_Type: 'Any',
    Max_Prep_Time: 60,
    Goal: 'Balanced Nutrition'
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : (type === 'number' ? Number(value) : value)
    });
  };

  const handleDemo = () => {
    setFormData({
      Name: 'Alex',
      Gender: 'Male',
      Age: 22,
      Height: 165,
      Weight: 65,
      Fitness_Goal: 'Cut',
      Daily_Calories: 1850,
      Daily_Protein: 120,
      Daily_Carbs: 200,
      Daily_Fat: 60,
      Daily_Fiber: 35,
      Daily_Budget: 250,
      Weekly_Budget: 1500,
      Is_Vegetarian: true,
      Cuisine_Preference: 'Indian',
      Meal_Type: 'Any',
      Max_Prep_Time: 30,
      Goal: 'High Protein'
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic Validation
    if (formData.Daily_Budget < 0 || formData.Daily_Calories <= 0) {
      setError("Please enter valid positive numbers for targets.");
      setLoading(false);
      return;
    }

    try {
      // Calculate BMI (Weight in kg / Height in m squared)
      const heightInMeters = formData.Height / 100;
      const bmi = parseFloat((formData.Weight / (heightInMeters * heightInMeters)).toFixed(1));
      
      const payload = {
        ...formData,
        BMI: bmi
      };

      const response = await axios.post('http://localhost:8000/predict', payload);
      // Store result in sessionStorage to pass to dashboard
      sessionStorage.setItem('recommendations', JSON.stringify(response.data));
      sessionStorage.setItem('userInput', JSON.stringify(payload));
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to connect to backend server. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Personal Requirements</h1>
          <p className="text-gray-500 mt-2">Enter your targets to let the AI build your plan.</p>
        </div>
        <button 
          type="button" 
          onClick={handleDemo}
          className="flex items-center gap-2 bg-indigo-100 text-indigo-700 px-4 py-2 rounded-lg font-medium hover:bg-indigo-200 transition-colors"
        >
          <Sparkles className="w-5 h-5" /> Load Demo User
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6 border border-red-200">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8 bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
        
        {/* Section 1: Demographics & Macros */}
        <div>
          <h2 className="text-xl font-semibold text-gray-800 border-b pb-2 mb-6">Personal & Nutrition Targets</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input type="text" name="Name" value={formData.Name} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
              <select name="Gender" value={formData.Gender} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary bg-white">
                <option value="Not Specified">Not Specified</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
              <input type="number" name="Age" value={formData.Age} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Height (cm)</label>
              <input type="number" name="Height" value={formData.Height} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Weight (kg)</label>
              <input type="number" name="Weight" value={formData.Weight} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fitness Goal</label>
              <select name="Fitness_Goal" value={formData.Fitness_Goal} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary bg-white">
                <option value="Maintain">Maintain Weight</option>
                <option value="Cut">Weight Loss (Cut)</option>
                <option value="Bulk">Muscle Gain (Bulk)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Calories (kcal/day)</label>
              <input type="number" name="Daily_Calories" value={formData.Daily_Calories} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Protein (g/day)</label>
              <input type="number" name="Daily_Protein" value={formData.Daily_Protein} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Carbs (g/day)</label>
              <input type="number" name="Daily_Carbs" value={formData.Daily_Carbs} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fat (g/day)</label>
              <input type="number" name="Daily_Fat" value={formData.Daily_Fat} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fiber (g/day)</label>
              <input type="number" name="Daily_Fiber" value={formData.Daily_Fiber} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
          </div>
        </div>

        {/* Section 2: Budget */}
        <div>
          <h2 className="text-xl font-semibold text-gray-800 border-b pb-2 mb-6">Budget Limitations</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Daily Budget (₹)</label>
              <input type="number" name="Daily_Budget" value={formData.Daily_Budget} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Weekly Budget (₹)</label>
              <input type="number" name="Weekly_Budget" value={formData.Weekly_Budget} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" required />
            </div>
          </div>
        </div>

        {/* Section 3: Preferences */}
        <div>
          <h2 className="text-xl font-semibold text-gray-800 border-b pb-2 mb-6">Preferences & Constraints</h2>
          
          <div className="mb-6 flex items-center">
            <input type="checkbox" id="Is_Vegetarian" name="Is_Vegetarian" checked={formData.Is_Vegetarian} onChange={handleChange} className="w-5 h-5 text-primary rounded border-gray-300 focus:ring-primary" />
            <label htmlFor="Is_Vegetarian" className="ml-3 font-medium text-gray-800">Strictly Vegetarian Diet</label>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Cuisine Preference</label>
              <select name="Cuisine_Preference" value={formData.Cuisine_Preference} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary bg-white">
                <option value="Any">Any</option>
                <option value="Indian">Indian</option>
                <option value="Italian">Italian</option>
                <option value="American">American</option>
                <option value="Mexican">Mexican</option>
                <option value="Asian">Asian</option>
                <option value="Mediterranean">Mediterranean</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Goal</label>
              <select name="Goal" value={formData.Goal} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary bg-white">
                <option value="Balanced Nutrition">Balanced Nutrition</option>
                <option value="High Protein">High Protein</option>
                <option value="Low Cost">Low Cost</option>
                <option value="Weight Management">Weight Management</option>
                <option value="General Healthy Eating">General Healthy Eating</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Max Prep Time (mins)</label>
              <input type="number" name="Max_Prep_Time" value={formData.Max_Prep_Time} onChange={handleChange} className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-primary focus:border-transparent" />
            </div>
          </div>
        </div>

        <div className="pt-4 border-t">
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-primary hover:bg-primary-dark text-white font-bold text-xl py-4 rounded-xl transition-colors shadow-md flex justify-center items-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Loader2 className="w-6 h-6" />}
            {loading ? 'Running ML Pipeline...' : 'Generate AI Recommendations'}
          </button>
        </div>
      </form>
    </div>
  );
}
