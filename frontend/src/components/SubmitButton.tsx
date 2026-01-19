'use client';

import { useFormStatus } from 'react-dom';
import { motion } from 'framer-motion';

export function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <motion.button
      whileHover={{ y: -2, boxShadow: "0px 4px 10px rgba(0,0,0,0.1)" }}
      whileTap={{ scale: 0.95 }}
      disabled={pending}
      type="submit"
      className="bg-lime-600 text-white px-6 py-2 rounded-lg font-medium disabled:bg-lime-300 transition-colors"
    >
      {pending ? 'Adding...' : 'Add Task'}
    </motion.button>
  );
}