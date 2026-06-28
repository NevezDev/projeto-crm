# Guia CRM

Um CRM simples para organizar contatos, empresas, oportunidades de venda e tarefas em um só lugar.

Criei o backend com Python e FastAPI, cuidando da autenticação, do banco de dados, das regras da aplicação e dos testes. O frontend foi desenvolvido com o auxílio do Claude na criação da interface e dos componentes visuais.

## Funcionalidades

- Cadastro e login com JWT.
- Gerenciamento de contatos, empresas, negócios e tarefas.
- Funil de vendas e resumo do pipeline.
- Atualização e conclusão rápida de tarefas.
- Dados separados por usuário.
- Documentação interativa pelo Swagger.

## Tecnologias

O backend utiliza Python, FastAPI, SQLAlchemy, Pydantic e SQLite. Também há suporte a PostgreSQL pela variável `DATABASE_URL`.

O frontend foi feito com HTML, CSS, JavaScript e Font Awesome.

## Como executar

1. Crie e ative o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env`:

```bash
copy .env.example .env
```

4. Inicie a API:

```bash
uvicorn main:app --reload
```

5. Abra o arquivo `frontend.html` no navegador.

A API estará em `http://127.0.0.1:8000` e o Swagger em `http://127.0.0.1:8000/docs`.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes verificam autenticação, validação dos dados, isolamento entre usuários e atualização de tarefas.

## Configuração

O projeto usa SQLite por padrão:

```env
DATABASE_URL=sqlite:///./crm.db
```

Para usar PostgreSQL, altere a variável no `.env`:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/banco
```

O frontend procura a API em `http://localhost:8000`. Em outro ambiente, o endereço pode ser informado pelo parâmetro `api`:

```text
https://seu-site.com/?api=https://sua-api.com
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
└── tests/
```

## Sobre o desenvolvimento

O backend, a integração com o banco, as rotas, a autenticação e os testes foram desenvolvidos por mim. Usei o Claude como ferramenta de apoio no desenvolvimento visual do frontend.

## Autor

Desenvolvido por [Sérgio Neves](https://github.com/NevezDev).

## Licença

Distribuído sob a licença MIT. Consulte [LICENSE](LICENSE).
