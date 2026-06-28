# Guia CRM

CRM full stack desenvolvido para organizar contatos, empresas, oportunidades de venda, tarefas e indicadores de pipeline.

O backend e toda a lógica da aplicação foram desenvolvidos por mim utilizando Python e FastAPI. A interface frontend foi criada com o auxílio do Claude, ferramenta de inteligência artificial da Anthropic.

## Funcionalidades

- Cadastro e login com autenticação JWT.
- CRUD de contatos, empresas, negócios e tarefas.
- Atualização e conclusão rápida de tarefas.
- Dashboard com contatos, oportunidades e receita em pipeline.
- Funil de vendas dividido por etapas.
- Isolamento dos dados por usuário.
- Validação dos dados com Pydantic.
- Documentação automática da API com Swagger.

## Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT com `python-jose`
- Passlib e bcrypt
- SQLite
- PostgreSQL opcional

### Frontend

- HTML
- CSS
- JavaScript
- Font Awesome
- Desenvolvimento realizado com auxílio do Claude

## Como executar localmente

1. Clone o repositório:

```bash
git clone https://github.com/NevezDev/projeto-crm.git
cd projeto-crm
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo de configuração:

```bash
copy .env.example .env
```

5. Inicie a API:

```bash
uvicorn main:app --reload
```

6. Abra o arquivo `frontend.html` no navegador.

A API estará disponível em `http://127.0.0.1:8000` e a documentação Swagger em `http://127.0.0.1:8000/docs`.

## Testes

Para executar os testes automatizados:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam:

- Validação do cadastro.
- Autenticação de usuários.
- Isolamento dos dados.
- Unicidade de empresas por usuário.
- Atualização parcial de tarefas.

## Configuração do frontend

Por padrão, o frontend utiliza a API disponível em `http://localhost:8000`.

Em uma publicação externa, a URL pode ser configurada pelo parâmetro `api`:

```text
https://seu-site.com/?api=https://sua-api.com
```

## Banco de dados

Por padrão, o projeto utiliza SQLite:

```env
DATABASE_URL=sqlite:///./crm.db
```

Para utilizar PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/banco
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

## Desenvolvimento e uso de inteligência artificial

O backend, incluindo arquitetura, regras de negócio, autenticação, banco de dados, endpoints e testes, foi desenvolvido por mim.

O frontend foi desenvolvido com o auxílio do Claude, utilizado como ferramenta de apoio na criação da interface, dos estilos e dos componentes visuais. A integração entre frontend e backend, assim como os ajustes e as validações finais, fizeram parte do desenvolvimento do projeto.

## Autor

Desenvolvido por [Sérgio Neves](https://github.com/NevezDev) como projeto de portfólio para demonstrar conhecimentos em desenvolvimento backend com Python e FastAPI.
