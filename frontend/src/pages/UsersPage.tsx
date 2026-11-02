import React, { useEffect, useState } from 'react';
import { Shield, CheckCircle, AlertCircle, RefreshCw, Lock } from 'lucide-react';
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
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center font-bold">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold uppercase">Administradores</span>
              <span className="text-xl font-bold text-slate-900 block mt-0.5">
                {users.filter((u) => u.cargo === 'Administrador').length}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
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
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50/60 transition-colors">
                    <td className="py-4 px-6 font-semibold text-slate-900">{u.nome}</td>
                    <td className="py-4 px-6 text-slate-600 font-mono text-xs">{u.email}</td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
                        u.cargo === 'Administrador'
                          ? 'bg-purple-100 text-purple-700'
                          : 'bg-blue-100 text-blue-700'
                      }`}>
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
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Nota Informativa */}
      <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/70 text-xs text-slate-500 leading-relaxed">
        <strong>Gerenciamento de Identidade:</strong> Os usuários listados acima correspondem às contas reais existentes no <code>Supabase Auth</code> do projeto. Novos operadores e senhas devem ser provisionados através do console do Supabase ou convite administrativo para garantir segurança com tokens JWT.
      </div>
    </div>
  );
};
