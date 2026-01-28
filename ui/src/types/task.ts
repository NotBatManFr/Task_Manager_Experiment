export type TaskStatus = 'todo' | 'in_progress' | 'done';

export interface TaskCreate {
  title: string;
  status?: TaskStatus;
  dueDate?: string | null; // ISO 8601 datetime string
}

export interface Task extends TaskCreate {
  id: string;
  status: TaskStatus;
}

export interface TaskResponse extends Task {
  // Response model that includes all fields
}
