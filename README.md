Hello!
Simple 2 microservices which can communicate between each other
My project have:

-Pydantic

-Db:Sqlalchemy

-Asyncio

-Httpx

1. Clone repository

`https://github.com/ShadowDubina/Fastapi-project.git`

2. Go to the direcroty:

`cd record'

3. Create vertual venv

`python -m venv env`

4. Go to the env

`env/Scripts/activate`

5. install requirements

`pip install -r requirements.txt`

6.Run microservice:

`uvicorn main:app --host 0.0.0.0 --port 80'

7.Open new cmd

8. Go to the direcroty:

`cd user'

9. Create vertual venv

`python -m venv env`

10. Go to the env

`env/Scripts/activate`

11. install requirements

`pip install -r requirements.txt`

12.Run microservice:

`uvicorn main:app --host 0.0.0.0 --port 81'
