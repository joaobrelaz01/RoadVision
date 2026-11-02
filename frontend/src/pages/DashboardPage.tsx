import React, { useEffect, useState } from 'react';
import {
  Activity,
  Wifi,
  WifiOff,
  Gauge,
  Car,
  Bike,
  Bus,
  Truck,
  AlertCircle,
  RefreshCw
} from 'lucide-react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip
} from 'recharts';
import { StatCard } from '../components/StatCard';
import { fetchDashboardData } from '../services/api';
import { DashboardMetrics, CategoryShare, HourlyFlowItem } from '../types';

export const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [categories, setCategories] = useState<CategoryShare[]>([]);
  const [hourlyFlow, setHourlyFlow] = useState<HourlyFlowItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadData = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchDashboardData()
      .then((data) => {
        setMetrics(data.metrics);
        setCategories(data.categories);
        setHourlyFlow(data.hourly_flow);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Falha ao conectar à API RoadVision.');
        setLoading(false);
      });
  };

  useEffect(() => {
    loadData();
  }, []);

  const formatNumber = (val: number) => val.toLocaleString('pt-BR');

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-slate-500 gap-3">
        <RefreshCw className="w-6 h-6 animate-spin text-sky-600" />
        <span className="text-sm font-medium">Consultando registros reais do Supabase...</span>
      </div>
    );
  }

  if (errorMessage || !metrics) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center max-w-xl mx-auto my-12">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h2 className="text-base font-bold text-rose-800">Erro na Comunicação com o Backend</h2>
        <p className="text-sm text-rose-600 mt-1 mb-4">{errorMessage || 'Não foi possível carregar as métricas.'}</p>
        <button
          onClick={loadData}
          className="inline-flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-semibold transition-colors cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Tentar novamente</span>
        </button>
      </div>
    );
  }

  const hasVehicleData = metrics.total_veiculos > 0;
  const filteredCategories = categories.filter((c) => c.value > 0);

  return (
    <div className="space-y-6">
      {/* Título e Subtítulo */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
            Dashboard
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Indicadores consolidados em tempo real a partir da tabela contagens_minuto do Supabase.
          </p>
        </div>

        <button
          onClick={loadData}
          title="Atualizar dados agora"
          className="self-start sm:self-auto p-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-lg shadow-2xs transition-colors cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Grid 1: Indicadores Globais Reais */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="TOTAL DE VEÍCULOS"
          value={formatNumber(metrics.total_veiculos)}
          icon={<Activity className="w-5 h-5" />}
          iconBgColor="bg-blue-50"
          iconColor="text-blue-600"
        />
        <StatCard
          title="CÂMERAS ONLINE"
          value={metrics.cameras_online}
          subtitle={`de ${metrics.total_cameras} cadastradas`}
          icon={<Wifi className="w-5 h-5" />}
          iconBgColor="bg-emerald-50"
          iconColor="text-emerald-600"
        />
        <StatCard
          title="CÂMERAS SEM CONEXÃO"
          value={metrics.cameras_offline}
          icon={<WifiOff className="w-5 h-5" />}
          iconBgColor="bg-rose-50"
          iconColor="text-rose-500"
        />
        <StatCard
          title="KM MONITORADOS"
          value={metrics.km_monitorados}
          subtitle={`${metrics.rodovias_ativas} rodovia ativa`}
          icon={<Gauge className="w-5 h-5" />}
          iconBgColor="bg-amber-50"
          iconColor="text-amber-600"
        />
      </div>

      {/* Grid 2: Categorias Reais */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="CARROS"
          value={formatNumber(metrics.carros)}
          icon={<Car className="w-5 h-5" />}
          iconBgColor="bg-sky-50"
          iconColor="text-sky-600"
        />
        <StatCard
          title="MOTOS"
          value={formatNumber(metrics.motos)}
          icon={<Bike className="w-5 h-5" />}
          iconBgColor="bg-orange-50"
          iconColor="text-orange-600"
        />
        <StatCard
          title="ÔNIBUS"
          value={formatNumber(metrics.onibus)}
          icon={<Bus className="w-5 h-5" />}
          iconBgColor="bg-cyan-50"
          iconColor="text-cyan-600"
        />
        <StatCard
          title="CAMINHÕES"
          value={formatNumber(metrics.caminhoes)}
          icon={<Truck className="w-5 h-5" />}
          iconBgColor="bg-slate-100"
          iconColor="text-slate-800"
        />
      </div>

      {/* Gráficos em Duas Colunas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Gráfico 1: Rosca de Categorias */}
        <div className="lg:col-span-5 bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-6">
              VEÍCULOS POR CATEGORIA
            </h2>
            <div className="h-64 w-full flex items-center justify-center">
              {hasVehicleData ? (
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
                    <Tooltip
                      formatter={(val: number) => [formatNumber(val), 'Veículos']}
                      contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center text-slate-400 text-sm">
                  Nenhum veículo contabilizado até o momento.
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

        {/* Gráfico 2: Linhas de Movimentação ao Longo do Dia */}
        <div className="lg:col-span-7 bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-6">
              MOVIMENTAÇÃO AO LONGO DO DIA
            </h2>
            <div className="h-64 w-full">
              {hasVehicleData ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={hourlyFlow} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                    <XAxis
                      dataKey="hora"
                      stroke="#94A3B8"
                      fontSize={11}
                      tickLine={false}
                      axisLine={{ stroke: '#E2E8F0' }}
                    />
                    <YAxis
                      stroke="#94A3B8"
                      fontSize={11}
                      tickLine={false}
                      axisLine={{ stroke: '#E2E8F0' }}
                      tickFormatter={(val) => val === 0 ? '0' : `${val}`}
                    />
                    <Tooltip
                      contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="carros"
                      name="Carros"
                      stroke="#0284c7"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 4 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="caminhoes"
                      name="Caminhões"
                      stroke="#1e293b"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 4 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="motos"
                      name="Motos"
                      stroke="#f97316"
                      strokeWidth={1.5}
                      dot={false}
                      activeDot={{ r: 4 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="onibus"
                      name="Ônibus"
                      stroke="#06b6d4"
                      strokeWidth={1.5}
                      dot={false}
                      activeDot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-center text-slate-400 text-sm">
                  Nenhum tráfego registrado nas últimas 24 horas.
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
    </div>
  );
};
