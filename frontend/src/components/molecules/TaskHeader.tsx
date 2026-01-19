export const TaskHeader = ({ title, count }: { title: string, count: number }) => (
  <header className="mb-8 flex justify-between items-end">
    <div>
      <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
      <p className="text-gray-500 text-sm mt-1">Organize your workflow effectively</p>
    </div>
    <div className="text-right">
      <span className="text-2xl font-mono font-bold text-blue-600">{count}</span>
      <p className="text-[10px] uppercase tracking-widest text-gray-400 font-bold">Total Tasks</p>
    </div>
  </header>
);