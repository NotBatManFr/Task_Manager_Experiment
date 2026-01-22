import { BaseSelect } from '../atoms/BaseSelect';
import { TaskStatus } from '../atoms/StatusBadge';

interface StatusPickerProps {
  currentStatus: TaskStatus;
  onStatusChange: (newStatus: TaskStatus) => void;
}

export const StatusPicker = ({ currentStatus, onStatusChange }: StatusPickerProps) => {
  const statusOptions = [
    { value: 'todo', label: 'To Do' },
    { value: 'in_progress', label: 'In Progress' },
    { value: 'done', label: 'Done' },
  ];

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-[10px] font-bold uppercase tracking-wider text-gray-400 ml-1">
        Status
      </label>
      <BaseSelect
        value={currentStatus}
        options={statusOptions}
        onChange={(val) => onStatusChange(val as TaskStatus)}
        className="min-w-[130px]"
      />
    </div>
  );
};