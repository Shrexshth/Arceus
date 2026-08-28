"use client";

import { useState } from "react";

export default function ArceusDashboard() {
  const [status, setStatus] = useState<"pending" | "generating" | "generated" | "submitting" | "success" | "error">("pending");
  const [tableName, setTableName] = useState("users");
  const [generatedTableName, setGeneratedTableName] = useState("");
  const [rowCount, setRowCount] = useState(5);
  const [data, setData] = useState<any[]>([]);
  const [errorMessage, setErrorMessage] = useState("");

  const handleGenerate = async () => {
    setStatus("generating");
    setErrorMessage("");
    setData([]);
    setGeneratedTableName("");

    if (!Number.isInteger(rowCount) || rowCount < 1 || rowCount > 100) {
      setStatus("error");
      setErrorMessage("Row count must be between 1 and 100");
      return;
    }

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tableName, rowCount })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to generate data");
      }
      
      const responseData = await response.json();
      if (!responseData.data || !Array.isArray(responseData.data)) {
         throw new Error("Invalid format returned from agent");
      }
      
      setData(responseData.data);
      setGeneratedTableName(tableName);
      setStatus("generated");
    } catch (error: any) {
      setStatus("error");
      setErrorMessage(error.message || "An unknown error occurred");
    }
  };

  const handleApprove = async () => {
    setStatus("submitting");
    setErrorMessage("");
    
    try {
      const response = await fetch("/api/approve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tableName: generatedTableName,
          data: data
        })
      });
      
      if (!response.ok) {
        throw new Error("Failed to inject data");
      }
      
      setStatus("success");
      setData([]);
    } catch (error: any) {
      setStatus("error");
      setErrorMessage(error.message || "An unknown error occurred");
    }
  };

  const handleClear = () => {
    setStatus("pending");
    setData([]);
    setGeneratedTableName("");
    setErrorMessage("");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans selection:bg-cyan-500/30">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10 flex items-center justify-between border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-500 bg-clip-text text-transparent mb-2 drop-shadow-sm">Arceus</h1>
            <p className="text-slate-400 text-sm tracking-wide">Data Injection Dashboard</p>
          </div>
          <div className="flex space-x-3">
            {(status === "generated" || status === "submitting" || status === "error") && (
              <button 
                onClick={handleClear}
                disabled={status === "submitting"}
                className="px-6 py-3 rounded-lg font-semibold uppercase tracking-wider text-sm transition-all border shadow-sm bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700"
              >
                Cancel / Clear
              </button>
            )}
            <button 
              onClick={handleApprove}
              disabled={status !== "generated" || data.length === 0}
              className={`px-6 py-3 rounded-lg font-semibold uppercase tracking-wider text-sm transition-all border shadow-sm ${
                status !== "generated" || data.length === 0
                  ? "bg-emerald-600/20 text-emerald-500/50 cursor-not-allowed border-emerald-500/10"
                  : "bg-emerald-600 hover:bg-emerald-500 text-white cursor-pointer border-emerald-400/50 shadow-[0_0_15px_rgba(16,185,129,0.3)]"
              }`}
            >
              {status === "submitting" ? "Injecting..." : status === "success" ? "Approved" : "Approve Injection"}
            </button>
          </div>
        </header>

        <section className="bg-slate-900/40 rounded-2xl border border-slate-800 p-6 mb-8 flex items-end space-x-6">
          <div className="flex-1">
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Table Name</label>
            <input 
              type="text" 
              value={tableName}
              onChange={(e) => setTableName(e.target.value)}
              disabled={status === "generating" || status === "submitting"}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-slate-200 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all disabled:opacity-50"
              placeholder="e.g. users"
            />
          </div>
          <div className="flex-1">
            <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Row Count</label>
            <input 
              type="number" 
              value={rowCount}
              onChange={(e) => {
                const val = parseInt(e.target.value);
                setRowCount(isNaN(val) ? "" as any : val);
              }}
              disabled={status === "generating" || status === "submitting"}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-slate-200 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all disabled:opacity-50"
              min={1} max={100}
            />
          </div>
          <div>
            <button 
              onClick={handleGenerate}
              disabled={status === "generating" || status === "submitting" || !tableName || Number(rowCount) < 1 || Number(rowCount) > 100}
              className={`px-6 py-3 rounded-lg font-semibold uppercase tracking-wider text-sm transition-all border shadow-sm ${
                status === "generating" || status === "submitting" || !tableName || Number(rowCount) < 1 || Number(rowCount) > 100
                  ? "bg-cyan-600/20 text-cyan-500/50 cursor-not-allowed border-cyan-500/10"
                  : "bg-cyan-600 hover:bg-cyan-500 text-white cursor-pointer border-cyan-400/50 shadow-[0_0_15px_rgba(6,182,212,0.3)]"
              }`}
            >
              {status === "generating" ? "Generating..." : "Generate Data"}
            </button>
          </div>
        </section>

        {status === "success" && (
          <div className="mb-8 p-4 bg-emerald-900/30 border border-emerald-500/50 rounded-xl flex items-center text-emerald-300">
            <svg className="w-6 h-6 mr-3 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="font-semibold">Injection Successful!</p>
              <p className="text-sm opacity-90">The mock data has been sent to TrueForge and injected into the database via MCP.</p>
            </div>
          </div>
        )}

        {status === "error" && (
          <div className="mb-8 p-4 bg-red-900/30 border border-red-500/50 rounded-xl flex items-center text-red-300">
            <svg className="w-6 h-6 mr-3 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <p className="font-semibold">Error Encountered</p>
              <p className="text-sm opacity-90">{errorMessage}</p>
            </div>
          </div>
        )}

        <section className="bg-slate-900/60 rounded-2xl border border-slate-800 p-8 backdrop-blur-md shadow-2xl">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-semibold text-slate-200 flex items-center">
              <span className={`w-2.5 h-2.5 rounded-full mr-3 shadow-[0_0_8px_rgba(245,158,11,0.6)] ${status === 'generated' ? 'bg-amber-500 animate-pulse' : 'bg-slate-600 animate-none'}`}></span>
              Pending Mock Data Preview
            </h2>
            <span className="text-xs font-medium px-3 py-1 bg-slate-800 text-slate-400 rounded-full border border-slate-700">target: public.{tableName}</span>
          </div>
          
          <div className="overflow-x-auto rounded-xl border border-slate-800/80 shadow-inner">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-slate-800/50 text-slate-400 border-b border-slate-700/50">
                <tr>
                  {data.length > 0 && Object.keys(data[0]).map(key => (
                    <th key={key} className="px-6 py-5 font-semibold tracking-wide text-xs uppercase">{key}</th>
                  ))}
                  {data.length === 0 && <th className="px-6 py-5 font-semibold tracking-wide text-xs uppercase">Columns</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80">
                {data.length > 0 ? data.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors text-slate-300">
                    {Object.values(row).map((val: any, colIdx) => (
                      <td key={colIdx} className="px-6 py-4 font-mono text-slate-500 text-xs">
                        {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                      </td>
                    ))}
                  </tr>
                )) : (
                  <tr>
                    <td className="px-6 py-8 text-center text-slate-500">
                      {status === "generating" ? "Waiting for TrueForge agent..." : status === "success" ? "Data has been successfully injected." : "No pending data. Generate data to preview."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          
          <div className="mt-6 flex justify-between items-center text-sm text-slate-500 bg-slate-950/50 p-4 rounded-xl border border-slate-800/50">
            <p className="flex items-center"><svg className="w-4 h-4 mr-2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> Showing {data.length} records.</p>
            <p className={`font-medium ${status === 'success' ? 'text-emerald-500/70' : status === 'generated' ? 'text-amber-500/70' : 'text-slate-500'}`}>
              {status === 'success' ? "Injection approved and executed." : status === "generated" ? "Awaiting human approval before injection..." : "Ready."}
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
