from fastapi import HTTPException
from fastapi.responses import JSONResponse

EXPLICACOES_HTTP = {
    200: "Status 200 indica sucesso e os dados foram recebidos corretamente. (RFC 7231, seção 6.3.1)",
    201: "Status 201 é retornado quando um novo recurso é criado. (RFC 7231, seção 6.3.2)",
    204: "Status 204 indica sucesso, sem conteúdo a retornar. (RFC 7231, seção 6.3.5)",
    400: "Status 400 indica erro na requisição do cliente. (RFC 7231, seção 6.5.1)",
    401: "Status 401 indica que a requisição requer autenticação. (RFC 7235, seção 3.1)",
    403: "Status 403 é usado quando há autenticação, mas sem permissão. (RFC 7231, seção 6.5.3)",
    404: "Status 404 indica que o recurso solicitado não foi encontrado. (RFC 7231, seção 6.5.4)",
    405: "Status 405 ocorre quando um método HTTP não é suportado. (RFC 7231, seção 6.5.5)",
    409: "Status 409 indica conflito de estado entre a requisição e o recurso atual. (RFC 7231, seção 6.5.8)",
    422: "Status 422 indica erro de validação semântica. (RFC 4918, seção 11.2)",
    429: "Status 429 indica que o cliente enviou muitas requisições em um curto período. (RFC 6585, seção 4)",
    500: "Status 500 indica erro inesperado no servidor. (RFC 7231, seção 6.6.1)",
}

def resposta_sucesso(status: int, mensagem: str, extra: dict = None):
    conteudo = {
        "status": status,
        "mensagem": mensagem,
        "explicacao": EXPLICACOES_HTTP[status]
    }
    if extra:
        conteudo.update(extra)
    return JSONResponse(status_code=status, content=conteudo)

def resposta_erro(status: int, mensagem: str):
    raise HTTPException(
        status_code=status,
        detail={
            "status": status,
            "mensagem": mensagem,
            "explicacao": EXPLICACOES_HTTP[status]
        }
    )

def resposta_customizada(status: int, mensagem: str, extra: dict = None):
    conteudo = {
        "status": status,
        "mensagem": mensagem,
        "explicacao": EXPLICACOES_HTTP.get(status, "Explicação não definida para este status code.")
    }
    if extra:
        conteudo.update(extra)
    return JSONResponse(status_code=status, content=conteudo)
