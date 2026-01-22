export const TaskHeader = ({ title, phrase, count }: { title: string; phrase: string; count: number }) => (
  <header className="relative mb-10 overflow-hidden rounded-3xl border border-white bg-white/60 p-8 shadow-sm backdrop-blur-md">
    {/* Decorative background element */}
    <div className="absolute -right-10 -top-10 h-32 w-32 rounded-full bg-blue-500/5 blur-3xl" />
    
    <div className="relative flex items-center justify-between">
      <div className="space-y-1">
        <h1 className="text-4xl font-black tracking-tight text-cyan-400">
          {title}
        </h1>
        <div className="flex items-center gap-2">
          <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse" />
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-400">
            {phrase}
          </p>
        </div>
      </div>

      <div className="flex flex-col items-end">
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-black text-cyan-400 tabular-nums">
            {count}
          </span>
          <span className="text-sm font-bold text-slate-300">Tasks</span>
        </div>
        <div className="mt-1 h-1 w-12 rounded-full bg-slate-100 overflow-hidden">
          <div 
            className="h-full bg-cyan-400 transition-all duration-500" 
            style={{ width: `${Math.min(count * 10, 100)}%` }} 
          />
        </div>
      </div>
    </div>
  </header>
);