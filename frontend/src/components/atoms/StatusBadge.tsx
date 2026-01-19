export type TaskStatus = 'todo' | 'in_progress' | 'done';

export const StatusBadge = ({ status }: { status: TaskStatus }) => {
  const config = {
    todo: { label: 'To Do', color: 'bg-slate-100 text-slate-700' },
    in_progress: { label: 'In Progress', color: 'bg-amber-100 text-amber-700' },
    done: { label: 'Done', color: 'bg-emerald-100 text-emerald-700' }
  };

  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${config[status].color}`}>
      {config[status].label}
    </span>
  );
};