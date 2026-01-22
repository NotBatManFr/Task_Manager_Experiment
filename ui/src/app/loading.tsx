export default function Loading() {
  return (
    <div className="p-8 max-w-2xl mx-auto animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded mb-6"></div>
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 bg-gray-100 rounded-lg border border-gray-200"></div>
        ))}
      </div>
    </div>
  );
}