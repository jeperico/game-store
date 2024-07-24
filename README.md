Django com Postgress + Django + Django Rest e Jazzmin

## PREREQUISITES
Ter docker e docker composer v2 e o virtualenv
```bash
sudo apt install docker-compose-v2 docker.io python3-virtualenv
```

Criar um virtual env e ativa-lo
```bash
virtualenv venv
source venv/bin/activate
```

Instalar o Poetry
```bash
pip install poetry
```

Rodar as dependências
```bash
poetry install
```

rodar a primeira vez
```bash
cp .env.example .env
make runserver
```


## RUN PROJECT
Para rodar o projeto em dev você pode usar o docker de banco de dados e em seguida subir a aplicação em dev
```bash
make rundb
make runserver
```

> [!CAUTION]
> NÃO UTILIZAR PIP INSTALL PARA NENHUMA DEPENDÊNCIA, SOMENTE 'poetry add'
