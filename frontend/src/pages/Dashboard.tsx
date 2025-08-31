import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  UsersIcon, 
  TruckIcon, 
  CalendarIcon, 
  CurrencyEuroIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  EyeIcon,
  PlusIcon,
  DocumentTextIcon,
  ChartBarIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline';

interface DashboardStats {
  totalCustomers: number;
  totalVehicles: number;
  todayAppointments: number;
  monthlyRevenue: number;
  activeCheckins: number;
  completedServices: number;
  pendingInvoices: number;
  aiDetections: number;
}

interface ActivityItem {
  icon: React.ComponentType<any>;
  title: string;
  time: string;
  color: string;
  bgColor: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalCustomers: 0,
    totalVehicles: 0,
    todayAppointments: 0,
    monthlyRevenue: 0,
    activeCheckins: 0,
    completedServices: 0,
    pendingInvoices: 0,
    aiDetections: 0,
  });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Mock data for recent activity
  const recentActivity: ActivityItem[] = [
    {
      icon: CheckCircleIcon,
      title: "Servizio completato - Cambio olio Fiat 500",
      time: "2 ore fa",
      color: "text-green-600",
      bgColor: "bg-green-100"
    },
    {
      icon: UsersIcon,
      title: "Nuovo cliente registrato - Mario Rossi",
      time: "4 ore fa",
      color: "text-blue-600",
      bgColor: "bg-blue-100"
    },
    {
      icon: CalendarIcon,
      title: "Appuntamento confermato - Revisione BMW X3",
      time: "6 ore fa",
      color: "text-purple-600",
      bgColor: "bg-purple-100"
    },
    {
      icon: TruckIcon,
      title: "Check-in automatico - Veicolo EF456GH",
      time: "8 ore fa",
      color: "text-orange-600",
      bgColor: "bg-orange-100"
    }
  ];

  useEffect(() => {
    // Simulate loading data
    setTimeout(() => {
      setStats({
        totalCustomers: 1247,
        totalVehicles: 1893,
        todayAppointments: 23,
        monthlyRevenue: 45600,
        activeCheckins: 8,
        completedServices: 156,
        pendingInvoices: 12,
        aiDetections: 89,
      });
      setLoading(false);
    }, 1000);
  }, []);

  const StatCard = ({ title, value, icon: Icon, color, change, subtitle }: any) => (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-300 hover:-translate-y-1">
      <div className="flex items-center justify-between mb-4">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">
            {typeof value === 'number' && value >= 1000 ? (value / 1000).toFixed(1) + 'k' : value}
          </p>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`w-12 h-12 ${color} rounded-xl flex items-center justify-center`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
      
      {change !== undefined && (
        <div className="flex items-center space-x-2">
          {change > 0 ? (
            <CheckCircleIcon className="w-4 h-4 text-green-500" />
          ) : (
            <ExclamationTriangleIcon className="w-4 h-4 text-red-500" />
          )}
          <span className={`text-sm font-medium ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
            {change > 0 ? '+' : ''}{change}% rispetto al mese scorso
          </span>
        </div>
      )}
    </div>
  );

  const QuickActionCard = ({ title, description, icon: Icon, color, onClick }: any) => (
    <div 
      className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 cursor-pointer hover:shadow-md transition-all duration-300 hover:-translate-y-1 text-center"
      onClick={onClick}
    >
      <div className={`w-12 h-12 ${color} rounded-xl flex items-center justify-center mx-auto mb-4`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">
          Panoramica completa dell'officina • Ultimo aggiornamento: {new Date().toLocaleString('it-IT')}
        </p>
      </div>

      {/* Main Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Clienti Totali"
          value={stats.totalCustomers}
          icon={UsersIcon}
          color="bg-blue-500"
          change={12}
          subtitle="Clienti registrati"
        />
        <StatCard
          title="Veicoli Registrati"
          value={stats.totalVehicles}
          icon={TruckIcon}
          color="bg-green-500"
          change={8}
          subtitle="Veicoli in database"
        />
        <StatCard
          title="Appuntamenti Oggi"
          value={stats.todayAppointments}
          icon={CalendarIcon}
          color="bg-purple-500"
          change={-3}
          subtitle="Appuntamenti programmati"
        />
        <StatCard
          title="Fatturato Mensile"
          value={`€${stats.monthlyRevenue.toLocaleString()}`}
          icon={CurrencyEuroIcon}
          color="bg-orange-500"
          change={15}
          subtitle="Ricavi del mese"
        />
      </div>

      {/* Secondary Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Check-in Attivi"
          value={stats.activeCheckins}
          icon={ClockIcon}
          color="bg-indigo-500"
          subtitle="Veicoli in officina"
        />
        <StatCard
          title="Servizi Completati"
          value={stats.completedServices}
          icon={CheckCircleIcon}
          color="bg-emerald-500"
          change={22}
          subtitle="Questo mese"
        />
        <StatCard
          title="Fatture in Sospeso"
          value={stats.pendingInvoices}
          icon={ExclamationTriangleIcon}
          color="bg-red-500"
          change={-5}
          subtitle="Da emettere"
        />
        <StatCard
          title="Riconoscimenti AI"
          value={stats.aiDetections}
          icon={EyeIcon}
          color="bg-cyan-500"
          change={18}
          subtitle="Targhe rilevate"
        />
      </div>

      {/* Quick Actions and Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Azioni Rapide</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <QuickActionCard
                title="Nuovo Appuntamento"
                description="Pianifica un nuovo appuntamento"
                icon={CalendarIcon}
                color="bg-blue-500"
                onClick={() => navigate('/appointments')}
              />
              <QuickActionCard
                title="Registra Cliente"
                description="Aggiungi un nuovo cliente"
                icon={UsersIcon}
                color="bg-green-500"
                onClick={() => navigate('/customers')}
              />
              <QuickActionCard
                title="Check-in Veicolo"
                description="Registra arrivo veicolo"
                icon={TruckIcon}
                color="bg-purple-500"
                onClick={() => navigate('/vehicles')}
              />
              <QuickActionCard
                title="Genera Fattura"
                description="Crea nuova fattura"
                icon={DocumentTextIcon}
                color="bg-orange-500"
                onClick={() => navigate('/invoices')}
              />
              <QuickActionCard
                title="Analytics"
                description="Visualizza statistiche"
                icon={ChartBarIcon}
                color="bg-indigo-500"
                onClick={() => navigate('/analytics')}
              />
              <QuickActionCard
                title="Impostazioni"
                description="Configura sistema"
                icon={Cog6ToothIcon}
                color="bg-gray-500"
                onClick={() => navigate('/settings')}
              />
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Attività Recenti</h2>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => {
                const Icon = activity.icon;
                return (
                  <div key={index} className="flex items-start space-x-3">
                    <div className={`w-8 h-8 ${activity.bgColor} rounded-lg flex items-center justify-center flex-shrink-0`}>
                      <Icon className={`w-4 h-4 ${activity.color}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 leading-tight">
                        {activity.title}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {activity.time}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
