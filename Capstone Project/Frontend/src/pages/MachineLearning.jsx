import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend, LineChart, Line, ScatterChart, Scatter, AreaChart, Area } from 'recharts';
import { Brain, Cpu, Database, SplitSquareVertical, Settings, TrendingUp, Target } from 'lucide-react';

export default function MachineLearning() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await axios.get('http://localhost:8000/model-metrics');
        setMetrics(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  if (loading) return <div className="p-10 text-center">Loading Model Details...</div>;
  if (!metrics || !metrics.metrics || Object.keys(metrics.metrics).length === 0) return <div className="p-10 text-center text-gray-600">No model trained yet. Go to <b>'Get Plan'</b> and generate recommendations first to run the ML pipeline!</div>;

  const chartData = metrics.feature_importances.map(f => ({
    name: f.Feature.replace('Meal_Type_', '').replace('Cuisine_', ''),
    Importance: parseFloat((f.Importance * 100).toFixed(2))
  }));

  // Actual vs Predicted data
  const predictionData = metrics.actual_vs_predicted || [];
  
  // Error distribution data (binned)
  const errors = predictionData.map(p => parseFloat((p.Predicted - p.Actual).toFixed(2)));
  const errorBins = {};
  errors.forEach(e => {
    const bin = Math.round(e / 2) * 2; // bin size of 2
    errorBins[bin] = (errorBins[bin] || 0) + 1;
  });
  const errorDistribution = Object.entries(errorBins)
    .map(([bin, count]) => ({ Error: parseFloat(bin), Count: count }))
    .sort((a, b) => a.Error - b.Error);

  // Accuracy metrics for bar chart
  const accuracyData = [
    { name: 'R² Score', value: parseFloat((metrics.metrics.R2 * 100).toFixed(1)), fill: '#10b981' },
    { name: 'Accuracy', value: parseFloat(Math.max(0, 100 - metrics.metrics.RMSE).toFixed(1)), fill: '#3b82f6' },
  ];

  const errorMetricsData = [
    { name: 'MSE', value: metrics.metrics.MSE, fill: '#ef4444' },
    { name: 'RMSE', value: metrics.metrics.RMSE, fill: '#f59e0b' },
    { name: 'MAE', value: metrics.metrics.MAE, fill: '#8b5cf6' },
  ];

  const modelParams = metrics.model_params || {};
  
  // Classification Metrics
  const precision = metrics.metrics.Precision != null ? (metrics.metrics.Precision * 100).toFixed(1) : 0;
  const recall = metrics.metrics.Recall != null ? (metrics.metrics.Recall * 100).toFixed(1) : 0;
  const f1Score = metrics.metrics.F1_Score != null ? (metrics.metrics.F1_Score * 100).toFixed(1) : 0;
  const cm = metrics.metrics.Confusion_Matrix || [[0, 0], [0, 0]];
  const [tn, fp, fn, tp] = [cm[0][0], cm[0][1], cm[1][0], cm[1][1]];

  return (
    <div className="space-y-8 py-6">
      
      <div className="text-center max-w-3xl mx-auto mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Explainable AI & Model Performance</h1>
        <p className="text-gray-600">
          This project uses a <b>Random Forest Regressor</b> to map user preferences and constraints to thousands of possible meal combinations, calculating an optimal Suitability Score.
        </p>
      </div>

      {/* Model Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-gray-200 text-center shadow-sm hover:shadow-md transition">
          <Database className="w-8 h-8 text-primary mx-auto mb-3" />
          <div className="text-sm text-gray-500 font-medium">Training Samples</div>
          <div className="text-3xl font-bold text-gray-900">{metrics.metrics.Train_Samples}</div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-200 text-center shadow-sm hover:shadow-md transition">
          <SplitSquareVertical className="w-8 h-8 text-blue-500 mx-auto mb-3" />
          <div className="text-sm text-gray-500 font-medium">Testing Samples</div>
          <div className="text-3xl font-bold text-gray-900">{metrics.metrics.Test_Samples}</div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-200 text-center shadow-sm hover:shadow-md transition">
          <Brain className="w-8 h-8 text-purple-500 mx-auto mb-3" />
          <div className="text-sm text-gray-500 font-medium">Model R² Score</div>
          <div className="text-3xl font-bold text-gray-900">{(metrics.metrics.R2 * 100).toFixed(1)}%</div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-200 text-center shadow-sm hover:shadow-md transition">
          <Cpu className="w-8 h-8 text-red-500 mx-auto mb-3" />
          <div className="text-sm text-gray-500 font-medium">RMSE Error</div>
          <div className="text-3xl font-bold text-gray-900">{metrics.metrics.RMSE}</div>
        </div>
      </div>

      {/* NEW: Actual vs Predicted + Accuracy Graphs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* Actual vs Predicted Line Chart */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2"><TrendingUp className="w-6 h-6 text-primary" /> Actual vs Predicted Scores</h2>
          <p className="text-gray-500 text-sm mb-6">How closely does the model's prediction match the actual suitability score?</p>
          <div className="h-80">
            {predictionData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={predictionData} margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="Actual" label={{ value: 'Sample Index', position: 'bottom', offset: -5 }} tick={false} />
                  <YAxis label={{ value: 'Score', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="Actual" stroke="#3b82f6" strokeWidth={2} dot={false} name="Actual Score" />
                  <Line type="monotone" dataKey="Predicted" stroke="#10b981" strokeWidth={2} dot={false} name="Predicted Score" />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400">Run a prediction first to see this graph.</div>
            )}
          </div>
        </div>

        {/* Model Accuracy & Error Metrics */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2"><Target className="w-6 h-6 text-blue-500" /> Accuracy & Error Metrics</h2>
          <p className="text-gray-500 text-sm mb-6">Visual comparison of model accuracy and different error measures.</p>
          <div className="h-36 mb-6">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={accuracyData} layout="vertical" margin={{ top: 5, right: 30, left: 60, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={true} horizontal={false} />
                <XAxis type="number" domain={[0, 100]} unit="%" />
                <YAxis dataKey="name" type="category" width={80} />
                <Tooltip formatter={(value) => `${value}%`} />
                <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                  {accuracyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="h-36">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={errorMetricsData} layout="vertical" margin={{ top: 5, right: 30, left: 60, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={true} horizontal={false} />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={80} />
                <Tooltip />
                <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                  {errorMetricsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* NEW: Error Distribution + Model Parameters */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* Error Distribution */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Prediction Error Distribution</h2>
          <p className="text-gray-500 text-sm mb-6">Distribution of errors (Predicted − Actual). A tight bell around zero means high accuracy.</p>
          <div className="h-72">
            {errorDistribution.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={errorDistribution} margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="Error" label={{ value: 'Error Value', position: 'bottom', offset: -5 }} />
                  <YAxis label={{ value: 'Count', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Area type="monotone" dataKey="Count" stroke="#8b5cf6" fill="#c4b5fd" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400">Run a prediction first to see this graph.</div>
            )}
          </div>
        </div>

        {/* Classification Metrics & Confusion Matrix */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm flex flex-col">
          <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">Classification Metrics</h2>
          <p className="text-gray-500 text-sm mb-6 text-center">Performance when thresholding Suitability Score &gt;= 75 as "Recommended".</p>
          
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-green-50 rounded-xl p-4 text-center border border-green-100">
              <div className="text-green-600 text-sm font-bold">F1 Score</div>
              <div className="text-2xl font-black text-gray-900">{f1Score}%</div>
            </div>
            <div className="bg-blue-50 rounded-xl p-4 text-center border border-blue-100">
              <div className="text-blue-600 text-sm font-bold">Recall</div>
              <div className="text-2xl font-black text-gray-900">{recall}%</div>
            </div>
            <div className="bg-purple-50 rounded-xl p-4 text-center border border-purple-100">
              <div className="text-purple-600 text-sm font-bold">Precision</div>
              <div className="text-2xl font-black text-gray-900">{precision}%</div>
            </div>
          </div>
          
          <h3 className="font-bold text-gray-700 mb-2 text-center">Confusion Matrix</h3>
          <div className="flex-1 grid grid-cols-2 gap-3 text-center text-sm">
            <div className="bg-gray-100 rounded-lg p-4 flex flex-col items-center justify-center border border-gray-200">
              <span className="text-gray-500 font-bold mb-1">True Negative</span>
              <span className="text-2xl font-black text-gray-800">{tn}</span>
            </div>
            <div className="bg-red-50 rounded-lg p-4 flex flex-col items-center justify-center border border-red-100">
              <span className="text-red-500 font-bold mb-1">False Positive</span>
              <span className="text-2xl font-black text-gray-800">{fp}</span>
            </div>
            <div className="bg-yellow-50 rounded-lg p-4 flex flex-col items-center justify-center border border-yellow-100">
              <span className="text-yellow-600 font-bold mb-1">False Negative</span>
              <span className="text-2xl font-black text-gray-800">{fn}</span>
            </div>
            <div className="bg-green-100 rounded-lg p-4 flex flex-col items-center justify-center border border-green-200">
              <span className="text-green-600 font-bold mb-1">True Positive</span>
              <span className="text-2xl font-black text-gray-800">{tp}</span>
            </div>
          </div>
        </div>
      </div>

        {/* Model Hyperparameters Table */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2"><Settings className="w-6 h-6 text-gray-600" /> Model Hyperparameters</h2>
          <p className="text-gray-500 text-sm mb-6">The configuration used to train the Random Forest model.</p>
          <div className="overflow-hidden rounded-xl border border-gray-200">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50 text-gray-500 text-sm uppercase tracking-wider">
                  <th className="p-4 font-medium">Parameter</th>
                  <th className="p-4 font-medium">Value</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {Object.entries(modelParams).map(([key, value], idx) => (
                  <tr key={idx} className="hover:bg-gray-50 transition-colors">
                    <td className="p-4 font-medium text-gray-800">{key.replace(/_/g, ' ')}</td>
                    <td className="p-4 text-gray-600 font-mono">{String(value)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      {/* Pipeline + Feature Importance + Category Pies */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* ML Pipeline Explanation */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Model Pipeline</h2>
          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center font-bold flex-shrink-0">1</div>
              <div>
                <h4 className="font-bold text-gray-900">Dynamic Label Generation</h4>
                <p className="text-sm text-gray-600 mt-1">Computes a target Suitability Score for each meal using heuristic penalties (cost &gt; budget, nutrition mismatch, BMI & fitness goals).</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center font-bold flex-shrink-0">2</div>
              <div>
                <h4 className="font-bold text-gray-900">Feature Engineering</h4>
                <p className="text-sm text-gray-600 mt-1">One-Hot Encoding applied to categorical variables like Cuisine and Meal Type.</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-bold flex-shrink-0">3</div>
              <div>
                <h4 className="font-bold text-gray-900">Random Forest Training</h4>
                <p className="text-sm text-gray-600 mt-1">An ensemble of 100 decision trees is trained to map macro/micro nutrients and cost to the Suitability Score.</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center font-bold flex-shrink-0">4</div>
              <div>
                <h4 className="font-bold text-gray-900">Prediction & Ranking</h4>
                <p className="text-sm text-gray-600 mt-1">The model predicts scores for the test set, ranks meals, and selects the optimal combination for daily and weekly plans.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Feature Importance Chart */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Feature Importance</h2>
          <p className="text-gray-500 text-sm mb-6">What factors influenced the AI's decision the most?</p>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 50, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                <XAxis type="number" unit="%" />
                <YAxis dataKey="name" type="category" width={80} tick={{fontSize: 12}} />
                <Tooltip formatter={(value) => `${value}%`} />
                <Bar dataKey="Importance" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Categorized Pie Charts */}
        <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm md:col-span-2">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Feature Weight by Category</h2>
          <p className="text-gray-500 text-sm mb-6">Explore the model's decision-making weights broken down by different metric categories.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Nutrition Features Pie */}
            <div className="h-64 flex flex-col items-center">
              <h3 className="font-bold text-gray-700 mb-2">Nutritional</h3>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData.filter(f => ['Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber'].includes(f.name))} dataKey="Importance" nameKey="name" cx="50%" cy="50%" outerRadius={70} label>
                    {chartData.filter(f => ['Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber'].includes(f.name)).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'][index % 5]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Logistics Pie */}
            <div className="h-64 flex flex-col items-center">
              <h3 className="font-bold text-gray-700 mb-2">Cost & Rating</h3>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData.filter(f => ['Cost', 'Prep_Time', 'Base_Rating'].includes(f.name))} dataKey="Importance" nameKey="name" cx="50%" cy="50%" outerRadius={70} label>
                    {chartData.filter(f => ['Cost', 'Prep_Time', 'Base_Rating'].includes(f.name)).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#ec4899', '#14b8a6', '#6366f1'][index % 3]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Preferences Pie */}
            <div className="h-64 flex flex-col items-center">
              <h3 className="font-bold text-gray-700 mb-2">Preferences</h3>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData.filter(f => !['Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 'Cost', 'Prep_Time', 'Base_Rating'].includes(f.name))} dataKey="Importance" nameKey="name" cx="50%" cy="50%" outerRadius={70} label>
                    {chartData.filter(f => !['Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 'Cost', 'Prep_Time', 'Base_Rating'].includes(f.name)).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#8b5cf6', '#f59e0b', '#10b981'][index % 3]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
          </div>
        </div>
      </div>

    </div>
  );
}
