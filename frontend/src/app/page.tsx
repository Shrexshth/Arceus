export default function ArceusDashboard() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans selection:bg-cyan-500/30">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10 flex items-center justify-between border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-500 bg-clip-text text-transparent mb-2 drop-shadow-sm">Arceus</h1>
            <p className="text-slate-400 text-sm tracking-wide">Data Injection Dashboard</p>
          </div>
          <button 
            disabled
            className="px-6 py-3 rounded-lg bg-emerald-600/20 text-emerald-500/50 cursor-not-allowed border border-emerald-500/10 shadow-[0_0_15px_rgba(16,185,129,0.05)] font-semibold uppercase tracking-wider text-sm transition-all"
          >
            Approve Injection
          </button>
        </header>

        <section className="bg-slate-900/60 rounded-2xl border border-slate-800 p-8 backdrop-blur-md shadow-2xl">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-semibold text-slate-200 flex items-center">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500 mr-3 animate-pulse shadow-[0_0_8px_rgba(245,158,11,0.6)]"></span>
              Pending Mock Data Preview
            </h2>
            <span className="text-xs font-medium px-3 py-1 bg-slate-800 text-slate-400 rounded-full border border-slate-700">target: arceus_db</span>
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
                <tr className="hover:bg-slate-800/40 transition-colors text-slate-300">
                  <td className="px-6 py-4 font-mono text-slate-500 text-xs">1</td>
                  <td className="px-6 py-4">John Doe</td>
                  <td className="px-6 py-4">john.doe@example.com</td>
                  <td className="px-6 py-4"><span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-md text-xs font-medium border border-emerald-500/20">Active</span></td>
                </tr>
                <tr className="hover:bg-slate-800/40 transition-colors text-slate-300">
                  <td className="px-6 py-4 font-mono text-slate-500 text-xs">2</td>
                  <td className="px-6 py-4">Jane Smith</td>
                  <td className="px-6 py-4">jane.smith@example.com</td>
                  <td className="px-6 py-4"><span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-md text-xs font-medium border border-emerald-500/20">Active</span></td>
                </tr>
                <tr className="hover:bg-slate-800/40 transition-colors text-slate-300">
                  <td className="px-6 py-4 font-mono text-slate-500 text-xs">3</td>
                  <td className="px-6 py-4">Alice Johnson</td>
                  <td className="px-6 py-4">alice.j@example.com</td>
                  <td className="px-6 py-4"><span className="px-2.5 py-1 bg-slate-500/10 text-slate-400 rounded-md text-xs font-medium border border-slate-500/20">Inactive</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div className="mt-6 flex justify-between items-center text-sm text-slate-500 bg-slate-950/50 p-4 rounded-xl border border-slate-800/50">
            <p className="flex items-center"><svg className="w-4 h-4 mr-2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg> Showing 3 placeholder records from generated script.</p>
            <p className="font-medium text-amber-500/70">Awaiting human approval before injection...</p>
          </div>
        </section>
      </div>
    </div>
  );
}
