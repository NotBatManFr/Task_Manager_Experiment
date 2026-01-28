interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  variant?: 'primary' | 'danger' | 'secondary';
  className?: string;
}

export const Button = ({ onClick, children, variant = 'primary', className = '' }: ButtonProps) => {
  const styles = {
    primary: 'bg-blue-400 hover:bg-emerald-400 text-white',
    danger: 'bg-red-500 hover:bg-red-600 text-white',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800'
  };

  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-lg font-medium transition-colors duration-200 active:scale-95 ${styles[variant]} ${className}`}
    >
      {children}
    </button>
  );
};