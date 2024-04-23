# Sky Sight

## Sobre o projeto

Sky Sight é um projeto que tem como objetivo mostrar a previsão do tempo do parque Ibirapuera, em São Paulo, usando a API do [OpenWeather](https://openweathermap.org/api) e usando uma base de dados do clima da Vila Mariana, em São Paulo, que foi coletada por um sensor de temperatura e umidade.

## Estrutura do Pastas

```
sky-sight
├── backend # Pasta do backend (Django)
│   ├── project # Pasta do projeto
│   ├── .env # Arquivo de variáveis de ambiente
│   ├── .env.docker # Arquivo de variáveis de ambiente para o docker
│   ├── .env.example # Arquivo de variáveis de ambiente de exemplo
│   ├── .gitignore # Arquivo de configuração do git
│   ├── Dockerfile # Arquivo de configuração do docker
│   ├── entrypoint.sh # Arquivo de configuração do docker
│   ├── manage.py # Arquivo de configuração do django
│   ├── poetry.lock # Arquivo de configuração do poetry
│   └── pyproject.toml # Arquivo de configuração do poetry
│
├── mobile # Pasta do mobile (Flutter)
│   ├── android # Pasta do android
│   ├── ios # Pasta do ios
│   ├── lib # Pasta do código fonte
│   ├── test # Pasta de testes
│   ├── .gitignore # Arquivo de configuração do git
│   ├── .metadata # Arquivo de configuração do flutter
│   ├── analysis_options.yaml # Arquivo de configuração do flutter
│   ├── pubspec.lock # Arquivo de configuração do flutter
│   ├── pubspec.yaml # Arquivo de configuração do flutter
│   └── README.md # Arquivo de documentação
│
├── .gitignore # Arquivo de configuração do git
├── docker-compose.yml # Arquivo de configuração do docker
└── README.md # Arquivo de documentação
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

4.1. Crie o arquivo `.env` com base no arquivo `.env.example` onde ele usar o sqlite como banco de dados

```bash
cp .env.example .env
```

4.2. Crie o arquivo `.env` com base no arquivo `.env.docker.example` onde ele usa o postgres como banco de dados

```bash
cp .env.docker .env
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
