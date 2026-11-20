import React, { useEffect, useState } from 'react';
import { Shield, CheckCircle, AlertCircle, RefreshCw, Lock, Crown, ShieldCheck } from 'lucide-react';
import { fetchUsers } from '../services/api';
import { UserProfile } from '../types';

export const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const carregarUsuarios = () => {
    setLoading(true);
    setErrorMessage(null);
    fetchUsers()
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        setErrorMessage(err.message || 'Erro ao carregar usuários.');
        setLoading(false);
      });
  };

  useEffect(() => {
    carregarUsuarios();
  }, []);

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight">
            Usuários
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Contas de operadores e administradores cadastradas no serviço oficial Supabase Auth.
          </p>
        </div>

        <button
          onClick={carregarUsuarios}
          className="self-start sm:self-auto inline-flex items-center gap-2 px-3.5 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-sm font-semibold shadow-2xs transition-colors cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Sincronizar Supabase Auth</span>
        </button>
      </div>

      {errorMessage && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 text-rose-700 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 shrink-0 text-rose-500" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Cards de Resumo de Permissões */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card Operador Master */}
        <div className="bg-gradient-to-br from-amber-50 to-orange-50/40 border border-amber-200/90 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-500 text-white flex items-center justify-center font-bold shadow-xs">
              <Crown className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs text-amber-800 font-bold uppercase tracking-wider">Operador Master</span>
              <span className="text-xl font-bold text-slate-900 block mt-0.5">
                {users.filter((u) => u.cargo === 'Operador Master' || u.is_master).length}
              </span>
            </div>
          </div>
        </div>

        {/* Card Administradores */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold uppercase">Administradores</span>
              <span className="text-xl font-bold text-slate-900 block mt-0.5">
                {users.filter((u) => u.cargo === 'Administrador').length}
              </span>
            </div>
          </div>
        </div>

        {/* Card Operadores */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold uppercase">Operadores</span>
              <span className="text-xl font-bold text-slate-900 block mt-0.5">
                {users.filter((u) => u.cargo === 'Operador').length}
              </span>
            </div>
          </div>
        </div>

        {/* Card Total */}
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center font-bold">
              <Lock className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold uppercase">Total no Supabase</span>
              <span className="text-xl font-bold text-slate-900 block mt-0.5">
                {users.length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Tabela de Usuários Reais */}
      <div className="bg-white border border-slate-200/80 rounded-xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center p-12 text-slate-400 gap-2">
            <RefreshCw className="w-5 h-5 animate-spin text-sky-600" />
            <span>Consultando contas no Supabase Auth...</span>
          </div>
        ) : users.length === 0 ? (
          <div className="p-12 text-center text-slate-400">
            Nenhum usuário cadastrado no Supabase Auth.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50/70 border-b border-slate-100 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-6">NOME</th>
                  <th className="py-3 px-6">EMAIL (SUPABASE AUTH)</th>
                  <th className="py-3 px-6">PERFIL</th>
                  <th className="py-3 px-6">STATUS</th>
                  <th className="py-3 px-6">DATA DE CADASTRO</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => {
                  const isMasterUser = u.cargo === 'Operador Master' || u.is_master;
                  return (
                    <tr
                      key={u.id}
                      className={`transition-colors ${
                        isMasterUser ? 'bg-amber-50/30 hover:bg-amber-50/50' : 'hover:bg-slate-50/60'
                      }`}
                    >
                      <td className="py-4 px-6 font-semibold text-slate-900 flex items-center gap-2">
                        {isMasterUser && <Crown className="w-4 h-4 text-amber-500 shrink-0" />}
                        <span>{u.nome}</span>
                      </td>
                      <td className="py-4 px-6 text-slate-600 font-mono text-xs">{u.email}</td>
                      <td className="py-4 px-6">
                        <span
                          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
                            isMasterUser
                              ? 'bg-amber-100 text-amber-800 border border-amber-300 shadow-2xs'
                              : u.cargo === 'Administrador'
                              ? 'bg-purple-100 text-purple-700'
                              : 'bg-blue-100 text-blue-700'
                          }`}
                        >
                          {u.cargo}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700">
                          <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                          {u.status}
                        </span>
                      </td>
                      <td className="py-4 px-6 text-slate-500 text-xs">{u.criado_em}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Nota Informativa com Política do Operador Master */}
      <div className="p-4 bg-gradient-to-r from-amber-50/60 via-slate-50 to-slate-50 rounded-xl border border-amber-200/60 text-xs text-slate-600 leading-relaxed space-y-1">
        <div className="font-bold text-slate-800 flex items-center gap-1.5">
          <Crown className="w-4 h-4 text-amber-600" />
          <span>Controle de Acesso & Operador Master:</span>
        </div>
        <p>
          O usuário <strong>João Brelaz</strong> (<code>joao.brelaz@uni9.edu.br</code>) detém o cargo de <strong>Operador Master</strong> com acesso irrestrito a todas as rodovias, telemetrias, inteligência analítica e gestão de usuários. Conforme as regras de segurança do RoadVision, a conta master possui imunidade permanente e não pode ser rebaixada ou excluída por outros administradores.
        </p>
      </div>
    </div>
  );
};
};
