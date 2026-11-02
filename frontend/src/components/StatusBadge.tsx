import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const isOnline = status.toLowerCase().includes('online') || status.toLowerCase().includes('conectado');

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
      isOnline 
        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
        : 'bg-slate-100 text-slate-600 border border-slate-200'
    }`}>
      <span className={`w-1.5 h-1.5 rounded-full ${
        isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'
      }`} />
      {status}
    </span>
  );
};
