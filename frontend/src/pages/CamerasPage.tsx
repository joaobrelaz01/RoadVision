import React, { useEffect, useState } from 'react';
import { Search, AlertCircle, RefreshCw } from 'lucide-react';
import { fetchCameras } from '../services/api';
import { Camera } from '../types';
import { StatusBadge } from '../components/StatusBadge';

export const CamerasPage: React.FC = () => {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [filteredCameras, setFilteredCameras] = useState<Camera[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMunicipio, setSelectedMunicipio] = useState('Todos');
  const [selectedStatus, setSelectedStatus] = useState('Todos');
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const carregarCameras = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchCameras()
      .then((data) => {
        setCameras(data);
        setFilteredCameras(data);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Erro ao carregar câmeras.');
        setLoading(false);
      });
  };

  useEffect(() => {
    carregarCameras();
  }, []);

  useEffect(() => {
    let result = [...cameras];

    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      result = result.filter(
        (c) =>
          c.id.toLowerCase().includes(term) ||
          c.nome.toLowerCase().includes(term) ||
          (c.municipio && c.municipio.toLowerCase().includes(term))
      );
    }

    if (selectedMunicipio !== 'Todos') {
      result = result.filter((c) => c.municipio === selectedMunicipio);
    }

    if (selectedStatus !== 'Todos') {
      result = result.filter((c) => c.status.toLowerCase().includes(selectedStatus.toLowerCase()));
    }

    setFilteredCameras(result);
  }, [searchTerm, selectedMunicipio, selectedStatus, cameras]);

  const municipios = ['Todos', 'Maranduba', 'Caraguatatuba', 'São Sebastião', 'Massaguaçu', 'Bertioga'];

  return (
    <div className="space-y-6">
      {/* Título e Subtítulo */}
      <div>
        <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
          Câmeras
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Lista de câmeras monitoradas ao longo da rodovia SP-055 e status de cadastro no Supabase.
        </p>
      </div>

      {/* Barra de Filtros */}
      <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
          <div className="md:col-span-6">
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">
              Pesquisar
            </label>
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="ID, local ou município"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-white border border-slate-200 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
              />
            </div>
          </div>

          <div className="md:col-span-3">
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">
              Município
            </label>
            <select
              value={selectedMunicipio}
              onChange={(e) => setSelectedMunicipio(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 cursor-pointer"
            >
              {municipios.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>

          <div className="md:col-span-3">
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">
              Status
            </label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 cursor-pointer"
            >
              <option value="Todos">Todos</option>
              <option value="Online">Online</option>
              <option value="Sem conexão">Sem conexão</option>
            </select>
          </div>
        </div>
      </div>

      {errorMessage && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 text-rose-700 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 text-rose-500" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Tabela de Câmeras */}
      <div className="bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-slate-400 gap-2">
            <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
            <span>Carregando câmeras cadastradas...</span>
          </div>
        ) : filteredCameras.length === 0 ? (
          <div className="p-12 text-center text-slate-400">
            Nenhuma câmera encontrada para os filtros selecionados.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50/70 border-b border-slate-100 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-6">ID</th>
                  <th className="py-3 px-6">LOCAL</th>
                  <th className="py-3 px-6">RODOVIA</th>
                  <th className="py-3 px-6">KM</th>
                  <th className="py-3 px-6">MUNICÍPIO</th>
                  <th className="py-3 px-6">BANCO</th>
                  <th className="py-3 px-6">STATUS</th>
                  <th className="py-3 px-6">ÚLTIMA ATUALIZAÇÃO</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredCameras.map((cam) => (
                  <tr key={cam.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-4 px-6 font-bold text-slate-800">
                      {cam.camera_der_id || cam.id}
                    </td>
                    <td className="py-4 px-6 font-medium text-slate-800">
                      {cam.nome}
                    </td>
                    <td className="py-4 px-6 text-slate-600">
                      {cam.rodovia}
                    </td>
                    <td className="py-4 px-6 text-slate-600">
                      {cam.km}
                    </td>
                    <td className="py-4 px-6 text-slate-600">
                      {cam.municipio || '—'}
                    </td>
                    <td className="py-4 px-6">
                      {cam.cadastrada_no_banco ? (
                        <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-100 text-emerald-800">
                          Cadastrada
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-xs text-slate-400">
                          Não cadastrada
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-6">
                      <StatusBadge status={cam.status} />
                    </td>
                    <td className="py-4 px-6 text-slate-400">
                      {cam.ultima_atualizacao || '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
