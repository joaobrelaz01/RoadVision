import React, { useEffect, useState } from 'react';
import { fetchCameras } from '../services/api';
import { Camera } from '../types';
import { HlsPlayer } from '../components/HlsPlayer';
import { StatusBadge } from '../components/StatusBadge';
import { ShieldAlert, Play, Square, AlertCircle, RefreshCw } from 'lucide-react';

export const LiveMonitorPage: React.FC = () => {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [selectedCamera, setSelectedCamera] = useState<Camera | null>(null);
  const [activeCameraIds, setActiveCameraIds] = useState<string[]>(['36']);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const carregarCameras = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchCameras()
      .then((data) => {
        setCameras(data);
        if (data.length > 0) {
          setSelectedCamera(data[0]);
        }
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

  const toggleCameraActivation = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (activeCameraIds.includes(id)) {
      setActiveCameraIds(activeCameraIds.filter((cId) => cId !== id));
    } else {
      if (activeCameraIds.length >= 2) {
        alert('Limite Operacional: No máximo 2 câmeras podem ser monitoradas simultaneamente.');
        return;
      }
      setActiveCameraIds([...activeCameraIds, id]);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 gap-2">
        <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
        <span>Carregando lista de câmeras...</span>
      </div>
    );
  }

  if (errorMessage) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center max-w-xl mx-auto my-12">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h2 className="text-base font-bold text-rose-800">Erro ao Conectar às Câmeras</h2>
        <p className="text-sm text-rose-600 mt-1 mb-4">{errorMessage}</p>
        <button
          onClick={carregarCameras}
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
            Monitoramento ao vivo
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Selecione uma câmera para visualizar o player HLS oficial do DER/SP.
          </p>
        </div>

        {/* Indicador de Limite Estrito de Câmeras Simultâneas */}
        <div className="flex items-center gap-2 bg-blue-50 border border-blue-200 text-blue-800 px-3.5 py-1.5 rounded-lg text-xs font-medium">
          <ShieldAlert className="w-4 h-4 text-blue-600 shrink-0" />
          <span>Monitoramento ativo: <strong>{activeCameraIds.length}/2 câmeras permitidas</strong></span>
        </div>
      </div>

      {/* Grid: Lista Lateral + Player Principal */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Coluna da Esquerda: CÂMERAS */}
        <div className="lg:col-span-4 bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden flex flex-col h-[520px]">
          <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
            <h2 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              CÂMERAS CADASTRADAS ({cameras.length})
            </h2>
            <span className="text-xs text-slate-400 font-mono">HLS DER</span>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-slate-100 p-2 space-y-1">
            {cameras.map((cam) => {
              const isSelected = selectedCamera?.id === cam.id;
              const isProcessing = activeCameraIds.includes(cam.id);

              return (
                <div
                  key={cam.id}
                  onClick={() => setSelectedCamera(cam)}
                  className={`p-3.5 rounded-lg cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-blue-50/70 border border-blue-200/80 shadow-2xs'
                      : 'hover:bg-slate-50 border border-transparent'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-slate-700">
                          ID {cam.camera_der_id || cam.id}
                        </span>
                        {cam.cadastrada_no_banco && (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                            Supabase
                          </span>
                        )}
                        {isProcessing && (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-blue-100 text-blue-700">
                            Foco
                          </span>
                        )}
                      </div>
                      <h3 className="text-sm font-semibold text-slate-900 mt-0.5">
                        {cam.nome}
                      </h3>
                      <p className="text-xs text-slate-500 mt-0.5">
                        {cam.rodovia} · km {cam.km}
                      </p>
                    </div>

                    <div className="flex flex-col items-end gap-2 shrink-0">
                      <StatusBadge status={cam.status} />
                      <button
                        onClick={(e) => toggleCameraActivation(cam.id, e)}
                        title={isProcessing ? "Desativar monitoramento" : "Ativar para monitoramento"}
                        className={`p-1 rounded text-xs transition-colors cursor-pointer ${
                          isProcessing 
                            ? 'text-rose-600 hover:bg-rose-50' 
                            : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
                        }`}
                      >
                        {isProcessing ? <Square className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Coluna da Direita: Player HLS */}
        <div className="lg:col-span-8">
          <HlsPlayer camera={selectedCamera} />
        </div>
      </div>
    </div>
  );
};
