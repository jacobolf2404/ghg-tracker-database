# GHG Tracker Project

The GHG Tracker Project provides comprehensive data on greenhouse gas (GHG) emissions and climate targets, focusing on both national and subnational actors (e.g., states, provinces, and cities). The project harmonizes emissions data and target information into a common framework. Its goal is to create a comprehensive, open-source database that serves as a reliable resource for researchers, policymakers, and stakeholders.

GHG Tracker collects and organizes data on emissions by sector and gas wherever possible. It also integrates national and subnational emission reduction pledges. In addition, the database includes contextual information such as population, GDP, and energy consumption, providing a more complete picture of the drivers behind emissions changes through frameworks like the Kaya identity.

GHG Tracker Database is written entirely in Python to facilitate easier collaboration, maintainability, and integration with the broader data science ecosystem. The first phase of the project is building out the database. The next phase will be a high-level API that makes it easy to query the database. 

## Database Setup

We use Docker and Docker Compose to setup the database.
First define envionrment variables for postgres databse in `./.env`. The `.env` should look like this if developing locally:

```sh
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_DB="ghgtracker"
POSTGRES_PORT="5432"
POSTGRES_HOST="localhost"
DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/ghgtracker"
```

Use the following command to start a database in a container and expose it on localhost port 5432.

```sh
docker-compose up -d
```

## Database migrations

We use [alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations and have it setup to autogenerate. What this means is all you have to do is change the schema in `models/models.py`. Then to create the migration file you run the following:

```sh
alembic revision --autogenerate -m "put message here" --rev-id $(date +"%Y%m%d%H%M%S")
```

this will create a new migration file with your given message in `./migrations/versions/`, it will use the timestamp as the revision `id`

Use the following command to apply the change:

```sh
alembic upgrade head
```

> [!NOTE]  
> since we are still in development phase, let's stick with a single migration file for the time being.