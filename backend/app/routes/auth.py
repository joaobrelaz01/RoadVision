from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.app.database.supabase_client import get_supabase

router = APIRouter(prefix="/api/auth", tags=["Autenticação e Usuários"])

class LoginRequest(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    id: str
    nome: str
    email: str
    cargo: str  # Administrador, Operador, Visualizador
    status: str  # Ativo, Inativo
    criado_em: str

@router.post("/login")
def login(req: LoginRequest):
    """
    Autentica o usuário de verdade via Supabase Auth.
    Não aceita logins fictícios.
    """
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=503, detail="Banco de dados Supabase indisponível")

    try:
        res = client.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        if res and res.user:
            return {
                "token": res.session.access_token if res.session else "token-auth",
                "user": {
                    "id": res.user.id,
                    "nome": res.user.email.split("@")[0].title(),
                    "email": res.user.email,
                    "cargo": "Administrador" if "admin" in res.user.email else "Operador",
                    "status": "Ativo",
                    "criado_em": res.user.created_at[:10] if res.user.created_at else "—"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="E-mail ou senha incorretos no Supabase Auth")
    except Exception as e:
        err_msg = str(e)
        if "Invalid login credentials" in err_msg:
            raise HTTPException(status_code=401, detail="Credenciais inválidas no Supabase Auth")
        raise HTTPException(status_code=400, detail=f"Falha na autenticação: {err_msg}")

@router.get("/usuarios", response_model=List[UserProfile])
def listar_usuarios():
    """
    Retorna os usuários REAIS cadastrados no Supabase Auth.
    Zero usuários inventados.
    """
    client = get_supabase()
    if not client:
        return []

    usuarios_reais: List[UserProfile] = []
    try:
        users_resp = client.auth.admin.list_users()
        for u in users_resp:
            email = u.email or "sem-email"
            nome_extraido = email.split("@")[0].replace(".", " ").title()
            
            # Determina o nível de acesso pelo papel ou e-mail
            cargo = "Administrador" if "joao" in email.lower() else "Operador"
            dt_criacao = str(u.created_at)[:10] if u.created_at else datetime.now().strftime("%Y-%m-%d")

            usuarios_reais.append(UserProfile(
                id=str(u.id),
                nome=nome_extraido,
                email=email,
                cargo=cargo,
                status="Ativo",
                criado_em=dt_criacao
            ))
    except Exception as e:
        print(f"[Auth] Erro ao listar usuários reais do Supabase: {e}")

    return usuarios_reais
