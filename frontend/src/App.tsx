import React, { useState, useEffect } from 'react';
import { Layout } from './components/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { LiveMonitorPage } from './pages/LiveMonitorPage';
import { HighwaysPage } from './pages/HighwaysPage';
import { CamerasPage } from './pages/CamerasPage';
import { StatisticsPage } from './pages/StatisticsPage';
import { ReportsPage } from './pages/ReportsPage';
import { UsersPage } from './pages/UsersPage';
import { SettingsPage } from './pages/SettingsPage';
import { subscribeToRealtimeCounts } from './services/supabase';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('dashboard');

  useEffect(() => {
    // Subscreve a eventos em tempo real do Supabase quando novos registros forem salvos
    const unsubscribe = subscribeToRealtimeCounts((newCount) => {
      console.log('[RoadVision App] Atualização em tempo real recebida do YOLO:', newCount);
    });

    return () => {
      if (unsubscribe) unsubscribe();
    };
  }, []);

  const renderActivePage = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardPage />;
      case 'monitoramento':
        return <LiveMonitorPage />;
      case 'rodovias':
        return <HighwaysPage />;
      case 'cameras':
        return <CamerasPage />;
      case 'estatisticas':
        return <StatisticsPage />;
      case 'relatorios':
        return <ReportsPage />;
      case 'usuarios':
        return <UsersPage />;
      case 'configuracoes':
        return <SettingsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <Layout activeTab={activeTab} setActiveTab={setActiveTab}>
      {renderActivePage()}
    </Layout>
  );
};

export default App;
