'use client';

import { useState } from 'react';
import { useTasks } from '@/hooks/useTasks';
import { TaskHeader } from '@/components/molecules/TaskHeader';
import { TaskContainer } from '@/components/organisms/TaskContainer';
import { Input } from '@/components/atoms/Input';
import { Button } from '@/components/atoms/Button';
import { StatusPicker } from '@/components/molecules/StatusPicker'; // Import the picker
import { TaskStatus } from '@/components/atoms/StatusBadge';

export default function Page() {
  const { tasks, loading, addTask, deleteTask, updateTaskStatus } = useTasks();
  
  // Local state for the "New Task" form
  const [newTitle, setNewTitle] = useState('');
  const [newStatus, setNewStatus] = useState<TaskStatus>('todo');

  const handleAdd = () => {
    if (!newTitle.trim()) return;
    
    // We update our addTask call to accept the chosen status
    addTask(newTitle, newStatus); 
    
    // Reset form
    setNewTitle('');
    setNewStatus('todo');
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <TaskHeader title="Workspace" count={tasks.length} />
        
        {/* The New "Creation Bar" Molecule */}
        <div className="flex flex-col md:flex-row gap-3 mb-8 bg-white p-4 rounded-xl shadow-sm border border-gray-100 items-end">
          <div className="flex-grow w-full">
            <label className="text-[10px] font-bold uppercase tracking-wider text-gray-400 ml-1 mb-1 block">
              Task Title
            </label>
            <Input 
              value={newTitle} 
              onChange={setNewTitle} 
              placeholder="What's your next goal?" 
              onEnter={handleAdd}
            />
          </div>
          
          <div className="w-full md:w-auto">
            <StatusPicker 
              currentStatus={newStatus} 
              onStatusChange={setNewStatus} 
            />
          </div>

          <Button onClick={handleAdd} className="h-[42px] w-full md:w-auto shadow-md">
            Add Task
          </Button>
        </div>

        {loading ? (
          <div className="flex justify-center p-10 text-gray-400 animate-pulse">
            Loading your space...
          </div>
        ) : (
          <TaskContainer 
            tasks={tasks} 
            actions={{ 
              delete: deleteTask, 
              updateStatus: updateTaskStatus 
            }} 
          />
        )}
      </div>
    </main>
  );
}