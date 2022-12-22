# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

- [Python](https://www.python.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [PostgresSQL:14 or Latest](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/downloads)

### Recommended

- [Visual Studio Code](https://code.visualstudio.com/Download) - IDE

<br>

# Project Structure

    .
    ├── venv                     - Python libs
    ├── _project                 - Global project settings
    ├── .github                  - Github Workflow Actions
    ├── addresses                - Model Address files
    ├── books                    - Model Book files
    ├── borroweds                - Model Borrowed files
    ├── extra_datas              - Model Extra_Data files
    ├── feed_back                - Model Feed_back files
    ├── genders                  - Model Gender files
    ├── pictures                 - Model Picture files
    ├── users                    - Model Users files
    ├── utils                    - Utils files
    ├── .coverage                - Coverage file
    ├── .coveragerc              - Tests coverage config file
    ├── .env                     - Environment variables
    ├── .env.example             - Environment variables example files
    ├── .gitignore               - Github ignore files config
    ├── docker-compose.yml       - Docker container config file
    ├── DockerFile               - Docker image config file
    ├── manage.py                - Django Utility file
    ├── requirements             - Dependencies file
    └── README.md                - Readme file from projet

## Installing

<br>

- **Clone repository**

```
git clone git@github.com:Projeto-final-M5/api.git
```

- **Copy the environment variables**

```
 cp .env.exemple .env
```

- **Write your environment variables**

```
    POSTGRES_DB='YourDatabaseName'
    POSTGRES_USER='YourDatabaseUser'
    POSTGRES_PASSWORD='YourUserPassword'
    SECRET_KEY='SetYourSecretKey'
    DB_HOST="db"
```

> - Change DB_HOST to "127.0.0.1"
>   if you want to run the project without docker

<br>

- **Access the Virtual Environment**

```
source venv/bin/activate
```

> - If you are using windows you need to use the powershell and activate the Virtual Enviroment using this command

```
.\venv\Scripts\activate
```

- **Install dependencies**

```
pip install -r requirements.txt
```

- **Run the Migrations**

```
python manage.py migrate
```

- **Start application**

```
python manage.py runserver
```

## Installing with docker

- **Build application**

```
docker compose up --build
```

- **Start application**

```
docker compose up
```

- **Access application**

```
http://localhost:8000/
```

[Documentation](https://localhost:8000/api/docs/)
