import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-xl p-6">
        <h1 className="text-2xl font-semibold">Joern's Forecasting Model</h1>
        <p className="mt-2 text-slate-600">
          Frontend scaffold (React + Vite + TypeScript).
        </p>
        <button
          className="mt-4 rounded bg-blue-600 px-3 py-2 text-white hover:bg-blue-700"
          onClick={() => setCount((c) => c + 1)}
        >
          Clicked {count} times
        </button>
      </div>
    </div>
  );
}

