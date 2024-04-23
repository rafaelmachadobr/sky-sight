# Sky Sight

## Sobre o projeto

Sky Sight é um projeto que tem como objetivo mostrar a previsão do tempo do parque Ibirapuera, em São Paulo, usando a API do [OpenWeather](https://openweathermap.org/api) e usando uma base de dados do clima da Vila Mariana, em São Paulo, que foi coletada por um sensor de temperatura e umidade.

## Estrutura do Pastas

```
sky-sight
├── backend  # Código-fonte e configurações do backend do projeto em Django.
│   ├── project  # Pasta principal do projeto Django.
│   ├── .env  # Variáveis de ambiente para configurações locais do backend.
│   ├── .env.docker.example  # Variáveis de ambiente para configurações do backend com Docker.
│   ├── .env.example  # Exemplo de variáveis de ambiente.
│   ├── .gitignore  # Configuração do Git para ignorar arquivos.
│   ├── Dockerfile  # Configuração do Docker para construir a imagem do backend.
│   ├── entrypoint.sh  # Script de entrada do Docker.
│   ├── manage.py  # Configuração principal do Django.
│   ├── poetry.lock  # Lockfile do Poetry para dependências Python.
│   └── pyproject.toml  # Configuração do Poetry para dependências do projeto Python.
│
├── mobile  # Código-fonte e configurações do aplicativo móvel em Flutter.
│   ├── android  # Arquivos específicos para Android.
│   ├── ios  # Arquivos específicos para iOS.
│   ├── lib  # Código-fonte principal.
│   ├── test  # Testes do aplicativo.
│   ├── .gitignore  # Configuração do Git para ignorar arquivos.
│   ├── .metadata  # Metadados do Flutter.
│   ├── analysis_options.yaml  # Opções de análise estática do Flutter.
│   ├── pubspec.lock  # Lockfile do Flutter para dependências.
│   ├── pubspec.yaml  # Configuração do Flutter para dependências do projeto.
│   └── README.md  # Documentação específica para o código-fonte do aplicativo móvel.
│
├── .gitignore  # Configuração do Git global.
├── docker-compose.yml  # Configuração do Docker Compose.
└── README.md  # Documentação principal do projeto.
```

## Tecnologias Utilizadas

### Backend

- [**Python**](https://www.python.org/)
- [**Django**](https://www.djangoproject.com/)
- [**Django Rest Framework**](https://www.django-rest-framework.org/)
- [**Poetry**](https://python-poetry.org/docs/)

### Mobile

- [**Dart**](https://dart.dev/)
- [**Flutter**](https://flutter.dev/)

### Banco de Dados

- [**SQLite**](https://www.sqlite.org/index.html)
- [**Postgres**](https://www.postgresql.org/)

### DevOps

- [**Git**](https://git-scm.com/downloads)
- [**Docker**](https://www.docker.com/)
- [**Docker Compose**](https://docs.docker.com/compose/install/)

### API Externa

- [**OpenWeather**](https://openweathermap.org/api)

## Pré requisitos

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Rodando Localmente

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

4. Crie o arquivo `.env` usando uma das opções abaixo

   4.1. Crie o arquivo `.env` com base no arquivo `.env.example` onde ele usar o sqlite como banco de dados e o backend será executado localmente

   ```bash
   cp .env.example .env
   ```

   4.2. Crie o arquivo `.env` com base no arquivo `.env.docker.example` onde ele usar o postgres como banco de dados e o backend será executado com Docker

   ```bash
   cp .env.docker.example .env
   ```

## Backend

### Pelo Poetry

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

## Pelo Docker

Entre na pasta do projeto

```bash
cd sky-sight
```

Inicie o docker

```bash
docker-compose up -d --build
```

Crie o banco de dados

```bash
docker-compose exec backend poetry run python manage.py migrate
```

Crie o super usuário

```bash
docker-compose exec backend poetry run python manage.py createsuperuser
```

## Mobile

Entre na pasta do mobile

```bash
cd mobile
```

Instale as dependências

```bash
flutter pub get
```

Inicie o aplicativo

```bash
flutter run
```

## Funcionalidades

- Em breve

## Desenvolvedores

- [Rafael Ferreira Machado](https://github.com/rafaelmachadobr)
- [Kayky Vasconcelos](https://github.com/kaykyvasconcelos)
- [Leonardo Arouche](https://github.com/LeoPDA)
- [Samara Marques](https://github.com/samrqs)
- [Thais](https://github.com/thaisisi)
