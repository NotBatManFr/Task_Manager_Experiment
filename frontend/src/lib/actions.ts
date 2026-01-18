'use server'

import {revalidatePath} from 'next/cache'

const API_URL = 'http://localhost:8000/tasks'

export async function addTaskAction(formData: FormData) {
    const title = formData.get('title') as string
    const status = formData.get('status') as string

    if(!title) return

    await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ title, status })
    })

    revalidatePath('/')
}

export async function deleteTaskAction(id: string) {
    await fetch(`${API_URL}/${id}`, {
        method: 'DELETE'
    })

    revalidatePath('/')
}