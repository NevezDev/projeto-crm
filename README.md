# Guia CRM

CRM full stack para organizar contatos, empresas, oportunidades de venda, tarefas e indicadores de pipeline. O projeto combina uma API REST em FastAPI com uma interface responsiva em HTML, CSS e JavaScript puro.

## Funcionalidades

- Cadastro e login com autenticação JWT.
- CRUD de contatos, empresas, negócios e tarefas.
- Atualização parcial e conclusão rápida de tarefas.
- Dashboard com contatos, oportunidades, receita e funil por etapa.
- Isolamento dos dados de cada usuário.
- Validação dos payloads com Pydantic.
- Documentação automática da API via Swagger em `/docs`.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- JWT com `python-jose`
- Passlib/bcrypt para hash de senhas
- SQLite para execução local rápida
- PostgreSQL opcional via `DATABASE_URL`
- HTML, CSS e JavaScript puro no frontend

## Como rodar localmente

1. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

```bash
copy .env.example .env
```

4. Inicie a API:

```bash
uvicorn main:app --reload
```

5. Abra `frontend.html` no navegador.

```text
frontend.html
```

A API ficará disponível em `http://127.0.0.1:8000`, e a documentação interativa em `http://127.0.0.1:8000/docs`.

## Testes

Os testes cobrem validação da autenticação, isolamento entre usuários, unicidade de empresas por usuário e atualização parcial de tarefas:

```bash
python -m unittest discover -s tests -v
```

## Configuração do frontend

Por padrão, o frontend usa `http://localhost:8000`. Em uma publicação estática, informe a API pelo parâmetro `api`:

```text
https://seu-usuario.github.io/projeto-crm/?api=https://sua-api.example.com
```

O endereço fica salvo no navegador. Também é possível defini-lo antes do script por `window.CRM_API_URL`.

## Banco de dados

Por padrão, o projeto usa SQLite local:

```env
DATABASE_URL=sqlite:///./crm.db
```

Para usar PostgreSQL, altere a variavel no `.env`:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

## Estrutura

```text
.
├── main.py
├── database.py
├── auth_utils.py
├── frontend.html
├── models/
├── routes/
├── schemas/
├── tests/
├── requirements.txt
└── .env.example
```

## Decisões técnicas

- API separada em models, schemas e rotas.
- Senhas armazenadas apenas como hash bcrypt.
- Segredos e conexão com banco definidos por variáveis de ambiente.
- Consultas sempre filtradas pelo usuário autenticado.
- Conteúdo dinâmico escapado no frontend para reduzir risco de XSS.
- SQLite no desenvolvimento e suporte a PostgreSQL em produção.

## Autor

Desenvolvido por [Sérgio Neves](https://github.com/NevezDev) como projeto de portfólio para demonstrar fundamentos de desenvolvimento full stack com Python.
