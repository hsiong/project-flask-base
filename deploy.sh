cd docker

sudo docker compose -f docker-compose.middleware.yaml down

sudo docker compose -f docker-compose.middleware.yaml up -d

```markdown
DBeaver
create table 'ai_parse'
grant privileges on ai_parse.* to 'test'@'%';
```

cd ..
uv pip install -r pyproject.toml
# uv pip install --extras dev  -r pyproject.toml

cd flaskr
PYTHONPATH=../ python main.py

