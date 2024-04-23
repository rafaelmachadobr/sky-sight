# Sky Sight

## Sobre o projeto

Sky Sight é um projeto que tem como objetivo mostrar a previsão do tempo do parque Ibirapuera, em São Paulo, usando a API do [OpenWeather](https://openweathermap.org/api) e usando uma base de dados do clima da Vila Mariana, em São Paulo, que foi coletada por um sensor de temperatura e umidade.

## Estrutura do Pastas

```
sky-sight
├── backend  # Contém o código-fonte e configurações relacionadas ao backend do projeto, desenvolvido com Django.
│   ├── project  # Pasta principal do projeto Django.
│   ├── .env  # Arquivo de variáveis de ambiente para configurações locais do backend.
│   ├── .env.docker.example  # Arquivo de variáveis de ambiente para configurações do backend quando executado com Docker.
│   ├── .env.example  # Exemplo de arquivo de variáveis de ambiente para referência ao criar o arquivo .env.
│   ├── .gitignore  # Arquivo de configuração do Git para especificar arquivos e pastas a serem ignorados no versionamento.
│   ├── Dockerfile  # Arquivo de configuração do Docker para construir a imagem do contêiner do backend.
│   ├── entrypoint.sh  # Script de entrada do Docker para configurar o ambiente antes de iniciar o backend.
│   ├── manage.py  # Arquivo de configuração principal do Django para operações de gerenciamento do projeto.
│   ├── poetry.lock  # Arquivo gerado pelo Poetry para travar as versões das dependências Python.
│   └── pyproject.toml  # Arquivo de configuração do Poetry que especifica as dependências e configurações do projeto Python.
│
├── mobile  # Contém o código-fonte e configurações relacionadas ao aplicativo móvel, desenvolvido com Flutter.
│   ├── android  # Pasta contendo arquivos e configurações específicos para a plataforma Android.
│   ├── ios  # Pasta contendo arquivos e configurações específicos para a plataforma iOS.
│   ├── lib  # Pasta principal do código-fonte do aplicativo Flutter.
│   ├── test  # Pasta contendo os testes do aplicativo Flutter.
│   ├── .gitignore  # Arquivo de configuração do Git para especificar arquivos e pastas a serem ignorados no versionamento.
│   ├── .metadata  # Arquivo de metadados do Flutter para manter informações sobre o projeto.
│   ├── analysis_options.yaml  # Arquivo de configuração do Flutter para especificar opções de análise estática.
│   ├── pubspec.lock  # Arquivo gerado pelo Flutter para travar as versões das dependências do aplicativo Flutter.
│   ├── pubspec.yaml  # Arquivo de configuração do Flutter que especifica as dependências e configurações do projeto.
│   └── README.md  # Arquivo de documentação específico para o código-fonte do aplicativo móvel.
│
├── .gitignore  # Arquivo de configuração do Git para especificar arquivos e pastas a serem ignorados no versionamento global do projeto.
├── docker-compose.yml  # Arquivo de configuração do Docker Compose para definir serviços, redes e volumes para a aplicação Dockerizada.
└── README.md  # Arquivo de documentação principal que fornece uma visão geral do projeto, instruções de instalação e outras informações relevantes.

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
