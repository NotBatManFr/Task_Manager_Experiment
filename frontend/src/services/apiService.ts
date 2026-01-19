const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiService = {
  getTasks: async () => {
    const res = await fetch(`${API_URL}/tasks`);
    return res.json();
  },
  saveTask: async (task: any) => {
    const res = await fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(task),
    });
    return res.json();
  },
  updateTask: async (id: string | number, updates: any) => {
    const res = await fetch(`${API_URL}/tasks/${id}`, {
      method: 'PUT', // or PATCH depending on your FastAPI route
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    return res.json();
  },
  // ... deleteTask, updateStatus
};