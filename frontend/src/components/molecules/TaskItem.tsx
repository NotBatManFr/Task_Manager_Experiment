import { StatusBadge, TaskStatus } from '../atoms/StatusBadge';
import { StatusPicker } from './StatusPicker';
import { Button } from '../atoms/Button';

interface TaskItemProps {
  task: {
    id: string | number;
    title: string;
    status: TaskStatus;
  };
  onDelete: () => void;
  onStatusUpdate: (newStatus: TaskStatus) => void;
}

export const TaskItem = ({ task, onDelete, onStatusUpdate }: TaskItemProps) => (
  <div className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-all group">
    <div className="flex flex-col gap-2 flex-grow">
      <div className="flex items-center gap-3">
        <StatusBadge status={task.status} />
        <h3 className="text-gray-800 font-semibold text-lg">{task.title}</h3>
      </div>
    </div>

    <div className="flex items-center gap-4">
      <StatusPicker 
        currentStatus={task.status} 
        onStatusChange={onStatusUpdate} 
      />
      <Button 
        variant="danger" 
        onClick={onDelete}
        className="opacity-0 group-hover:opacity-100 transition-opacity"
      >
        Delete
      </Button>
    </div>
  </div>
);