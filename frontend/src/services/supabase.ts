import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

export const supabase = (supabaseUrl && supabaseAnonKey)
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export function subscribeToRealtimeCounts(callback: (payload: any) => void) {
  if (!supabase) return () => {};

  const channel = supabase
    .channel('roadvision-realtime')
    .on(
      'postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'contagens_minuto' },
      (payload) => {
        console.log('[Supabase Realtime] Nova contagem por minuto:', payload);
        callback(payload.new);
      }
    )
    .on(
      'postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'contagens_por_sentido' },
      (payload) => {
        console.log('[Supabase Realtime] Nova contagem por sentido:', payload);
        callback(payload.new);
      }
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
}
