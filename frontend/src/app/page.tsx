"use client";

import { useState } from "react";

export default function ArceusDashboard() {
  const [status, setStatus] = useState<"pending" | "submitting" | "success" | "error">("pending");
  const [data, setData] = useState([
    { id: 1, name: "John Doe", email: "john.doe@example.com", status: "Active" },
    { id: 2, name: "Jane Smith", email: "jane.smith@example.com", status: "Active" },
    { id: 3, name: "Alice Johnson", email: "alice.j@example.com", status: "Inactive" }
  ]);
  const [errorMessage, setErrorMessage] = useState("");

  const handleApprove = async () => {
    setStatus("submitting");
    setErrorMessage("");
    
    try {
      const response = await fetch("/api/approve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tableName: "users",
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

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans selection:bg-cyan-500/30">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10 flex items-center justify-between border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-500 bg-clip-text text-transparent mb-2 drop-shadow-sm">Arceus</h1>
            <p className="text-slate-400 text-sm tracking-wide">Data Injection Dashboard</p>
          </div>
          <button 
            onClick={handleApprove}
            disabled={status === "submitting" || status === "success" || data.length === 0}
            className={`px-6 py-3 rounded-lg font-semibold uppercase tracking-wider text-sm transition-all border shadow-sm ${
              status === "submitting" || data.length === 0 || status === "success"
                ? "bg-emerald-600/20 text-emerald-500/50 cursor-not-allowed border-emerald-500/10"
                : "bg-emerald-600 hover:bg-emerald-500 text-white cursor-pointer border-emerald-400/50 shadow-[0_0_15px_rgba(16,185,129,0.3)]"
            }`}
          >
            {status === "submitting" ? "Injecting..." : status === "success" ? "Approved" : "Approve Injection"}
          </button>
        </header>

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
              <p className="font-semibold">Injection Failed</p>
              <p className="text-sm opacity-90">{errorMessage}</p>
            </div>
          </div>
        )}

        <section className="bg-slate-900/60 rounded-2xl border border-slate-800 p-8 backdrop-blur-md shadow-2xl">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-semibold text-slate-200 flex items-center">
              <span className={`w-2.5 h-2.5 rounded-full mr-3 shadow-[0_0_8px_rgba(245,158,11,0.6)] ${status === 'success' ? 'bg-slate-600 animate-none' : 'bg-amber-500 animate-pulse'}`}></span>
              Pending Mock Data Preview
            </h2>
            <span className="text-xs font-medium px-3 py-1 bg-slate-800 text-slate-400 rounded-full border border-slate-700">target: public.users</span>
          </div>
          
          <div className="overflow-x-auto rounded-xl border border-slate-800/80 shadow-inner">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-slate-800/50 text-slate-400 border-b border-slate-700/50">
                <tr>
                  <th className="px-6 py-5 font-semibold tracking-wide text-xs uppercase">ID</th>
                  <th className="px-6 py-5 font-semibold tracking-wide text-xs uppercase">Name</th>
                  <th className="px-6 py-5 font-semibold tracking-wide text-xs uppercase">Email</th>
                  <th className="px-6 py-5 font-semibold tracking-wide text-xs uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80">
                {data.length > 0 ? data.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-800/40 transition-colors text-slate-300">
                    <td className="px-6 py-4 font-mono text-slate-500 text-xs">{row.id}</td>
                    <td className="px-6 py-4">{row.name}</td>
                    <td className="px-6 py-4">{row.email}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2.5 py-1 rounded-md text-xs font-medium border ${row.status === 'Active' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-slate-500/10 text-slate-400 border-slate-500/20'}`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                      {status === "success" ? "Data has been successfully injected." : "No pending data."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          
          <div className="mt-6 flex justify-between items-center text-sm text-slate-500 bg-slate-950/50 p-4 rounded-xl border border-slate-800/50">
            <p className="flex items-center"><svg className="w-4 h-4 mr-2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> Showing {data.length} placeholder records from generated script.</p>
            <p className={`font-medium ${status === 'success' ? 'text-emerald-500/70' : 'text-amber-500/70'}`}>
              {status === 'success' ? "Injection approved and executed." : "Awaiting human approval before injection..."}
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
