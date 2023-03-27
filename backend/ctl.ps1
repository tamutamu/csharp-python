# poetry run alembic -c .\src\alembic.ini revision --autogenerate -m $Args[0]
poetry run alembic -c .\src\alembic.ini upgrade head
