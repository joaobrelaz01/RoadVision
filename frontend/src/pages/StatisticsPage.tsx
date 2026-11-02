import React, { useEffect, useState } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  LineChart,
  Line
} from 'recharts';
import { Filter, RefreshCw, AlertCircle } from 'lucide-react';
import { fetchStatistics, fetchCameras } from '../services/api';
import { CategoryShare, CameraComparisonItem, Camera } from '../types';

export const StatisticsPage: React.FC = () => {
  const [categories, setCategories] = useState<CategoryShare[]>([]);
  const [cameraComparison, setCameraComparison] = useState<CameraComparisonItem[]>([]);
  const [timeSeries, setTimeSeries] = useState<{ periodo: string; total: number }[]>([]);
  const [totalPeriodo, setTotalPeriodo] = useState<number>(0);
  const [cameras, setCameras] = useState<Camera[]>([]);

  // Datas padrão reais: últimos 7 dias até hoje
  const hoje = new Date().toISOString().split('T')[0];
  const seteDiasAtras = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  const [dataDe, setDataDe] = useState(seteDiasAtras);
  const [dataAte, setDataAte] = useState(hoje);
  const [selectedRodovia, setSelectedRodovia] = useState('Todas');
  const [selectedCamera, setSelectedCamera] = useState('Todas');

  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchCameras()
      .then((data) => setCameras(data))
      .catch((e) => console.warn('Falha ao obter lista de câmeras para filtros:', e));
  }, []);

  const aplicarFiltros = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchStatistics({
      de: dataDe,
      ate: dataAte,
      camera_id: selectedCamera,
      rodovia: selectedRodovia
    })
      .then((data) => {
        setCategories(data.categories);
        setCameraComparison(data.camera_comparison);
        setTimeSeries(data.time_series);
        setTotalPeriodo(data.total_periodo || 0);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Erro ao consultar estatísticas.');
        setLoading(false);
      });
  };

  useEffect(() => {
    aplicarFiltros();
  }, []);

  const formatNumber = (val: number) => val.toLocaleString('pt-BR');
  const hasData = totalPeriodo > 0;
  const filteredCategories = categories.filter((c) => c.value > 0);

  return (
    <div className="space-y-6">
      {/* Título e Subtítulo */}
      <div>
        <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
          Estatísticas
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Dados reais agregados diretamente a partir do banco de dados do RoadVision.
        </p>
      </div>

      {/* Barra de Filtros Reais */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 items-end">
          <div>
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">De</label>
            <input
              type="date"
              value={dataDe}
              onChange={(e) => setDataDe(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">Até</label>
            <input
              type="date"
              value={dataAte}
              onChange={(e) => setDataAte(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">Rodovia</label>
            <select
              value={selectedRodovia}
              onChange={(e) => setSelectedRodovia(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 cursor-pointer"
            >
              <option value="Todas">Todas</option>
              <option value="SP-055">SP-055 — Rodovia Rio-Santos</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">Câmera</label>
            <select
              value={selectedCamera}
              onChange={(e) => setSelectedCamera(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 cursor-pointer"
            >
              <option value="Todas">Todas as Câmeras</option>
              {cameras.map((c) => (
                <option key={c.id} value={c.id}>
                  ID {c.camera_der_id || c.id} — {c.nome}
                </option>
              ))}
            </select>
          </div>

          <div>
            <button
              onClick={aplicarFiltros}
              disabled={loading}
              className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 bg-[#0284C7] hover:bg-[#0369A1] text-white rounded-lg text-sm font-semibold shadow-sm transition-colors cursor-pointer disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Filter className="w-4 h-4" />}
              <span>Filtrar</span>
            </button>
          </div>
        </div>
      </div>

      {errorMessage && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 text-rose-700 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 text-rose-500" />
          <span>{errorMessage}</span>
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center h-64 text-slate-400 gap-2">
          <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
          <span>Calculando dados estatísticos reais...</span>
        </div>
      ) : (
        <>
          {/* Grid: Rosca + Comparação entre Câmeras */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Rosca de Categorias */}
            <div className="lg:col-span-5 bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    VEÍCULOS POR CATEGORIA
                  </h2>
                  <span className="text-xs font-bold text-slate-700">
                    Total: {formatNumber(totalPeriodo)}
                  </span>
                </div>
                <div className="h-64 w-full flex items-center justify-center">
                  {hasData ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={filteredCategories.length > 0 ? filteredCategories : categories}
                          innerRadius={65}
                          outerRadius={95}
                          paddingAngle={3}
                          dataKey="value"
                        >
                          {categories.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(val: number) => [formatNumber(val), 'Veículos']} />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="text-center text-slate-400 text-sm">
                      Nenhum veículo encontrado para os filtros selecionados.
                    </div>
                  )}
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-4 pt-4 border-t border-slate-100 text-xs">
                {categories.map((c) => (
                  <div key={c.name} className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: c.color }} />
                    <span className="text-slate-600 font-medium">{c.name}: {formatNumber(c.value)}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Comparação entre Câmeras */}
            <div className="lg:col-span-7 bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm flex flex-col justify-between">
              <div>
                <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-6">
                  COMPARAÇÃO ENTRE CÂMERAS COM CONTAGEM
                </h2>
                <div className="h-64 w-full">
                  {cameraComparison.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={cameraComparison} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                        <XAxis dataKey="nome_curto" stroke="#94A3B8" fontSize={11} tickLine={false} />
                        <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} tickFormatter={(val) => `${val}`} />
                        <Tooltip formatter={(val: number) => [formatNumber(val), '']} />
                        <Bar dataKey="carros" stackId="a" fill="#0284c7" name="Carros" />
                        <Bar dataKey="motos" stackId="a" fill="#f97316" name="Motos" />
                        <Bar dataKey="onibus" stackId="a" fill="#06b6d4" name="Ônibus" />
                        <Bar dataKey="caminhoes" stackId="a" fill="#1e293b" name="Caminhões" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-full flex items-center justify-center text-center text-slate-400 text-sm">
                      Nenhuma contagem registrada para as câmeras neste período.
                    </div>
                  )}
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-4 pt-4 border-t border-slate-100 text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#0284c7]" />
                  <span className="text-slate-600 font-medium">Carros</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#f97316]" />
                  <span className="text-slate-600 font-medium">Motos</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#06b6d4]" />
                  <span className="text-slate-600 font-medium">Ônibus</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#1e293b]" />
                  <span className="text-slate-600 font-medium">Caminhões</span>
                </div>
              </div>
            </div>
          </div>

          {/* Gráfico Inferior: Movimentação por Período */}
          <div className="bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm">
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-6">
              MOVIMENTAÇÃO DIÁRIA NO PERÍODO
            </h2>
            <div className="h-64 w-full">
              {timeSeries.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={timeSeries} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                    <XAxis dataKey="periodo" stroke="#94A3B8" fontSize={11} tickLine={false} />
                    <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} tickFormatter={(val) => `${val}`} />
                    <Tooltip formatter={(val: number) => [formatNumber(val), 'Total de Veículos']} />
                    <Line
                      type="monotone"
                      dataKey="total"
                      name="Total"
                      stroke="#0284c7"
                      strokeWidth={2.5}
                      dot={{ r: 4, fill: '#0284c7' }}
                      activeDot={{ r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-center text-slate-400 text-sm">
                  Nenhum dado temporal disponível no intervalo selecionado.
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
