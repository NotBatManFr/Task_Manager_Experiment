import TaskContainer from '@/components/TaskContainer';

const API_URL = `${process.env.API_URL}/tasks`

export default async function Page() {
  const res = await fetch(API_URL, { cache: 'no-store' });
  const tasks = await res.json();

  return (
    <div className="min-h-screen bg-slate-50 py-20 px-4">
      <div className="max-w-xl mx-auto">
        <header className="mb-10 text-center">
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">Focus.</h1>
          <p className="text-slate-500 mt-2 font-medium">Manage your daily flow with ease.</p>
        </header>

        <TaskContainer initialTasks={tasks} />
      </div>
    </div>
  );
}