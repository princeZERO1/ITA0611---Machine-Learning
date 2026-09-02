import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { Activity, Wallet, Target, Star, Leaf, Clock, CheckCircle, Sparkles } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [user, setUser] = useState(null);

  const [missingIngredients, setMissingIngredients] = useState({});

  const toggleMissing = (mealType) => {
    setMissingIngredients(prev => ({
      ...prev,
      [mealType]: !prev[mealType]
    }));
  };

  useEffect(() => {
    const rawData = sessionStorage.getItem('recommendations');
    const rawUser = sessionStorage.getItem('userInput');
    if (!rawData || !rawUser) {
      navigate('/input');
      return;
    }
    setData(JSON.parse(rawData));
    setUser(JSON.parse(rawUser));
  }, [navigate]);

  if (!data || !user) return <div className="p-10 text-center">Loading Dashboard...</div>;

  // Chart Colors
  const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'];
  const BUDGET_COLORS = ['#10b981', '#e5e7eb'];

  // Nutrition Comparison Data
  const nutritionData = [
    { name: 'Calories', Target: user.Daily_Calories, Recommended: data.daily_totals.Calories },
    { name: 'Protein', Target: user.Daily_Protein, Recommended: data.daily_totals.Protein },
    { name: 'Carbs', Target: user.Daily_Carbs, Recommended: data.daily_totals.Carbs },
    { name: 'Fat', Target: user.Daily_Fat, Recommended: data.daily_totals.Fat },
    { name: 'Fiber', Target: user.Daily_Fiber, Recommended: data.daily_totals.Fiber },
  ];

  // Budget Data
  const dailySpent = data.daily_totals.Cost;
  const dailyRemaining = Math.max(0, user.Daily_Budget - dailySpent);
  const budgetPieData = [
    { name: 'Spent', value: dailySpent },
    { name: 'Remaining', value: dailyRemaining },
  ];
  
  const getBmiCategory = (bmi) => {
    if (bmi < 18.5) return 'Underweight';
    if (bmi >= 18.5 && bmi < 25) return 'Normal';
    if (bmi >= 25 && bmi < 30) return 'Overweight';
    return 'Obese';
  };

  return (
    <div className="space-y-8 pb-10">
      
      {/* Header Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        
        {/* BMI Card */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium mb-1">{user.Name ? `${user.Name}'s` : 'Your'} BMI</div>
          <div className="flex justify-between items-end">
            <div>
              <span className="text-3xl font-bold text-gray-900">{user.BMI}</span>
            </div>
            <div className="bg-purple-100 p-2 rounded-lg text-purple-600"><Target size={20} /></div>
          </div>
          <div className="mt-4 text-sm font-bold text-purple-600">
            {getBmiCategory(user.BMI)} 
            {user.Gender && user.Gender !== 'Not Specified' && <span className="font-normal text-gray-400"> • {user.Gender}</span>}
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium mb-1">Daily Nutrition</div>
          <div className="flex justify-between items-end">
            <div>
              <span className="text-3xl font-bold text-gray-900">{data.daily_totals.Calories}</span>
              <span className="text-gray-500 ml-1">kcal</span>
            </div>
            <div className="bg-green-100 p-2 rounded-lg text-primary-dark"><Activity size={20} /></div>
          </div>
          <div className="w-full bg-gray-200 h-2 rounded-full mt-4 overflow-hidden">
            <div className="bg-primary h-full" style={{ width: `${Math.min(100, (data.daily_totals.Calories / user.Daily_Calories) * 100)}%` }}></div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium mb-1">Total Cost</div>
          <div className="flex justify-between items-end">
            <div>
              <span className="text-3xl font-bold text-gray-900">₹{data.daily_totals.Cost}</span>
            </div>
            <div className="bg-blue-100 p-2 rounded-lg text-blue-600"><Wallet size={20} /></div>
          </div>
          <div className="w-full bg-gray-200 h-2 rounded-full mt-4 overflow-hidden">
            <div className="bg-blue-500 h-full" style={{ width: `${Math.min(100, (data.daily_totals.Cost / user.Daily_Budget) * 100)}%` }}></div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium mb-1">Protein Hit</div>
          <div className="flex justify-between items-end">
            <div>
              <span className="text-3xl font-bold text-gray-900">{data.daily_totals.Protein}g</span>
            </div>
            <div className="bg-yellow-100 p-2 rounded-lg text-yellow-600"><Target size={20} /></div>
          </div>
          <div className="w-full bg-gray-200 h-2 rounded-full mt-4 overflow-hidden">
            <div className="bg-yellow-500 h-full" style={{ width: `${Math.min(100, (data.daily_totals.Protein / user.Daily_Protein) * 100)}%` }}></div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
          <div className="text-gray-500 text-sm font-medium mb-1">Budget Status</div>
          <div className="flex justify-between items-end">
            <div>
              <span className="text-xl font-bold text-gray-900">{dailyRemaining > 0 ? `₹${dailyRemaining} Saved` : 'Over Budget'}</span>
            </div>
            <div className="bg-green-100 p-2 rounded-lg text-primary-dark"><CheckCircle size={20} /></div>
          </div>
          <div className="mt-4 text-sm text-gray-500">Weekly Est: ₹{data.weekly_totals.Cost} / ₹{user.Weekly_Budget}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Meal Plan & Recommendations */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Daily Meal Plan */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 border-b pb-4">
              {user.Name ? `${user.Name}'s AI Recommended Meal Plan` : "Today's AI Recommended Meal Plan"}
            </h2>
            <div className="space-y-4">
              {['Breakfast', 'Lunch', 'Snack', 'Dinner'].map((type, idx) => {
                const meal = data.daily_plan[type];
                if (!meal) return null;
                return (
                  <React.Fragment key={idx}>
                  <div className="flex flex-col sm:flex-row items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-green-50 transition-colors">
                    <div className="flex-1">
                      <span className="text-xs font-bold text-primary tracking-wider uppercase mb-1 block">{type}</span>
                      <h3 className="font-bold text-gray-800 text-lg">{meal.Meal_Name}</h3>
                      <div className="flex flex-wrap gap-3 text-sm text-gray-500 mt-2">
                        <span className="flex items-center gap-1"><Activity size={14}/> {meal.Calories} kcal</span>
                        <span className="flex items-center gap-1"><Target size={14}/> {meal.Protein}g P</span>
                        {meal.Is_Vegetarian === 1 && <span className="flex items-center gap-1 text-green-600"><Leaf size={14}/> Veg</span>}
                        <span className="flex items-center gap-1"><Clock size={14}/> {meal.Prep_Time} min</span>
                      </div>
                    </div>
                    <div className="mt-4 sm:mt-0 text-right flex flex-col items-end gap-2">
                      <div className="text-xl font-bold text-gray-900">₹{meal.Cost}</div>
                      <div className="text-xs font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded-md inline-block">
                        AI Score: {meal.Suitability_Score.toFixed(0)}/100
                      </div>
                      
                      <button 
                        onClick={() => toggleMissing(type)}
                        className={`text-xs font-bold px-3 py-1.5 rounded-md mt-2 transition-colors ${missingIngredients[type] ? 'bg-red-100 text-red-600' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                      >
                        {missingIngredients[type] ? 'Missing Ingredients!' : 'Have Ingredients?'}
                      </button>
                    </div>
                  </div>
                  
                  {missingIngredients[type] && (
                    <div className="mt-2 p-3 bg-red-50 border border-red-100 rounded-lg flex flex-col sm:flex-row gap-3 items-center justify-between text-sm">
                      <span className="text-red-700 font-medium">Order instead or find a restaurant:</span>
                      <div className="flex gap-2">
                        <a href={`https://www.zomato.com/search?q=${encodeURIComponent(meal.Meal_Name)}`} target="_blank" rel="noreferrer" className="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-md font-bold transition">Zomato</a>
                        <a href={`https://www.swiggy.com/search?res=${encodeURIComponent(meal.Meal_Name)}`} target="_blank" rel="noreferrer" className="bg-orange-500 hover:bg-orange-600 text-white px-3 py-1.5 rounded-md font-bold transition">Swiggy</a>
                        <a href={`https://www.google.com/maps/search/nearest+restaurant+serving+${encodeURIComponent(meal.Meal_Name)}`} target="_blank" rel="noreferrer" className="bg-green-600 hover:bg-green-700 text-white px-3 py-1.5 rounded-md font-bold transition">Maps</a>
                      </div>
                    </div>
                  )}
                  </React.Fragment>
                );
              })}
            </div>
          </div>

          {/* Top 5 Recommendations */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 border-b pb-4">Top Highly Rated Meals</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.top_recommendations.slice(0, 6).map((meal, idx) => (
                <div key={idx} className="border border-gray-200 rounded-xl p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-gray-800 leading-tight pr-2">{meal.Meal_Name}</h3>
                    <span className="bg-gray-100 text-gray-800 text-xs font-bold px-2 py-1 rounded-md">{meal.Meal_Type}</span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600 mt-3 border-t pt-3">
                    <span>{meal.Calories} kcal</span>
                    <span>₹{meal.Cost}</span>
                    <span className="flex items-center gap-1 text-yellow-500 font-bold"><Star size={14} fill="currentColor"/> {meal.Base_Rating}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: Charts */}
        <div className="space-y-8">
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Budget Breakdown</h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={budgetPieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {budgetPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={BUDGET_COLORS[index % BUDGET_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `₹${value}`} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="text-center mt-2">
              <p className="text-gray-500">Daily Budget: <span className="font-bold text-gray-800">₹{user.Daily_Budget}</span></p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Nutrition Match</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={nutritionData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={60} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="Target" fill="#e5e7eb" radius={[0, 4, 4, 0]} />
                  <Bar dataKey="Recommended" fill="#10b981" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-green-50 p-6 rounded-2xl border border-green-100">
             <h3 className="font-bold text-primary-dark mb-2 flex items-center gap-2"><Sparkles size={18}/> Why this meal plan?</h3>
             <ul className="text-sm text-green-800 space-y-2">
               <li>• Balanced nutrition carefully mapped to your macros</li>
               <li>• Random Forest confirmed {data.daily_plan['Breakfast'].Suitability_Score.toFixed(0)}% suitability</li>
               <li>• Preserves ₹{dailyRemaining} of your daily budget</li>
               <li>• Filters applied for your {user.Cuisine_Preference} cuisine preference</li>
             </ul>
          </div>
          
        </div>
      </div>
    </div>
  );
}
