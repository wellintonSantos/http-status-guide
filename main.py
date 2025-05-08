from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException as FastAPIHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils import resposta_sucesso, resposta_erro, resposta_customizada, EXPLICACOES_HTTP

app = FastAPI(title="HTTP Status Code Guide")

# ================================
# MODELS
# ================================

class UsuarioInput(BaseModel):
    nome: str
    idade: int

# ================================
# ENDPOINTS
# ================================

@app.get(
    "/usuarios/{usuario_id}",
    tags=["Exemplos de chamadas HTTP"],
    summary="Buscar um usuário pelo ID",
    description="Retorna os dados de um usuário específico se o ID for válido. Caso contrário, retorna erro 404 com explicação."
)
def get_usuario(usuario_id: int):
    if usuario_id == 123:
        return resposta_sucesso(200, "Usuário encontrado com sucesso")
    else:
        return resposta_erro(404, "Usuário não encontrado")

@app.post(
    "/usuarios",
    tags=["Exemplos de chamadas HTTP"],
    summary="Criar um novo usuário fictício",
    description="Simula a criação de um recurso, retornando status 201 sem necessidade de payload."
)
def criar_usuario():
    return resposta_sucesso(201, "Usuário criado com sucesso")

@app.delete(
    "/usuarios/{usuario_id}",
    tags=["Exemplos de chamadas HTTP"],
    summary="Deletar um usuário",
    description="Simula a exclusão de um usuário retornando status 204. Nenhum conteúdo é retornado."
)
def deletar_usuario(usuario_id: int):
    status = 204
    return JSONResponse(
        status_code=status,
        content=None,
        headers={"X-Explicacao": EXPLICACOES_HTTP[status]}
    )

@app.get(
    "/admin",
    tags=["Exemplos de chamadas HTTP"],
    summary="Autenticação com token",
    description="Requer token via header Authorization. Retorna 200, 401 ou 403 dependendo do caso."
)
def acesso_admin(authorization: str = Header(None)):
    if authorization is None:
        return resposta_erro(401, "Token ausente")
    elif authorization != "Bearer QSByZXNwb3N0YSDDqTogNDI=":
        return resposta_erro(403, "Acesso negado")
    return resposta_sucesso(200, "Bem-vindo, admin")

@app.get(
    "/perfil",
    tags=["Exemplos de chamadas HTTP"],
    summary="Acessar o perfil do usuário autenticado",
    description="Retorna 200 se o token estiver presente, ou 401 se ausente."
)
def perfil(authorization: str = Header(None)):
    if not authorization:
        return resposta_erro(401, "Token de autenticação ausente")
    return resposta_sucesso(200, "Perfil acessado com sucesso")

@app.get(
    "/admin-area",
    tags=["Exemplos de chamadas HTTP"],
    summary="Acesso restrito à área administrativa",
    description="Apenas usuários com token específico têm permissão. Caso contrário, retorna 403."
)
def admin_area(authorization: str = Header(None)):
    if authorization != "Bearer admin123":
        return resposta_erro(403, "Você não tem permissão para acessar esta área")
    return resposta_sucesso(200, "Bem-vindo à área administrativa")

@app.post(
    "/usuarios/registrar",
    tags=["Exemplos de chamadas HTTP"],
    summary="Registrar um novo usuário",
    description="Simula registro com verificação de duplicidade. Retorna 409 se o e-mail já existir."
)
def registrar_usuario(dado: dict):
    if dado.get("email") == "wellinton@email.com":
        return resposta_customizada(409, "Este email já está cadastrado")
    return resposta_sucesso(201, "Usuário registrado com sucesso")

@app.get(
    "/limite",
    tags=["Exemplos de chamadas HTTP"],
    summary="Simular limite de requisições",
    description="Simula o erro 429 por excesso de requisições. Útil para testes de rate limiting."
)
def limite_de_requisicoes():
    return resposta_customizada(429, "Limite de requisições excedido")

@app.post(
    "/badrequest",
    tags=["Exemplos de chamadas HTTP"],
    summary="Simular uma requisição inválida",
    description="Retorna 400 se o campo obrigatório estiver ausente no corpo JSON."
)
def bad_request_simulado(dado: dict):
    if "nome" not in dado:
        return resposta_erro(400, "Campo 'nome' é obrigatório")
    return resposta_sucesso(200, "Requisição válida")

@app.post(
    "/validar",
    tags=["Exemplos de chamadas HTTP"],
    summary="Validar campos com Pydantic",
    description="Retorna 200 se os dados forem válidos, ou 422 em caso de erro de validação."
)
def validar_usuario(usuario: UsuarioInput):
    return resposta_sucesso(200, f"Usuário {usuario.nome} com {usuario.idade} anos recebido com sucesso!")

@app.get(
    "/explicacoes",
    tags=["Exemplos de chamadas HTTP"],
    summary="Listar todas as explicações dos códigos",
    description="Retorna um dicionário com todas as explicações padronizadas por status HTTP."
)
def explicacoes():
    return EXPLICACOES_HTTP

# ================================
# HANDLERS GLOBAIS
# ================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 405:
        return resposta_customizada(405, "Método não permitido para este endpoint")
    raise exc

@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
    return resposta_customizada(500, "Erro inesperado no servidor")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return resposta_customizada(422, "Erro de validação nos dados enviados", {"detalhes": exc.errors()})

@app.exception_handler(FastAPIHTTPException)
async def fastapi_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
