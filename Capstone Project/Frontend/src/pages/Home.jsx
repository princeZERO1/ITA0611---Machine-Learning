import React from 'react';
import { Link } from 'react-router-dom';
import { BrainCircuit, Salad, PiggyBank, ArrowRight, Activity, TrendingUp } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col gap-16 py-10">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto space-y-6">
        <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight leading-tight">
          AI-Driven Meal Recommendation System
        </h1>
        <p className="text-2xl font-light text-primary-dark">
          Personalized Nutrition + Smart Budget Planning Using Machine Learning
        </p>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          NutriBudget AI uses a Random Forest regression model to balance your dietary goals, taste preferences, and wallet limits, creating the perfect meal plan tailored just for you.
        </p>
        <div className="pt-8">
          <Link to="/input" className="inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-8 py-4 rounded-full font-bold text-lg transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            Start Recommendation <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* How It Works / Benefits Section */}
      <section className="grid md:grid-cols-3 gap-8 pt-8">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="w-14 h-14 bg-green-100 text-primary-dark rounded-xl flex items-center justify-center mb-6">
            <BrainCircuit className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-3">Machine Learning</h3>
          <p className="text-gray-600 leading-relaxed">
            Our Random Forest model analyzes 500+ meals and dynamically calculates suitability scores based on real-time budget and nutritional constraints.
          </p>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="w-14 h-14 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center mb-6">
            <Salad className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-3">Balanced Nutrition</h3>
          <p className="text-gray-600 leading-relaxed">
            Meets your specific targets for Calories, Protein, Carbs, Fat, and Fiber. We optimize your daily intake down to the gram.
          </p>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="w-14 h-14 bg-purple-100 text-purple-600 rounded-xl flex items-center justify-center mb-6">
            <PiggyBank className="w-8 h-8" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-3">Smart Budget</h3>
          <p className="text-gray-600 leading-relaxed">
            Eating healthy shouldn't break the bank. NutriBudget AI penalizes expensive outliers, ensuring your weekly budget stays green.
          </p>
        </div>
      </section>

      {/* Project Technology Section */}
      <section className="bg-white rounded-3xl p-10 border border-gray-200 shadow-sm mt-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Capstone Technology Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div className="p-4 bg-gray-50 rounded-xl">
            <p className="font-bold text-gray-800">Frontend</p>
            <p className="text-gray-500 text-sm mt-1">React, Tailwind CSS, Recharts</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-xl">
            <p className="font-bold text-gray-800">Backend</p>
            <p className="text-gray-500 text-sm mt-1">Python, FastAPI, Pandas</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-xl">
            <p className="font-bold text-gray-800">Machine Learning</p>
            <p className="text-gray-500 text-sm mt-1">Scikit-learn, Random Forest</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-xl">
            <p className="font-bold text-gray-800">Data</p>
            <p className="text-gray-500 text-sm mt-1">Synthetic 500+ Meal Dataset</p>
          </div>
        </div>
      </section>
    </div>
  );
}
