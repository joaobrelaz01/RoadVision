import React, { useEffect, useState } from 'react';
import { Database, Server, Cpu, Cloud, CheckCircle2, Sliders, Shield, AlertCircle, RefreshCw, XCircle } from 'lucide-react';
import { fetchSystemStatus } from '../services/api';
import { SystemStatus } from '../types';

export const SettingsPage: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const carregarStatus = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchSystemStatus()
      .then((data) => {
        setStatus(data);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Erro ao checar status do sistema.');
        setLoading(false);
      });
  };

  useEffect(() => {
    carregarStatus();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 gap-2">
        <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
        <span>Diagnosticando conexões dos serviços...</span>
      </div>
    );
  }

  if (errorMessage || !status) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center max-w-xl mx-auto my-12">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h2 className="text-base font-bold text-rose-800">Falha no Diagnóstico dos Serviços</h2>
        <p className="text-sm text-rose-600 mt-1 mb-4">{errorMessage || 'Não foi possível contatar a API.'}</p>
        <button
          onClick={carregarStatus}
          className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-semibold transition-colors cursor-pointer"
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Título e Subtítulo */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
            Configurações e Status
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Diagnóstico de saúde das conexões, limites de processamento e infraestrutura.
          </p>
        </div>

        <button
          onClick={carregarStatus}
          className="self-start sm:self-auto inline-flex items-center gap-2 px-3.5 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-sm font-semibold shadow-2xs transition-colors cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Atualizar Diagnóstico</span>
        </button>
      </div>

      {/* Grid de Estado dos Serviços Reais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Supabase */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                BANCO DE DADOS
              </span>
              <div className="text-lg font-bold text-slate-900">
                Supabase
              </div>
              <p className="text-xs text-slate-500 mt-1">
                PostgreSQL + Realtime
              </p>
            </div>
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
              status.supabase_connected ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'
            }`}>
              <Database className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1.5 text-xs font-semibold">
            {status.supabase_connected ? (
              <>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                <span className="text-emerald-700">Conexão verificada ativa</span>
              </>
            ) : (
              <>
                <XCircle className="w-4 h-4 text-rose-500" />
                <span className="text-rose-700">Falha na conexão</span>
              </>
            )}
          </div>
        </div>

        {/* FastAPI */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                BACKEND API
              </span>
              <div className="text-lg font-bold text-slate-900">
                FastAPI
              </div>
              <p className="text-xs text-slate-500 mt-1">
                v{status.version}
              </p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Server className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1.5 text-xs font-semibold text-emerald-700">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>Servidor {status.api_status}</span>
          </div>
        </div>

        {/* Processamento YOLO */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                PROCESSAMENTO IA
              </span>
              <div className="text-lg font-bold text-slate-900">
                YOLO11
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Detecção e tracking
              </p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center">
              <Cpu className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1.5 text-xs font-medium text-slate-600">
            <span>{status.yolo_processing_status}</span>
          </div>
        </div>

        {/* Oracle Cloud */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                ORACLE CLOUD
              </span>
              <div className="text-lg font-bold text-slate-900">
                Oracle VM
              </div>
              <p className="text-xs text-slate-500 mt-1">
                Workflow cd-oracle.yml
              </p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-orange-50 text-orange-600 flex items-center justify-center">
              <Cloud className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-1.5 text-xs font-medium text-slate-600">
            <span className="truncate">{status.oracle_cloud_status}</span>
          </div>
        </div>
      </div>

      {/* Parâmetros Operacionais */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <Sliders className="w-5 h-5 text-slate-700" />
          <h2 className="text-base font-bold text-slate-900">
            Parâmetros Operacionais e Limites Verificados
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200/70">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-slate-800">Limite de Câmeras Simultâneas</span>
              <span className="px-2 py-0.5 rounded text-xs font-bold bg-blue-100 text-blue-700">
                {status.active_cameras_limit} câmeras
              </span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              O pipeline do RoadVision processa no máximo {status.active_cameras_limit} câmeras simultaneamente para respeitar os limites de CPU e memória da VM Oracle Cloud.
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200/70">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-slate-800">Tabelas Supabase Conectadas</span>
              <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-100 text-emerald-700">
                Verificadas
              </span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Tabelas ativas com dados gravados: <code className="text-sky-700 bg-sky-50 px-1 rounded">cameras</code>, <code className="text-sky-700 bg-sky-50 px-1 rounded">contagens_minuto</code> e <code className="text-sky-700 bg-sky-50 px-1 rounded">contagens_por_sentido</code>.
            </p>
          </div>
        </div>
      </div>

      {/* Diretrizes de Segurança */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-3">
          <Shield className="w-5 h-5 text-emerald-600" />
          <h2 className="text-base font-bold text-slate-900">
            Segurança e Integridade
          </h2>
        </div>
        <ul className="text-xs text-slate-600 space-y-2 list-disc list-inside">
          <li>As consultas do frontend passam pelo backend FastAPI em <code className="text-slate-800 font-mono bg-slate-100 px-1 rounded">/api</code>.</li>
          <li>A chave administrativa <code className="text-rose-600 font-mono bg-rose-50 px-1 rounded">SUPABASE_SERVICE_ROLE_KEY</code> permanece restrita ao backend e protegida contra exposição no navegador.</li>
          <li>Última verificação de integridade realizada em: <span className="font-mono">{status.last_ping}</span>.</li>
        </ul>
      </div>
    </div>
  );
};
