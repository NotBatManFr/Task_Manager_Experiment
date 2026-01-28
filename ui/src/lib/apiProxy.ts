import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_BACKEND_URL || 'http://backend:8000';

export type ProxyRequestOptions = {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: Record<string, any> | null;
  headers?: Record<string, string>;
};

export type MiddlewareContext = {
  request: NextRequest;
  headers: Record<string, string>;
};

export type Middleware = (context: MiddlewareContext) => Promise<void>;

/**
 * Authentication middleware for future use
 * Currently extracts auth headers if present, can be extended to validate tokens
 */
export const authMiddleware: Middleware = async (context: MiddlewareContext) => {
  const authHeader = context.request.headers.get('authorization');
  if (authHeader) {
    context.headers['authorization'] = authHeader;
  }
};

/**
 * Request ID middleware for tracing (future enhancement)
 */
export const requestIdMiddleware: Middleware = async (context: MiddlewareContext) => {
  const requestId = context.request.headers.get('x-request-id') || 
    `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  context.headers['x-request-id'] = requestId;
};

/**
 * Applies all registered middlewares to the request
 */
async function applyMiddlewares(
  request: NextRequest,
  headers: Record<string, string>,
  middlewares: Middleware[]
): Promise<void> {
  const context: MiddlewareContext = { request, headers };
  for (const middleware of middlewares) {
    await middleware(context);
  }
}

/**
 * Proxies a request to the FastAPI backend
 * @param path - API endpoint path (e.g., '/tasks', '/tasks/123')
 * @param nextRequest - The incoming Next.js request
 * @param options - Request options (method, body, headers)
 * @param middlewares - Array of middleware functions to apply
 * @returns NextResponse with the backend response
 */
export async function proxyRequest(
  path: string,
  nextRequest: NextRequest,
  options: ProxyRequestOptions,
  middlewares: Middleware[] = [authMiddleware, requestIdMiddleware]
): Promise<NextResponse> {
  try {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    };

    // Apply all middlewares (auth, logging, etc.)
    await applyMiddlewares(nextRequest, headers, middlewares);

    const url = `${BACKEND_URL}${path}`;

    const fetchOptions: RequestInit = {
      method: options.method,
      headers,
    };

    if (options.body) {
      fetchOptions.body = JSON.stringify(options.body);
    }

    const response = await fetch(url, fetchOptions);
    const data = await response.json();

    // Map backend status codes to appropriate responses
    if (!response.ok) {
      return NextResponse.json(
        {
          error: data.error || data.message || 'Backend request failed',
          statusCode: response.status,
        },
        { status: response.status }
      );
    }

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error(`Proxy request failed for ${path}:`, error);
    return NextResponse.json(
      {
        error: 'Failed to communicate with backend',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

/**
 * Helper to extract path parameters from URL
 */
export function getPathParam(pathname: string, paramName: string): string | null {
  const regex = new RegExp(`/api/tasks/([^/]+)`);
  const match = pathname.match(regex);
  return match ? match[1] : null;
}
