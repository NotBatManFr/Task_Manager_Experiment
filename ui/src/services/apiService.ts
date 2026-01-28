import { Task, TaskCreate } from '@/types/task';

const API_URL = '/api/tasks';

export const apiService = {
  getTasks: async (): Promise<Task[]> => {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error('Failed to fetch tasks');
    return res.json();
  },
  
  saveTask: async (task: TaskCreate): Promise<Task> => {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task),
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to create task');
    }
    return res.json();
  },
  
  updateTask: async (id: string, task: TaskCreate): Promise<Task> => {
    const res = await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task),
    });
    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.error || 'Failed to update task');
    }
    return res.json();
  },
  
  deleteTask: async (id: string): Promise<void> => {
    const res = await fetch(`${API_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete task');
  },
};