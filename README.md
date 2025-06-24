# F1 Virtual - Gerenciador de Campeonatos

Um aplicativo simples para gerenciar campeonatos de F1 virtual, permitindo cadastrar pilotos, corridas, resultados e visualizar a classificação.

## Funcionalidades

- Cadastro de múltiplos campeonatos
- Cadastro de pilotos para cada campeonato
- Cadastro de corridas para cada campeonato
- Registro de resultados das corridas
- Sistema de pontuação personalizável
- Visualização da classificação geral
- Armazenamento de dados em arquivos CSV

## Tecnologias Utilizadas

- Backend: Python com Flask
- Frontend: HTML, CSS e JavaScript
- Banco de Dados: Arquivos CSV

## Como Executar

1. Certifique-se de ter o Python instalado (versão 3.6 ou superior)
2. Instale as dependências:
   ```
   pip install flask
   ```
3. Navegue até a pasta do aplicativo:
   ```
   cd app
   ```
4. Execute o aplicativo:
   ```
   python app.py
   ```
5. Acesse o aplicativo no navegador:
   ```
   http://localhost:5000
   ```

## Estrutura do Projeto

- `/app` - Diretório principal do aplicativo
  - `/static` - Arquivos estáticos (CSS, JS, imagens)
  - `/templates` - Templates HTML
  - `/data` - Diretório onde os dados são armazenados
  - `app.py` - Arquivo principal do aplicativo

## Estrutura de Dados

- `championships.csv` - Lista de campeonatos
- `[championship_id]/drivers.csv` - Lista de pilotos do campeonato
- `[championship_id]/races.csv` - Lista de corridas do campeonato
- `[championship_id]/results_[race_id].csv` - Resultados de uma corrida
- `[championship_id]/scoring.json` - Sistema de pontuação do campeonato

## Licença

Este projeto é para uso pessoal e educacional.
