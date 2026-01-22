const STORAGE_KEY = 'taskflow_guest_tasks';

export const localStorageService = {
  getTasks: () => {
    if (typeof window === 'undefined') return [];
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  },
  saveTask: (task: any) => {
    const tasks = localStorageService.getTasks();
    const updated = [...tasks, { ...task, id: Date.now() }];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    return updated[updated.length - 1];
  },
  deleteTask: (id: string | number) => {
    const tasks = localStorageService.getTasks();
    const filtered = tasks.filter((t: any) => t.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
  },
  updateTask: (id: string | number, updates: any) => {
    const tasks = localStorageService.getTasks();
    const updatedTasks = tasks.map((t: any) => 
      t.id === id ? { ...t, ...updates } : t
    );
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedTasks));
    return updatedTasks.find((t: any) => t.id === id);
  }
};