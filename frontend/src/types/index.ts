export interface Camera {
  id: string;
  camera_der_id?: number;
  nome: string;
  rodovia: string;
  km: string;
  municipio?: string;
  stream_url?: string;
  status: string;
  ativa: boolean;
  cadastrada_no_banco?: boolean;
  ultima_atualizacao?: string;
}

export interface DashboardMetrics {
  total_veiculos: number;
  cameras_online: number;
  cameras_offline: number;
  total_cameras: number;
  km_monitorados: number;
  rodovias_ativas: number;
  carros: number;
  motos: number;
  onibus: number;
  caminhoes: number;
  is_demo: boolean;
}

export interface CategoryShare {
  name: string;
  value: number;
  color: string;
}

export interface HourlyFlowItem {
  hora: string;
  carros: number;
  motos: number;
  onibus: number;
  caminhoes: number;
  total: number;
}

export interface HighwaySummary {
  nome: string;
  trecho: string;
  km_total: number;
  cameras_count: number;
  municipios_count: number;
  status: string;
  detalhes_municipios: {
    municipio: string;
    cameras: number;
    quilometros: string;
    status: string;
  }[];
}

export interface CameraComparisonItem {
  camera_id: string;
  nome_curto: string;
  carros: number;
  motos: number;
  onibus: number;
  caminhoes: number;
  total: number;
}

export interface ReportItem {
  id: number | string;
  data_hora: string;
  data_hora_raw?: string;
  camera?: string;
  camera_id?: string;
  sentido: string;
  carros: number;
  motos: number;
  onibus: number;
  caminhoes: number;
  total: number;
}

export interface UserProfile {
  id: string;
  nome: string;
  email: string;
  cargo: 'Administrador' | 'Operador' | 'Visualizador';
  status: 'Ativo' | 'Inativo';
  criado_em: string;
}

export interface SystemStatus {
  supabase_connected: boolean;
  api_status: string;
  yolo_processing_status: string;
  oracle_cloud_status: string;
  active_cameras_limit: number;
  active_cameras_count: number;
  version: string;
  last_ping: string;
}
