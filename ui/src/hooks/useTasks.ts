import { useState, useEffect } from 'react';
import { localStorageService } from '@/services/localStorageService';
import { apiService } from '@/services/apiService';
import { TaskStatus } from '@/components/atoms/StatusBadge';
import { DateTimeInput } from '@/components/atoms/DateTimeInput';

export function useTasks() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Future toggle: this will be driven by your Auth Service
  const isLoggedIn = false; 

  const activeService = isLoggedIn ? apiService : localStorageService;

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await activeService.getTasks();
      setTasks(data);
    } catch (err) {
      console.error("Failed to load tasks", err);
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (title: string, status: TaskStatus = 'todo', dueDate?: string) => {
    const newTaskTemplate = { title, status, dueDate: dueDate || null };
    const savedTask = await activeService.saveTask(newTaskTemplate);
    setTasks(prev => [...prev, savedTask]);
  };

  const deleteTask = async (id: string | number) => {
    await activeService.deleteTask(id);
    setTasks(prev => prev.filter(t => t.id !== id));
  };

  const updateTaskStatus = async (id: string | number, newStatus: TaskStatus) => {
    try {
      // Optimistic Update: change UI immediately
      setTasks(prev => prev.map(t => t.id === id ? { ...t, status: newStatus } : t));
      
      // Persist change
      await activeService.updateTask(id, { status: newStatus });
    } catch (err) {
      console.error("Failed to update status", err);
      // Fallback: reload data if persistence fails
      loadData();
    }
  };

  const STATUS_ORDER: TaskStatus[] = ['todo', 'in_progress', 'done'];

  const moveTask = async (id: string | number, direction: 'forward' | 'backward') => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    const currentIndex = STATUS_ORDER.indexOf(task.status);
    const nextIndex = direction === 'forward' ? currentIndex + 1 : currentIndex - 1;

    if (nextIndex >= 0 && nextIndex < STATUS_ORDER.length) {
      await updateTaskStatus(id, STATUS_ORDER[nextIndex]);
    }
  };

  useEffect(() => {
    loadData();
  }, [isLoggedIn]);

  return { tasks, loading, addTask, deleteTask, updateTaskStatus, moveTask };
}