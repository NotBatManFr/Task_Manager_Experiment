import { useState, useEffect } from 'react';
import { localStorageService } from '@/services/localStorageService';
import { apiService } from '@/services/apiService';
import { TaskStatus } from '@/components/atoms/StatusBadge';
import { Task, TaskCreate } from '@/types/task';
// import { TaskItem } from '@/components/molecules/TaskItem';
// import { DateTimeInput } from '@/components/atoms/DateTimeInput';

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Future toggle: this will be driven by the Auth Service
  const isLoggedIn = true; 

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
    const newTaskTemplate: TaskCreate = { title, status, dueDate: dueDate || null };
    const savedTask = await activeService.saveTask(newTaskTemplate);
    setTasks(prev => [...prev, savedTask]);
  };

  //  | number
  const deleteTask = async (id: string | number) => {
    await activeService.deleteTask(id);
    setTasks(prev => prev.filter(t => t.id !== String(id)));
  };

  const updateTaskStatus = async (id: string | number, status: TaskStatus) => {
    const taskToUpdate = tasks.find(t => t.id === String(id));
    if (!taskToUpdate) return;

    const updatedTask: Task = {
      ...taskToUpdate,
      status,
    };

    try {
      // Optimistic Update: change UI immediately
      setTasks(prev => prev.map(t => t.id === String(id) ? { ...t, status } : t));
      
      // Persist change
      await activeService.updateTask(id, updatedTask);
    } catch (err) {
      console.error("Failed to update status", err);
      // Fallback: reload data if persistence fails
      loadData();
    }
  };

  const STATUS_ORDER: TaskStatus[] = ['todo', 'in_progress', 'done'];

  const moveTask = async (id: string | number, direction: 'forward' | 'backward') => {
    const task = tasks.find(t => t.id === String(id));
    if (!task) return;

    const currentIndex = STATUS_ORDER.indexOf(task.status);
    const nextIndex = direction === 'forward' ? currentIndex + 1 : currentIndex - 1;

    if (nextIndex < 0 || nextIndex >= STATUS_ORDER.length) return;

    await updateTaskStatus(id, STATUS_ORDER[nextIndex]);
  };

  useEffect(() => {
    loadData();
  }, [isLoggedIn]);

  return { tasks, loading, addTask, deleteTask, updateTaskStatus, moveTask };
}