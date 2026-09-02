import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Users as UsersIcon, User, Calendar, Activity, Target, ChevronDown, ChevronUp } from 'lucide-react';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedUser, setExpandedUser] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await axios.get('http://localhost:8000/users');
        setUsers(res.data.users);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);

  if (loading) {
    return <div className="p-10 text-center">Loading User Data...</div>;
  }

  return (
    <div className="py-6 max-w-7xl mx-auto px-4">
      <div className="flex items-center gap-3 mb-8">
        <UsersIcon className="w-8 h-8 text-primary" />
        <h1 className="text-3xl font-bold text-gray-900">User History</h1>
      </div>
      
      {users.length === 0 ? (
        <div className="text-center p-12 bg-white rounded-2xl border border-gray-100 shadow-sm text-gray-500">
          No users have generated a meal plan yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {users.map((u, i) => (
            <div 
              key={i} 
              className={`bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition cursor-pointer ${expandedUser === i ? 'ring-2 ring-primary ring-opacity-50' : ''}`}
              onClick={() => setExpandedUser(expandedUser === i ? null : i)}
            >
              <div className="flex items-center gap-3 mb-4 border-b pb-4">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center text-primary font-bold text-xl">
                  {u.Name.charAt(0).toUpperCase()}
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 text-lg">{u.Name}</h3>
                  <div className="text-sm text-gray-500 flex items-center gap-2">
                    <User size={14}/> {u.Gender} • {u.Age} yrs
                  </div>
                </div>
                <div>
                  {expandedUser === i ? <ChevronUp className="text-gray-400" /> : <ChevronDown className="text-gray-400" />}
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500 flex items-center gap-1"><Activity size={16}/> BMI</span>
                  <span className="font-bold text-gray-800">{u.BMI}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500 flex items-center gap-1"><Target size={16}/> Fitness Goal</span>
                  <span className="font-bold text-primary">{u.Fitness_Goal}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-500 flex items-center gap-1"><Calendar size={16}/> Last Plan Generated</span>
                  <span className="font-medium text-gray-700">{u.Timestamp ? u.Timestamp.split(' ')[0] : 'Unknown'}</span>
                </div>
              </div>

              {expandedUser === i && (
                <div className="mt-4 pt-4 border-t border-gray-100 animate-in fade-in slide-in-from-top-2 duration-200">
                  <h4 className="font-bold text-gray-800 mb-3 text-sm">Recommended Daily Plan:</h4>
                  {u.Daily_Plan ? (
                    <div className="space-y-3">
                      {Object.entries(u.Daily_Plan).map(([mealType, meal]) => (
                        <div key={mealType} className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                          <div className="text-xs font-bold text-primary mb-1 uppercase tracking-wider">{mealType}</div>
                          <div className="text-sm font-medium text-gray-800">{meal.Meal_Name}</div>
                          <div className="text-xs text-gray-500 mt-1">{meal.Calories} kcal • {meal.Protein}g Protein</div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-sm text-gray-500 italic bg-gray-50 p-3 rounded-lg">
                      Plan details were not recorded for this past session.
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
