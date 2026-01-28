import { motion } from "framer-motion";
import { VerticalNavButton } from "../atoms/VerticalNavButton";
import { TaskStatus } from "../atoms/StatusBadge";

const STATUS_ORDER: TaskStatus[] = ["todo", "in_progress", "done"];

export const TaskItem = ({ task, onMove, onDelete }: any) => {
  const currentIndex = STATUS_ORDER.indexOf(task.status);

  // Calculate target statuses for the buttons
  const prevStatus = STATUS_ORDER[currentIndex - 1];
  const nextStatus = STATUS_ORDER[currentIndex + 1];

  return (
    <motion.div
      layout
      className="relative flex bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden group min-h-[110px]">
      {/* LEFT: Move Backward */}
      {prevStatus && (
        <VerticalNavButton
          direction="left"
          targetStatus={prevStatus}
          onClick={() => onMove("backward")}
          title={`Move to ${prevStatus}`}
        />
      )}

      {/* CENTER CONTENT */}
      <div className="flex-grow p-4 flex flex-col justify-between">
        <div className="flex justify-between items-start">
          <h4 className="font-bold text-slate-400 leading-tight pr-2">
            {task.title}
          </h4>
          
        </div>
          {task.dueDate && (
            <div className="flex items-center gap-1.5 mt-2">
              <span className="text-[10px] font-medium text-orange-400">🕒
                {new Date(task.dueDate).toLocaleString([], {
                  month: "short",
                  day: "numeric",
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
            </div>
          )}
          <button
            onClick={onDelete}
            className="ml-auto p-1 text-slate-300 hover:text-red-500 transition-colors">
            x
          </button>
      </div>

      {/* RIGHT: Move Forward */}
      {nextStatus && (
        <VerticalNavButton
          direction="right"
          targetStatus={nextStatus}
          onClick={() => onMove("forward")}
          title={`Move to ${nextStatus}`}
        />
      )}
    </motion.div>
  );
};
