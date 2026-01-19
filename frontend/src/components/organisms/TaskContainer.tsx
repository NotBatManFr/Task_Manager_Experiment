import { TaskItem } from '../molecules/TaskItem';
import { TaskStatus } from '../atoms/StatusBadge';

interface TaskContainerProps {
  tasks: any[];
  actions: {
    delete: (id: string | number) => void;
    updateStatus: (id: string | number, status: TaskStatus) => void;
  };
}

export const TaskContainer = ({ tasks, actions }: TaskContainerProps) => (
  <section className="space-y-4">
    {tasks.map((task) => (
      <TaskItem 
        key={task.id} 
        task={task} 
        onDelete={() => actions.delete(task.id)}
        onStatusUpdate={(newStatus) => actions.updateStatus(task.id, newStatus)}
      />
    ))}
  </section>
);