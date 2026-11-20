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
  extensao_trecho_cadastrado_km?: number;
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
  cargo: 'Operador Master' | 'Administrador' | 'Operador' | 'Visualizador';
  status: 'Ativo' | 'Inativo';
  criado_em: string;
  is_master?: boolean;
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

export interface IntensidadeFluxo {
  classificacao: 'Baixo' | 'Moderado' | 'Intenso' | 'Dados insuficientes para análise';
  taxa_media_veic_h?: number | null;
  criterio_documentado: string;
  detalhes: string;
}

export interface HorariosPico {
  janela_pico: string | null;
  volume_pico: number;
  periodo_analisado: string;
  texto: string;
}

export interface ComposicaoTrafego {
  categoria_lider: string;
  percentual_lider: number;
  distribuicao: Record<string, number>;
  texto: string;
}

export interface PontoMovimentacao {
  camera_id: string;
  camera_der_id?: number | null;
  nome: string;
  km: string;
  total_veiculos: number;
  percentual: number;
}

export interface PontosMaiorMovimentacao {
  ranking: PontoMovimentacao[];
  camera_lider?: string | null;
  texto: string;
}

export interface TendenciaTrafego {
  classificacao: 'Aumento' | 'Redução' | 'Estabilidade' | 'Dados insuficientes para análise';
  variacao_percentual?: number | null;
  volume_atual: number;
  volume_anterior: number;
  texto: string;
}

export interface ConfiabilidadeDados {
  score: 'Alta' | 'Parcial' | 'Limitada';
  total_registros: number;
  cameras_com_dados: number;
  total_cameras_cadastradas: number;
  detalhes: string;
}

export interface AnaliseInteligente {
  intensidade: IntensidadeFluxo;
  horarios_pico: HorariosPico;
  composicao: ComposicaoTrafego;
  pontos_movimentacao: PontosMaiorMovimentacao;
  tendencia: TendenciaTrafego;
  confiabilidade: ConfiabilidadeDados;
  observacoes_automaticas: string[];
}

export interface UltimaCapturaResponse {
  camera_id: string;
  camera_der_id?: number | null;
  nome_camera: string;
  origem: string;
  image_url: string;
  captured_at: string;
  status_modo: string;
  disponivel: boolean;
}

