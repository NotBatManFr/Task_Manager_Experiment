'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTasks } from '@/hooks/useTasks';
import { TaskHeader } from '@/components/molecules/TaskHeader';
import { KanbanBoard } from '@/components/organisms/KanbanBoard';
import { Input } from '@/components/atoms/Input';
import { Button } from '@/components/atoms/Button';
// import { StatusPicker } from '@/components/molecules/StatusPicker';
import { TaskStatus } from '@/components/atoms/StatusBadge';
import { DateTimeInput } from '@/components/atoms/DateTimeInput';

export default function Page() {
  const { tasks, loading, addTask, deleteTask, updateTaskStatus, moveTask } = useTasks();
  const [newTitle, setNewTitle] = useState('');
  const [newStatus, setNewStatus] = useState<TaskStatus>('todo');
  const [dueDate, setDueDate] = useState('');

  const handleAdd = () => {
    if (!newTitle.trim()) return;
    addTask(newTitle, newStatus, dueDate);
    setNewTitle('');
    setNewStatus('todo');
    setDueDate('');
  };

  return (
    <main className="min-h-screen bg-[#F8FAFC] py-12 px-6">
      <div className="max-w-6xl mx-auto">
        <TaskHeader title="TASK BOARD" phrase="What are your plans for today? 🤦‍♀️" count={tasks.length} />
        
        {/* Animated Creation Bar */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row gap-4 mb-12 bg-white p-5 rounded-2xl shadow-sm border border-slate-200 items-end">
          
          <div className="flex-grow w-full">

            <Input 
              value={newTitle} 
              onChange={setNewTitle} 
              placeholder='Write your task here and press "Create"' 
              onEnter={handleAdd}
            />

          </div>

          <DateTimeInput value={dueDate} onChange={setDueDate} />

          <Button onClick={handleAdd} className="h-[46px] px-8 shadow-blue-100 shadow-lg">
            Create
          </Button>
        </motion.div>

        {loading ? (
          <div className="flex flex-col items-center justify-center p-20 space-y-4">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-slate-400 font-medium">Synchronizing workspace...</p>
          </div>
        ) : (
          <AnimatePresence mode="popLayout">
            <KanbanBoard 
              tasks={tasks} 
              actions={{ 
                delete: deleteTask, 
                updateStatus: updateTaskStatus,
                move: moveTask
              }} 
            />
          </AnimatePresence>
        )}
      </div>
    </main>
  );
}