'use client'; // Error components must be Client Components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="p-8 max-w-2xl mx-auto text-center">
      <h2 className="text-2xl font-bold text-red-600 mb-4">Service Unavailable</h2>
      <p className="text-gray-600 mb-6">
        We're having trouble reaching the Task Service. It might be undergoing maintenance.
      </p>
      <button
        onClick={() => reset()}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        Try Again
      </button>
    </div>
  );
}