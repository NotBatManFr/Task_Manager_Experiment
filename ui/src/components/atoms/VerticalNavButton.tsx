import { TaskStatus } from './StatusBadge';

interface VerticalNavButtonProps {
  onClick: () => void;
  direction: 'left' | 'right';
  targetStatus: TaskStatus; // New prop
  title?: string;
}

export const VerticalNavButton = ({ onClick, direction, targetStatus, title }: VerticalNavButtonProps) => {
  const isLeft = direction === 'left';
  
  // Define the hover colors for each status
  const hoverColors = {
    todo: 'hover:bg-slate-500',
    in_progress: 'hover:bg-amber-500',
    done: 'hover:bg-emerald-500',
  };

  return (
    <button 
      onClick={onClick}
      title={title}
      className={`
        w-[10%] min-w-[30px] flex items-center justify-center 
        bg-slate-50 text-slate-400 transition-all duration-300
        hover:text-white ${hoverColors[targetStatus]}
        ${isLeft ? 'border-r' : 'border-l'} border-slate-100
      `}
    >
      <span className="font-bold text-xl transition-transform group-hover:scale-125">
        {isLeft ? '←' : '→'}
      </span>
    </button>
  );
};