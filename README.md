# sky-sight

# Pré requisitos

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

# Instalação

1. Clone o repositório

```bash
git clone git@github.com:rafaelmachadobr/sky-sight.git
```

2. Entre na pasta do projeto

```bash
cd sky-sight
```

3. Altere a branch para `develop`

```bash
git checkout develop
```

4. Crie o arquivo `.env` com base no arquivo `.env.example`

```bash
cp .env.example .env
```

## Backend

Entre na pasta do backend

```bash
cd backend
```

Instale as dependências

```bash
poetry install
```

Crie o banco de dados

```bash
poetry run python manage.py migrate
```

Crie o super usuário

```bash
poetry run python manage.py createsuperuser
```

Inicie o servidor

```bash
poetry run python manage.py runserver
```
