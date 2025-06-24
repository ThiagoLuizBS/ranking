# Instruções para Execução em Docker

Este aplicativo pode ser executado facilmente usando Docker. Siga as instruções abaixo:

## Pré-requisitos

- Docker instalado
- Docker Compose instalado

## Passos para Execução

1. Navegue até a pasta raiz do projeto (onde está o Dockerfile)

2. Construa e inicie o contêiner:

   ```
   docker-compose up -d
   ```

3. Acesse o aplicativo no navegador:

   ```
   http://localhost:5000
   ```

4. Para parar o contêiner:
   ```
   docker-compose down
   ```

## Dados Persistentes

Os dados serão armazenados na pasta `app/data` e serão preservados mesmo se o contêiner for reiniciado ou recriado.

## Observações

- O aplicativo está configurado para rodar em modo de produção
- O servidor Flask está disponível na porta 5000
- Caso precise alterar a porta, edite o arquivo `docker-compose.yml`
