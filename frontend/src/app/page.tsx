import { addTaskAction, deleteTaskAction } from "@/lib/actions"

interface Task {
    id: string
    title: string
    status: string
}

export default async function Page() {
    const response = await fetch('http://localhost:8000/tasks', { cache: 'no-store' })
    const tasks: Task[] = await response.json()

    return (
        <html>
            <body className="p-10 max-w-md mx-auto">
                <h1 className="text-2xl font-bold mb-4">Tasks (Server Actions)</h1>
                <form action={addTaskAction} className="flex gap-2 mb-6">
                    <input name="title" className="border p-2 flex-1 rounded text-white" placeholder="Add a new task" required/>
                    <select name="status" className="border p-2 rounded text-white">
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="done">Done</option>
                    </select>
                    <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Add</button>
                </form>
                <ul className="space-y-2">
                    {tasks.map((task) => (
                        <li key={task.id} className="flex justify-between items-center p-3 border rounded">
                            <span>
                                {task.title} <small className="text-gray-400">({task.status})</small>
                            </span>
                            <form action={deleteTaskAction.bind(null, task.id)}>
                                <button className="bg-red-500 text-white px-2 py-1 rounded text-sm">Delete</button>
                            </form>
                        </li>
                    ))}
                </ul>
            </body>
        </html>
    )
}