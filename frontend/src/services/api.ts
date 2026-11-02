import {
  Camera,
  DashboardMetrics,
  CategoryShare,
  HourlyFlowItem,
  HighwaySummary,
  CameraComparisonItem,
  ReportItem,
  UserProfile,
  SystemStatus
} from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function fetchDashboardData(): Promise<{
  metrics: DashboardMetrics;
  categories: CategoryShare[];
  hourly_flow: HourlyFlowItem[];
}> {
  const res = await fetch(`${API_BASE}/api/dashboard`);
  if (!res.ok) {
    throw new Error(`Falha ao obter dados do Dashboard (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchCameras(): Promise<Camera[]> {
  const res = await fetch(`${API_BASE}/api/cameras`);
  if (!res.ok) {
    throw new Error(`Falha ao obter lista de câmeras (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchHighways(): Promise<HighwaySummary[]> {
  const res = await fetch(`${API_BASE}/api/rodovias`);
  if (!res.ok) {
    throw new Error(`Falha ao obter rodovias (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchStatistics(params?: {
  de?: string;
  ate?: string;
  camera_id?: string;
  rodovia?: string;
}): Promise<{
  categories: CategoryShare[];
  camera_comparison: CameraComparisonItem[];
  time_series: { periodo: string; total: number }[];
  total_periodo: number;
}> {
  const query = new URLSearchParams();
  if (params?.de) query.append('de', params.de);
  if (params?.ate) query.append('ate', params.ate);
  if (params?.camera_id && params.camera_id !== 'Todas') query.append('camera_id', params.camera_id);
  if (params?.rodovia && params.rodovia !== 'Todas') query.append('rodovia', params.rodovia);

  const url = `${API_BASE}/api/estatisticas${query.toString() ? `?${query.toString()}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Falha ao obter estatísticas (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchReports(params?: {
  de?: string;
  ate?: string;
  camera_id?: string;
  sentido?: string;
}): Promise<{
  filtros: any;
  total_registros: number;
  registros: ReportItem[];
}> {
  const query = new URLSearchParams();
  if (params?.de) query.append('de', params.de);
  if (params?.ate) query.append('ate', params.ate);
  if (params?.camera_id && params.camera_id !== 'Todas') query.append('camera_id', params.camera_id);
  if (params?.sentido && params.sentido !== 'Todos') query.append('sentido', params.sentido);

  const url = `${API_BASE}/api/relatorios${query.toString() ? `?${query.toString()}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Falha ao obter relatórios (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchUsers(): Promise<UserProfile[]> {
  const res = await fetch(`${API_BASE}/api/auth/usuarios`);
  if (!res.ok) {
    throw new Error(`Falha ao obter usuários (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}

export async function fetchSystemStatus(): Promise<SystemStatus> {
  const res = await fetch(`${API_BASE}/api/status`);
  if (!res.ok) {
    throw new Error(`Falha ao obter status dos serviços (${res.status}): ${res.statusText}`);
  }
  return await res.json();
}
