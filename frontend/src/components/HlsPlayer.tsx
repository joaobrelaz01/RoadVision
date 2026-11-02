import React, { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';
import { VideoOff, RefreshCw } from 'lucide-react';
import { Camera } from '../types';

interface HlsPlayerProps {
  camera: Camera | null;
}

export const HlsPlayer: React.FC<HlsPlayerProps> = ({ camera }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [streamError, setStreamError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setStreamError(false);
    if (!camera || !camera.stream_url) {
      setStreamError(true);
      return;
    }

    const video = videoRef.current;
    if (!video) return;

    let hls: Hls | null = null;
    setIsLoading(true);

    if (Hls.isSupported()) {
      hls = new Hls({
        enableWorker: true,
        lowLatencyMode: true,
        backBufferLength: 90
      });

      hls.loadSource(camera.stream_url);
      hls.attachMedia(video);

      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        setIsLoading(false);
        video.play().catch(() => {
          // Autoplay prevenido pelo navegador
        });
      });

      hls.on(Hls.Events.ERROR, () => {
        setIsLoading(false);
        setStreamError(true);
      });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      // Suporte nativo Safari/iOS
      video.src = camera.stream_url;
      video.addEventListener('loadedmetadata', () => {
        setIsLoading(false);
        video.play().catch(() => {});
      });
      video.addEventListener('error', () => {
        setIsLoading(false);
        setStreamError(true);
      });
    } else {
      setIsLoading(false);
      setStreamError(true);
    }

    return () => {
      if (hls) {
        hls.destroy();
      }
    };
  }, [camera]);

  if (!camera) {
    return (
      <div className="bg-[#0B192C] text-white rounded-xl h-[480px] flex items-center justify-center p-8">
        <p className="text-slate-400">Selecione uma câmera para visualizar.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#0B192C] rounded-xl overflow-hidden shadow-lg border border-slate-800 flex flex-col h-[520px]">
      {/* Faixa decorativa Hazard Tape idêntica à imagem oficial Lovable */}
      <div className="h-2 w-full hazard-stripes shrink-0" />

      {/* Área do Player de Vídeo */}
      <div className="relative flex-1 bg-[#071322] flex items-center justify-center overflow-hidden">
        {streamError ? (
          <div className="text-center p-8 max-w-md animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-slate-800/60 border border-slate-700/80 flex items-center justify-center mx-auto mb-4 text-slate-400">
              <VideoOff className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">
              Stream não configurado
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Configure a URL do stream (HLS) desta câmera para exibir o vídeo.
            </p>
          </div>
        ) : (
          <>
            {isLoading && (
              <div className="absolute inset-0 flex items-center justify-center bg-[#071322]/80 z-10">
                <RefreshCw className="w-8 h-8 text-sky-400 animate-spin" />
              </div>
            )}
            <video
              ref={videoRef}
              className="w-full h-full object-contain"
              muted
              playsInline
              controls
            />
          </>
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
          <span>Última atualização: {camera.ultima_atualizacao || '—'}</span>
        </div>
      </div>
    </div>
  );
};
