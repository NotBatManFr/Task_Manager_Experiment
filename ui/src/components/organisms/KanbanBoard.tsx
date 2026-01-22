import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TaskItem } from '../molecules/TaskItem';
import { TaskStatus } from '../atoms/StatusBadge';

interface KanbanBoardProps {
  tasks: any[];
  actions: {
    delete: (id: string | number) => void;
    updateStatus: (id: string | number, status: TaskStatus) => void;
    move: (id: string | number, direction: 'forward' | 'backward') => void;
  };
}

const COLUMNS: { id: TaskStatus; label: string; color: string }[] = [
  { id: 'todo', label: 'To Do', color: 'bg-slate-500' },
  { id: 'in_progress', label: 'In Progress', color: 'bg-amber-500' },
  { id: 'done', label: 'Done', color: 'bg-emerald-500' },
];

export const KanbanBoard = ({ tasks, actions }: KanbanBoardProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
      {COLUMNS.map((column) => {
        const columnTasks = tasks.filter((t) => t.status === column.id);

        return (
          <div key={column.id} className="flex flex-col w-full group">
            {/* Column Header */}
            <div className="flex items-center justify-between mb-5 px-2">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${column.color}`} />
                <h3 className="text-xs font-black uppercase tracking-[0.15em] text-slate-500">
                  {column.label}
                </h3>
              </div>
              <span className="bg-slate-200/50 text-slate-500 text-[10px] px-2 py-0.5 rounded-md font-bold tabular-nums">
                {columnTasks.length}
              </span>
            </div>

            {/* Column Body */}
            <div className="bg-slate-100/40 border border-slate-200/60 rounded-3xl p-4 min-h-[500px] transition-colors group-hover:bg-slate-100/60">
              <div className="flex flex-col gap-4">
                <AnimatePresence mode="popLayout">
                  {columnTasks.length === 0 ? (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-12 flex flex-col items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl">
                      <p className="text-[10px] font-bold uppercase tracking-widest text-slate-300">
                        Empty Shelf
                      </p>
                    </motion.div>
                  ) : (
                    columnTasks.map((task) => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        onMove={(dir: 'forward' | 'backward') =>
                          actions.move(task.id, dir)
                        }
                        onDelete={() => actions.delete(task.id)}
                      />
                    ))
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};