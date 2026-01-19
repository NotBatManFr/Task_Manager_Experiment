interface InputProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  onEnter?: () => void;
}

export const Input = ({ value, onChange, placeholder, onEnter }: InputProps) => (
  <input
    type="text"
    value={value}
    onChange={(e) => onChange(e.target.value)}
    onKeyDown={(e) => e.key === 'Enter' && onEnter?.()}
    placeholder={placeholder}
    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-700"
  />
);