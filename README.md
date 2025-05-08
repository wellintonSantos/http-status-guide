# 🚦 HTTP Status Code Guide (com FastAPI)

Este projeto simula os principais **status HTTP** utilizados em APIs RESTful, com exemplos práticos, explicações baseadas nas RFCs e mensagens padronizadas para facilitar o aprendizado e a padronização entre times de desenvolvimento, QA e arquitetura.

---

## ✅ Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Python 3.10+

---

## 🚀 Como rodar localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/http-status-guide.git
cd http_status_guide
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Rode o servidor:
```bash
uvicorn main:app --reload
```

5. Acesse a documentação (Swagger):
```
http://localhost:8000/docs
```

---

## 📚 Endpoints disponíveis

| Método | Rota                       | Descrição                                      | Status esperados |
|--------|----------------------------|------------------------------------------------|-----------------|
| GET    | `/usuarios/123`            | Busca usuário válido                           | **200 OK**          |
| GET    | `/usuarios/999`            | Retorna erro de "não encontrado"               | **404 Not Found**   |
| POST   | `/usuarios`                | Criação de usuário fictício                    | **201 Created**     |
| DELETE | `/usuarios/123`            | Exclusão de usuário                            | **204 No Content**  |
| GET    | `/admin`                   | Autenticação com token                         | **401 Unauthorized / 403 Forbidden / 200 OK** |
| GET    | `/perfil`                  | Requer autenticação                            | **401 Unauthorized/ 200 OK**       |
| GET    | `/admin-area`             | Verifica permissão de acesso                   | **403 Forbidden / 200 OK**       |
| POST   | `/usuarios/registrar`      | Conflito ao tentar registrar e-mail repetido   | **409 Conflict**    |
| GET    | `/limite`                  | Simula excesso de requisições                  | **429 Too Many**    |
| POST   | `/badrequest`              | Requisição com campo obrigatório ausente       | **400 Bad Request** |
| POST   | `/validar`                 | Validação com Pydantic                         | **200 OK / 422 Unprocessable Entity**       |
| GET    | `/explicacoes`             | Retorna explicações de todos os códigos usados | **200 OK**          |

---

## 🧪 Como testar a API

### ✅ Swagger UI
Você pode acessar a interface interativa automática gerada pelo FastAPI acessando:

```
http://localhost:8000/docs
```

Lá você pode executar requisições, visualizar os parâmetros, corpos de requisição e os exemplos de retorno para todos os endpoints disponíveis. Super útil para aprender ou testar rapidamente.

---

### ✅ Testes via `curl` (linha de comando)
Caso prefira testar via terminal ou automações, aqui estão alguns exemplos:

```bash
# ✅ Sucesso (200)
curl -X GET http://localhost:8000/usuarios/123

# ❌ Não encontrado (404)
curl -X GET http://localhost:8000/usuarios/999

# ✅ Criação (201)
curl -X POST http://localhost:8000/usuarios

# ❌ Requisição malformada (400)
curl -X POST http://localhost:8000/badrequest -H "Content-Type: application/json" -d '{}'

# ❌ Sem autenticação (401)
curl -X GET http://localhost:8000/perfil

# ✅ Acesso autorizado (200)
curl -H "Authorization: Bearer QSByZXNwb3N0YSDDqTogNDI=" http://localhost:8000/admin

# ❌ Acesso negado (403)
curl -H "Authorization: Bearer usuario_comum" http://localhost:8000/admin

# ❌ Conflito (409)
curl -X POST http://localhost:8000/usuarios/registrar -H "Content-Type: application/json" -d '{"email":"wellinton@email.com"}'

# ❌ Muitas requisições (429)
curl -X GET http://localhost:8000/limite
```

---

## 💡 Objetivo

O projeto busca **educar, padronizar e facilitar a compreensão dos principais status HTTP** utilizados no desenvolvimento de APIs REST. Com respostas explicativas e estrutura padronizada, ele pode servir como referência para desenvolvedores, QAs, arquitetos e squads ágeis.

---

## ✨ Autor

Desenvolvido com 💙 por Wellinton.