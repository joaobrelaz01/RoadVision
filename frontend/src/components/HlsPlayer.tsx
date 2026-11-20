import React, { useEffect, useState } from 'react';
import { VideoOff, RefreshCw, Camera as CameraIcon, Radio, Zap } from 'lucide-react';
import { Camera, UltimaCapturaResponse } from '../types';
import { fetchUltimaCaptura, getLiveCameraUrl } from '../services/api';

interface HlsPlayerProps {
  camera: Camera | null;
}

export const HlsPlayer: React.FC<HlsPlayerProps> = ({ camera }) => {
  const [isLiveActive, setIsLiveActive] = useState(true);
  const [streamError, setStreamError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [fallbackCapture, setFallbackCapture] = useState<UltimaCapturaResponse | null>(null);
  const [lastFetchTime, setLastFetchTime] = useState<number>(Date.now());
  const [retryKey, setRetryKey] = useState<number>(0);

  // Busca a última captura para o caso de fallback
  const carregarUltimaCaptura = (camId?: string) => {
    fetchUltimaCaptura(camId)
      .then((cap) => {
        setFallbackCapture(cap);
        setLastFetchTime(Date.now());
      })
      .catch((err) => {
        console.warn('Falha ao carregar última captura:', err);
      });
  };

  useEffect(() => {
    if (!camera) return;

    // Tenta primeiro o stream ao vivo real
    setIsLoading(true);
    setStreamError(false);
    setIsLiveActive(true);

    carregarUltimaCaptura(camera.id);

    // Polling a cada 30 segundos para manter a captura atualizada
    const interval = setInterval(() => {
      carregarUltimaCaptura(camera.id);
    }, 30000);

    return () => clearInterval(interval);
  }, [camera, retryKey]);

  const tentarReconectarAoVivo = () => {
    setIsLoading(true);
    setStreamError(false);
    setIsLiveActive(true);
    setRetryKey((prev) => prev + 1);
  };

  if (!camera) {
    return (
      <div className="bg-[#0B192C] text-white rounded-xl h-[480px] flex items-center justify-center p-8">
        <p className="text-slate-400">Selecione uma câmera para visualizar.</p>
      </div>
    );
  }

  const liveUrl = getLiveCameraUrl(camera.id);

  return (
    <div className="bg-[#0B192C] rounded-xl overflow-hidden shadow-lg border border-slate-800 flex flex-col h-[520px]">
      {/* Faixa decorativa Hazard Tape */}
      <div className="h-2 w-full hazard-stripes shrink-0" />

      {/* Área do Player / Stream Ao Vivo / Captura */}
      <div className="relative flex-1 bg-[#071322] flex items-center justify-center overflow-hidden">
        {/* Caso 1: Ao Vivo Ativo (ou tentando carregar ao vivo) */}
        {!streamError ? (
          <div className="relative w-full h-full flex items-center justify-center bg-black">
            {/* Selo Verde AO VIVO com Indicador Pulsante */}
            <div className="absolute top-3 left-3 z-20 flex items-center gap-2 bg-emerald-600/95 text-white px-3 py-1 rounded-md text-xs font-bold shadow-md backdrop-blur-xs border border-emerald-400/40">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-200 animate-ping absolute" />
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-300 relative" />
              <span className="tracking-wide">AO VIVO</span>
            </div>

            <div className="absolute top-3 right-3 z-20 flex items-center gap-2 bg-slate-900/80 text-emerald-400 px-2.5 py-1 rounded-md text-[11px] font-mono border border-emerald-500/30">
              <Radio className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
              <span>Stream DER/SP Real</span>
            </div>

            {isLoading && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-[#071322]/80 z-10 gap-2">
                <RefreshCw className="w-8 h-8 text-emerald-400 animate-spin" />
                <span className="text-xs text-slate-300 font-medium">Sintonizando stream da câmera...</span>
              </div>
            )}

            {/* Imagem do Stream MJPEG multipart em tempo real */}
            <img
              key={`live-stream-${camera.id}-${retryKey}`}
              src={`${liveUrl}?t=${retryKey}`}
              alt={`Transmissão ao vivo da ${camera.nome}`}
              className="w-full h-full object-contain"
              onLoad={() => {
                setIsLoading(false);
                setStreamError(false);
                setIsLiveActive(true);
              }}
              onError={() => {
                console.warn('Stream ao vivo indisponível. Alternando para Modo Captura / Arquivo.');
                setIsLoading(false);
                setStreamError(true);
                setIsLiveActive(false);
              }}
            />
          </div>
        ) : (
          /* Caso 2: Fallback Modo Captura / Arquivo */
          fallbackCapture ? (
            <div className="relative w-full h-full flex flex-col items-center justify-center bg-black/90">
              {/* Badge Amarela Modo Captura / Arquivo */}
              <div className="absolute top-3 left-3 z-20 flex items-center gap-2 bg-amber-500/95 text-slate-950 px-3 py-1 rounded-md text-xs font-bold shadow-md backdrop-blur-xs">
                <CameraIcon className="w-3.5 h-3.5" />
                <span>Modo Captura / Arquivo (Stream DER Offline)</span>
              </div>

              <div className="absolute top-3 right-3 z-20 flex items-center gap-2">
                <button
                  onClick={tentarReconectarAoVivo}
                  className="flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white px-2.5 py-1 rounded-md text-[11px] font-semibold transition-colors cursor-pointer shadow-sm"
                  title="Tentar reconectar stream ao vivo"
                >
                  <Zap className="w-3 h-3" />
                  <span>Tentar Ao Vivo</span>
                </button>
              </div>

              {/* Imagem da Captura Real com cache-busting */}
              <img
                src={`${fallbackCapture.image_url}?t=${lastFetchTime}`}
                alt={`Última captura da ${fallbackCapture.nome_camera}`}
                className="w-full h-full object-contain"
              />
            </div>
          ) : (
            <div className="text-center p-8 max-w-md animate-fade-in">
              <div className="w-16 h-16 rounded-2xl bg-slate-800/60 border border-slate-700/80 flex items-center justify-center mx-auto mb-4 text-slate-400">
                <VideoOff className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">
                Stream temporariamente indisponível
              </h3>
              <p className="text-sm text-slate-400 leading-relaxed mb-4">
                A transmissão desta câmera do DER/SP não pôde ser iniciada no momento.
              </p>
              <button
                onClick={tentarReconectarAoVivo}
                className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-semibold transition-colors cursor-pointer"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Reconectar ao vivo</span>
              </button>
            </div>
          )
        )}
      </div>

      {/* Barra Inferior com Informações de Detecção e Atualização */}
      <div className="h-12 bg-[#09182C] px-5 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400 shrink-0">
        <div className="flex items-center gap-3">
          <span className="font-semibold text-slate-200">ID {camera.camera_der_id || camera.id}</span>
          <span className="text-slate-500">•</span>
          <span>{camera.rodovia} · km {camera.km} · {camera.municipio || 'DER/SP'}</span>
        </div>
        <div className="flex items-center gap-2">
          {isLiveActive && !streamError ? (
            <span className="inline-flex items-center gap-1.5 text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              Sinal Contínuo Real (25 FPS)
            </span>
          ) : fallbackCapture ? (
            <span>Última captura: {fallbackCapture.captured_at}</span>
          ) : (
            <span>Aguardando sinal...</span>
          )}
        </div>
      </div>
    </div>
  );
};
