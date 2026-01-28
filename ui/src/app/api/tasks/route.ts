import { NextRequest, NextResponse } from 'next/server';
import { proxyRequest } from '@/lib/apiProxy';
import { TaskCreate, Task } from '@/types/task';

/**
 * GET /api/tasks
 * Retrieve all tasks from the backend
 */
export async function GET(request: NextRequest): Promise<NextResponse> {
  return proxyRequest('/tasks', request, {
    method: 'GET',
  });
}

/**
 * POST /api/tasks
 * Create a new task
 */
export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json() as TaskCreate;

    // Validate required fields
    if (!body.title || typeof body.title !== 'string') {
      return NextResponse.json(
        { error: 'Task title is required and must be a string' },
        { status: 400 }
      );
    }

    return proxyRequest('/tasks', request, {
      method: 'POST',
      body: {
        title: body.title,
        status: body.status || 'todo',
        dueDate: body.dueDate || null,
      },
    });
  } catch (error) {
    console.error('Error parsing POST request:', error);
    return NextResponse.json(
      { error: 'Invalid request body' },
      { status: 400 }
    );
  }
}
