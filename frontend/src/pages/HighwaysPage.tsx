import React, { useEffect, useState } from 'react';
import { Plus, RefreshCw, AlertCircle } from 'lucide-react';
import { fetchHighways } from '../services/api';
import { HighwaySummary } from '../types';
import { StatusBadge } from '../components/StatusBadge';

export const HighwaysPage: React.FC = () => {
  const [highways, setHighways] = useState<HighwaySummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const carregarRodovias = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchHighways()
      .then((data) => {
        setHighways(data);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Erro ao carregar dados das rodovias.');
        setLoading(false);
      });
  };

  useEffect(() => {
    carregarRodovias();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 gap-2">
        <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
        <span>Carregando dados das rodovias...</span>
      </div>
    );
  }

  if (errorMessage) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center max-w-xl mx-auto my-12">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h2 className="text-base font-bold text-rose-800">Falha ao Carregar Rodovias</h2>
        <p className="text-sm text-rose-600 mt-1 mb-4">{errorMessage}</p>
        <button
          onClick={carregarRodovias}
          className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-semibold transition-colors cursor-pointer"
        >
          Tentar novamente
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho da Página com Botão + Nova Rodovia */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
            Rodovias
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Trechos monitorados e municípios atendidos ao longo da rodovia SP-055.
          </p>
        </div>

        <button
          onClick={() => alert('Cadastro de rodovias requer privilégios de Administrador no Supabase.')}
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#0284C7] hover:bg-[#0369A1] text-white rounded-lg text-sm font-semibold shadow-sm transition-colors cursor-pointer self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Nova rodovia</span>
        </button>
      </div>

      {/* Cards de Rodovias */}
      {highways.map((hw, idx) => (
        <div key={idx} className="bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden">
          {/* Header do Card */}
          <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <h2 className="text-base font-bold text-slate-800 tracking-tight">
              {hw.nome}
            </h2>
            <StatusBadge status={hw.status} />
          </div>

          {/* Grid de Métricas da Rodovia (4 colunas) */}
          <div className="grid grid-cols-2 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-slate-100 p-6 bg-slate-50/50">
            <div className="p-3">
              <span className="text-xs text-slate-500 font-medium block">Trecho monitorado</span>
              <span className="text-base font-bold text-slate-900 mt-1 block">{hw.trecho}</span>
            </div>
            <div className="p-3">
              <span className="text-xs text-slate-500 font-medium block">Km monitorados</span>
              <span className="text-2xl font-bold text-slate-900 mt-1 block">{hw.km_total}</span>
            </div>
            <div className="p-3">
              <span className="text-xs text-slate-500 font-medium block">Câmeras vinculadas</span>
              <span className="text-2xl font-bold text-slate-900 mt-1 block">{hw.cameras_count}</span>
            </div>
            <div className="p-3">
              <span className="text-xs text-slate-500 font-medium block">Municípios atendidos</span>
              <span className="text-2xl font-bold text-slate-900 mt-1 block">{hw.municipios_count}</span>
            </div>
          </div>

          {/* Tabela de Municípios Cobertos */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50/70 border-y border-slate-100 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-6">MUNICÍPIO</th>
                  <th className="py-3 px-6">CÂMERAS</th>
                  <th className="py-3 px-6">QUILÔMETROS COBERTOS</th>
                  <th className="py-3 px-6">STATUS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {hw.detalhes_municipios.map((m, mIdx) => (
                  <tr key={mIdx} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-4 px-6 font-semibold text-slate-800">{m.municipio}</td>
                    <td className="py-4 px-6 text-slate-600 font-medium">{m.cameras}</td>
                    <td className="py-4 px-6 text-slate-600">{m.quilometros}</td>
                    <td className="py-4 px-6">
                      <StatusBadge status={m.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
};
