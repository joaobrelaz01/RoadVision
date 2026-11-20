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
    cargo: str  # Operador Master, Administrador, Operador, Visualizador
    status: str  # Ativo, Inativo
    criado_em: str
    is_master: Optional[bool] = False

@router.post("/login")
def login(req: LoginRequest):
    """
    Autentica o usuário de verdade via Supabase Auth.
    Identifica papéis reais: Operador Master (João Brelaz), Administrador e Operador.
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
            email = (res.user.email or "").strip().lower()
            app_meta = getattr(res.user, 'app_metadata', {}) or {}
            user_meta = getattr(res.user, 'user_metadata', {}) or {}

            is_master = (
                email == "joao.brelaz@uni9.edu.br" or
                app_meta.get("is_master") is True or
                app_meta.get("role") == "master" or
                user_meta.get("is_master") is True
            )

            if is_master:
                cargo = "Operador Master"
                nome = user_meta.get("nome", "João Brelaz")
            elif (
                app_meta.get("role") == "admin" or
                user_meta.get("role") == "admin" or
                email == "joao.santossilva@uni9.edu.br"
            ):
                cargo = "Administrador"
                nome = user_meta.get("nome", "João Santossilva")
            else:
                cargo = user_meta.get("cargo", "Operador")
                nome = user_meta.get("nome", email.split("@")[0].replace(".", " ").title())

            return {
                "token": res.session.access_token if res.session else "token-auth",
                "user": {
                    "id": res.user.id,
                    "nome": nome,
                    "email": res.user.email,
                    "cargo": cargo,
                    "is_master": is_master,
                    "status": "Ativo",
                    "criado_em": res.user.created_at[:10] if res.user.created_at else "—"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="E-mail ou senha incorretos no Supabase Auth")
    except HTTPException:
        raise
    except Exception as e:
        err_msg = str(e)
        if "Invalid login credentials" in err_msg:
            raise HTTPException(status_code=401, detail="Credenciais inválidas no Supabase Auth")
        raise HTTPException(status_code=400, detail=f"Falha na autenticação: {err_msg}")

@router.get("/usuarios", response_model=List[UserProfile])
def listar_usuarios():
    """
    Retorna os usuários REAIS cadastrados no Supabase Auth.
    Garante o reconhecimento de João Brelaz como Operador Master e preserva os demais.
    """
    client = get_supabase()
    if not client:
        return []

    usuarios_reais: List[UserProfile] = []
    try:
        users_resp = client.auth.admin.list_users()
        for u in users_resp:
            email = (u.email or "").strip().lower()
            app_meta = getattr(u, 'app_metadata', {}) or {}
            user_meta = getattr(u, 'user_metadata', {}) or {}

            is_master = (
                email == "joao.brelaz@uni9.edu.br" or
                app_meta.get("is_master") is True or
                app_meta.get("role") == "master" or
                user_meta.get("is_master") is True or
                user_meta.get("role") == "master"
            )

            if is_master:
                cargo = "Operador Master"
                nome = user_meta.get("nome", "João Brelaz")
            elif (
                app_meta.get("role") == "admin" or
                user_meta.get("role") == "admin" or
                email == "joao.santossilva@uni9.edu.br"
            ):
                cargo = "Administrador"
                nome = user_meta.get("nome", "João Santossilva")
            else:
                cargo = user_meta.get("cargo", "Operador")
                nome = user_meta.get("nome", email.split("@")[0].replace(".", " ").title())

            dt_criacao = str(u.created_at)[:10] if u.created_at else datetime.now().strftime("%Y-%m-%d")

            usuarios_reais.append(UserProfile(
                id=str(u.id),
                nome=nome,
                email=u.email,
                cargo=cargo,
                is_master=is_master,
                status="Ativo",
                criado_em=dt_criacao
            ))
    except Exception as e:
        print(f"[Auth] Erro ao listar usuários reais do Supabase: {e}")

    # Ordena com Operador Master em primeiro lugar, seguido por Administradores
    ordem_cargos = {"Operador Master": 0, "Administrador": 1, "Operador": 2, "Visualizador": 3}
    usuarios_reais.sort(key=lambda x: ordem_cargos.get(x.cargo, 9))

    return usuarios_reais

@router.delete("/usuarios/{user_id}")
def excluir_usuario(user_id: str):
    """
    Exclui um usuário do Supabase Auth.
    Impede estritamente a exclusão do Operador Master.
    """
    client = get_supabase()
    if not client:
        raise HTTPException(status_code=503, detail="Banco de dados Supabase indisponível")

    try:
        user_res = client.auth.admin.get_user_by_id(user_id)
        if user_res and user_res.user:
            u_email = (user_res.user.email or "").lower()
            if u_email == "joao.brelaz@uni9.edu.br" or user_res.user.app_metadata.get("is_master"):
                raise HTTPException(status_code=403, detail="O Operador Master possui imunidade permanente e não pode ser excluído.")
        client.auth.admin.delete_user(user_id)
        return {"mensagem": "Usuário excluído com sucesso do Supabase Auth."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

