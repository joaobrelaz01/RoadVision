import React, { useState } from 'react';
import {
  LayoutDashboard,
  Video,
  Route,
  Camera,
  BarChart3,
  FileText,
  Users,
  Settings,
  PanelLeft,
  Moon,
  Sun,
  Database,
  ChevronDown
} from 'lucide-react';

interface LayoutProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({
  activeTab,
  setActiveTab,
  children
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [userRole, setUserRole] = useState<'Administrador' | 'Operador' | 'Visualizador'>('Administrador');
  const [isDarkMode, setIsDarkMode] = useState(false);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'monitoramento', label: 'Monitoramento ao vivo', icon: Video },
    { id: 'rodovias', label: 'Rodovias', icon: Route },
    { id: 'cameras', label: 'Câmeras', icon: Camera },
    { id: 'estatisticas', label: 'Estatísticas', icon: BarChart3 },
    { id: 'relatorios', label: 'Relatórios', icon: FileText },
    { id: 'usuarios', label: 'Usuários', icon: Users },
    { id: 'configuracoes', label: 'Configurações', icon: Settings },
  ];

  return (
    <div className={`min-h-screen flex flex-col ${isDarkMode ? 'dark bg-slate-950 text-white' : 'bg-[#F8FAFC] text-slate-800'}`}>
      {/* 1. Barra Superior - Status de Conexão Real */}
      <div className="bg-emerald-50 border-b border-emerald-200 px-4 py-1.5 flex items-center justify-between text-xs text-emerald-800 font-medium z-50">
        <div className="flex items-center gap-2">
          <Database className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
          <span>
            <strong className="font-semibold">SISTEMA INTEGRADO AO SUPABASE</strong> — Exibindo registros reais de tráfego e câmeras do DER/SP.
          </span>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-[11px] text-emerald-700">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>PostgreSQL Realtime Conectado</span>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* 2. Barra Lateral (Sidebar) */}
        <aside
          className={`${
            sidebarOpen ? 'w-64' : 'w-20'
          } bg-[#0B192C] text-slate-300 transition-all duration-300 flex flex-col shrink-0 select-none z-40 border-r border-slate-800`}
        >
          {/* Logo RoadVision */}
          <div className="h-16 flex items-center px-5 border-b border-slate-800/80 gap-3">
            <div className="w-9 h-9 rounded-lg bg-[#EA580C] flex items-center justify-center text-white font-bold text-lg shadow-sm shrink-0">
              <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <rect width="18" height="14" x="3" y="5" rx="3" />
                <path d="M7 10h.01" />
                <path d="M12 12a3 3 0 1 0 0-4 3 3 0 0 0 0 4z" />
                <path d="M17 10h.01" />
              </svg>
            </div>
            {sidebarOpen && (
              <span className="font-bold text-xl text-white tracking-tight">
                Road<span className="text-white">Vision</span>
              </span>
            )}
          </div>

          {/* Seção Navegação */}
          <div className="px-4 pt-5 pb-2">
            {sidebarOpen && (
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-3 block mb-2">
                Navegação
              </span>
            )}
          </div>

          {/* Itens do Menu */}
          <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  title={!sidebarOpen ? item.label : undefined}
                  className={`w-full flex items-center gap-3.5 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-[#1C3558] text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-[#162842]'
                  }`}
                >
                  <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  {sidebarOpen && <span className="truncate">{item.label}</span>}
                </button>
              );
            })}
          </nav>

          {/* Rodapé da Sidebar */}
          {sidebarOpen && (
            <div className="p-4 border-t border-slate-800/80 text-xs text-slate-500">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                <span>YOLO11 & Oracle VM</span>
              </div>
            </div>
          )}
        </aside>

        {/* 3. Área de Conteúdo Principal */}
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          {/* Header Superior */}
          <header className="h-14 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 flex items-center justify-between shrink-0">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1.5 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
              title="Alternar menu lateral"
            >
              <PanelLeft className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <span>Visualizar como</span>
                <div className="relative">
                  <select
                    value={userRole}
                    onChange={(e) => setUserRole(e.target.value as any)}
                    className="appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md py-1.5 pl-3 pr-8 text-xs font-semibold text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-sky-500 cursor-pointer"
                  >
                    <option value="Administrador">Administrador</option>
                    <option value="Operador">Operador</option>
                    <option value="Visualizador">Visualizador</option>
                  </select>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                </div>
              </div>

              <button
                onClick={() => setIsDarkMode(!isDarkMode)}
                className="p-1.5 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                title="Alternar tema"
              >
                {isDarkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            </div>
          </header>

          {/* Conteúdo das Páginas */}
          <main className="flex-1 p-6 lg:p-8 max-w-7xl w-full mx-auto">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
};
