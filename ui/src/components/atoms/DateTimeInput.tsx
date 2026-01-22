interface DateTimeInputProps {
  value: string;
  onChange: (val: string) => void;
}

export const DateTimeInput = ({ value, onChange }: DateTimeInputProps) => (
  <div className="flex flex-col gap-1.5 w-full md:w-auto">
    <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1 block">
      Due Date (Optional)
    </label>
    <input
      type="datetime-local"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="h-[46px] px-3 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none bg-slate-50 text-slate-600 text-sm transition-all"
    />
  </div>
);