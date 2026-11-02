import React, { useEffect, useState } from 'react';
import { Download, FileSpreadsheet, FileText as FilePdfIcon, Filter, RefreshCw, AlertCircle } from 'lucide-react';
import { fetchReports, fetchCameras } from '../services/api';
import { ReportItem, Camera } from '../types';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as XLSX from 'xlsx';

export const ReportsPage: React.FC = () => {
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [cameras, setCameras] = useState<Camera[]>([]);
  
  // Datas padrão: últimos 7 dias até hoje
  const hoje = new Date().toISOString().split('T')[0];
  const seteDiasAtras = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  const [dataDe, setDataDe] = useState(seteDiasAtras);
  const [dataAte, setDataAte] = useState(hoje);
  const [selectedCamera, setSelectedCamera] = useState('Todas');
  const [selectedSentido, setSelectedSentido] = useState('Todos');

  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchCameras()
      .then((data) => setCameras(data))
      .catch((e) => console.warn('Erro ao listar câmeras:', e));
  }, []);

  const carregarRelatorios = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchReports({
      de: dataDe,
      ate: dataAte,
      camera_id: selectedCamera,
      sentido: selectedSentido
    })
      .then((data) => {
        setReports(data.registros || []);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Erro ao carregar relatórios.');
        setLoading(false);
      });
  };

  useEffect(() => {
    carregarRelatorios();
  }, []);

  const exportToExcel = () => {
    if (reports.length === 0) {
      alert('Não há registros para exportar com os filtros atuais.');
      return;
    }

    const ws = XLSX.utils.json_to_sheet(
      reports.map((r) => ({
        ID: r.id,
        'Data e Hora': r.data_hora,
        Câmera: r.camera || r.camera_id,
        Sentido: r.sentido,
        Carros: r.carros,
        Motos: r.motos,
        Ônibus: r.onibus,
        Caminhões: r.caminhoes,
        Total: r.total
      }))
    );
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Relatório RoadVision Real');
    XLSX.writeFile(wb, `relatorio_roadvision_${dataDe}_a_${dataAte}.xlsx`);
  };

  const exportToPDF = () => {
    if (reports.length === 0) {
      alert('Não há registros para exportar com os filtros atuais.');
      return;
    }

    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text('Relatório Oficial de Tráfego — RoadVision', 14, 18);
    doc.setFontSize(10);
    doc.text(`Período: ${dataDe} até ${dataAte} | Sentido: ${selectedSentido} | Registros: ${reports.length}`, 14, 25);

    const tableData = reports.map((r) => [
      r.data_hora,
      r.camera || r.camera_id || 'SP-055',
      r.sentido,
      r.carros,
      r.motos,
      r.onibus,
      r.caminhoes,
      r.total
    ]);

    autoTable(doc, {
      startY: 32,
      head: [['Data/Hora', 'Câmera', 'Sentido', 'Carros', 'Motos', 'Ônibus', 'Caminhões', 'Total']],
      body: tableData,
      theme: 'grid',
      headStyles: { fillColor: [11, 25, 44] }
    });

    doc.save(`relatorio_roadvision_${dataDe}_a_${dataAte}.pdf`);
  };

  const totaisGerais = reports.reduce(
    (acc, r) => ({
      carros: acc.carros + r.carros,
      motos: acc.motos + r.motos,
      onibus: acc.onibus + r.onibus,
      caminhoes: acc.caminhoes + r.caminhoes,
      total: acc.total + r.total,
    }),
    { carros: 0, motos: 0, onibus: 0, caminhoes: 0, total: 0 }
  );

  return (
    <div className="space-y-6">
      {/* Título e Botões de Exportação */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
            Relatórios
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Consultas históricas reais da tabela contagens_por_sentido no Supabase com exportação para Excel e PDF.
          </p>
        </div>

        <div className="flex items-center gap-2.5 self-start sm:self-auto">
          <button
            onClick={exportToExcel}
            className="inline-flex items-center gap-2 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm font-semibold shadow-sm transition-colors cursor-pointer"
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Excel (.xlsx)</span>
          </button>
          <button
            onClick={exportToPDF}
            className="inline-flex items-center gap-2 px-3.5 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-semibold shadow-sm transition-colors cursor-pointer"
          >
            <FilePdfIcon className="w-4 h-4" />
            <span>PDF</span>
          </button>
        </div>
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
            <label className="text-xs font-semibold text-slate-500 block mb-1.5">Sentido de Deslocamento</label>
            <select
              value={selectedSentido}
              onChange={(e) => setSelectedSentido(e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 cursor-pointer"
            >
              <option value="Todos">Todos os Sentidos</option>
              <option value="Maranduba">Sentido Maranduba</option>
              <option value="Ubatuba">Sentido Ubatuba</option>
            </select>
          </div>

          <div>
            <button
              onClick={carregarRelatorios}
              disabled={loading}
              className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-sm font-semibold shadow-sm transition-colors cursor-pointer disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Filter className="w-4 h-4" />}
              <span>Consultar</span>
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

      {/* Cards de Resumo dos Registros */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm">
          <span className="text-xs text-slate-500 uppercase font-semibold">Total Geral</span>
          <span className="text-xl font-bold text-slate-900 block mt-1">{totaisGerais.total.toLocaleString('pt-BR')}</span>
        </div>
        <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm">
          <span className="text-xs text-sky-600 uppercase font-semibold">Carros</span>
          <span className="text-xl font-bold text-slate-900 block mt-1">{totaisGerais.carros.toLocaleString('pt-BR')}</span>
        </div>
        <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm">
          <span className="text-xs text-orange-600 uppercase font-semibold">Motos</span>
          <span className="text-xl font-bold text-slate-900 block mt-1">{totaisGerais.motos.toLocaleString('pt-BR')}</span>
        </div>
        <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm">
          <span className="text-xs text-cyan-600 uppercase font-semibold">Ônibus</span>
          <span className="text-xl font-bold text-slate-900 block mt-1">{totaisGerais.onibus.toLocaleString('pt-BR')}</span>
        </div>
        <div className="bg-white border border-slate-200/80 rounded-xl p-4 shadow-sm">
          <span className="text-xs text-slate-800 uppercase font-semibold">Caminhões</span>
          <span className="text-xl font-bold text-slate-900 block mt-1">{totaisGerais.caminhoes.toLocaleString('pt-BR')}</span>
        </div>
      </div>

      {/* Tabela de Relatório */}
      <div className="bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-slate-400 gap-2">
            <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
            <span>Consultando registros reais no Supabase...</span>
          </div>
        ) : reports.length === 0 ? (
          <div className="p-12 text-center text-slate-400">
            <p className="text-base font-semibold text-slate-600">Nenhum registro encontrado</p>
            <p className="text-xs text-slate-400 mt-1">Não foram encontradas contagens para os filtros e período selecionados.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50/70 border-b border-slate-100 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-6">DATA E HORA</th>
                  <th className="py-3 px-6">CÂMERA</th>
                  <th className="py-3 px-6">SENTIDO</th>
                  <th className="py-3 px-6">CARROS</th>
                  <th className="py-3 px-6">MOTOS</th>
                  <th className="py-3 px-6">ÔNIBUS</th>
                  <th className="py-3 px-6">CAMINHÕES</th>
                  <th className="py-3 px-6">TOTAL</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {reports.map((row) => (
                  <tr key={row.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-4 px-6 text-slate-700 font-mono text-xs">{row.data_hora}</td>
                    <td className="py-4 px-6 font-semibold text-slate-800">{row.camera || row.camera_id}</td>
                    <td className="py-4 px-6">
                      <span className={`inline-block px-2.5 py-0.5 rounded text-xs font-semibold ${
                        row.sentido === 'Ubatuba' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {row.sentido}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-slate-700">{row.carros}</td>
                    <td className="py-4 px-6 text-slate-700">{row.motos}</td>
                    <td className="py-4 px-6 text-slate-700">{row.onibus}</td>
                    <td className="py-4 px-6 text-slate-700">{row.caminhoes}</td>
                    <td className="py-4 px-6 font-bold text-slate-900">{row.total}</td>
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
