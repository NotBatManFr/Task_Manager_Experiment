import { Task, TaskCreate } from '@/types/task';

const STORAGE_KEY = 'taskflow_guest_tasks';

export const localStorageService = {
  getTasks: (): Task[] => {
    if (typeof window === 'undefined') return [];
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) as Task[] : [];
  },
  saveTask: (task: TaskCreate): Task => {
    const tasks = localStorageService.getTasks();

    const newTask: Task = {
      ...task,
      id: Date.now().toString(),
      status: task.status ?? 'todo',
      dueDate: task.dueDate ?? null,
    };

    const updated = [...tasks, newTask];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return newTask;
  },
  deleteTask: (id: string | number): void => {
    const tasks = localStorageService.getTasks();
    const filtered = tasks.filter((t) => t.id !== String(id));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
  },
  updateTask: (id: string | number, updates: TaskCreate): Task | undefined => {
    const tasks = localStorageService.getTasks();
    const updatedTasks = tasks.map((t) => 
      t.id === String(id) ? { ...t, ...updates } : t
    );
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedTasks));
    return updatedTasks.find((t) => t.id === String(id));
  }
};