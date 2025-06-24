from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'f1virtual'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Garantir que o diretório de dados existe
os.makedirs(DATA_DIR, exist_ok=True)

def get_championships():
    """Retorna a lista de campeonatos cadastrados"""
    championships_file = os.path.join(DATA_DIR, 'championships.csv')
    
    if not os.path.exists(championships_file):
        # Criar arquivo se não existir
        with open(championships_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'category', 'created_at'])
        return []
    
    championships = []
    with open(championships_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            championships.append(row)
    
    return championships

def get_championship(championship_id):
    """Retorna os detalhes de um campeonato específico"""
    championships = get_championships()
    for championship in championships:
        if championship['id'] == championship_id:
            return championship
    return None

def save_championship(name, category):
    """Salva um novo campeonato"""
    championships_file = os.path.join(DATA_DIR, 'championships.csv')
    
    # Gerar ID único
    championship_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    championships = get_championships()
    
    # Verificar se o arquivo já existe
    file_exists = os.path.exists(championships_file)
    
    with open(championships_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'name', 'category', 'created_at']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Escrever cabeçalho se o arquivo for novo
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'id': championship_id,
            'name': name,
            'category': category,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Criar diretório para o campeonato
    championship_dir = os.path.join(DATA_DIR, championship_id)
    os.makedirs(championship_dir, exist_ok=True)
    
    # Criar arquivo de pontuação padrão
    scoring_file = os.path.join(championship_dir, 'scoring.json')
    default_scoring = {
        'positions': {
            '1': 25,
            '2': 18,
            '3': 15,
            '4': 12,
            '5': 10,
            '6': 8,
            '7': 6,
            '8': 4,
            '9': 2,
            '10': 1
        }
    }
    
    with open(scoring_file, 'w', encoding='utf-8') as f:
        json.dump(default_scoring, f, indent=4)
    
    return championship_id

def get_drivers(championship_id):
    """Retorna a lista de pilotos de um campeonato"""
    drivers_file = os.path.join(DATA_DIR, championship_id, 'drivers.csv')
    
    if not os.path.exists(drivers_file):
        # Criar arquivo se não existir
        os.makedirs(os.path.dirname(drivers_file), exist_ok=True)
        with open(drivers_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'team', 'number'])
        return []
    
    drivers = []
    with open(drivers_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            drivers.append(row)
    
    return drivers

def save_driver(championship_id, name, team, number):
    """Salva um novo piloto no campeonato"""
    drivers_file = os.path.join(DATA_DIR, championship_id, 'drivers.csv')
    
    # Gerar ID único
    driver_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Verificar se o arquivo já existe
    file_exists = os.path.exists(drivers_file)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(drivers_file), exist_ok=True)
    
    with open(drivers_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'name', 'team', 'number']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Escrever cabeçalho se o arquivo for novo
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'id': driver_id,
            'name': name,
            'team': team,
            'number': number
        })
    
    return driver_id

def get_races(championship_id):
    """Retorna a lista de corridas de um campeonato"""
    races_file = os.path.join(DATA_DIR, championship_id, 'races.csv')
    
    if not os.path.exists(races_file):
        # Criar arquivo se não existir
        os.makedirs(os.path.dirname(races_file), exist_ok=True)
        with open(races_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'date', 'track'])
        return []
    
    races = []
    with open(races_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            races.append(row)
    
    return races

def save_race(championship_id, name, date, track):
    """Salva uma nova corrida no campeonato"""
    races_file = os.path.join(DATA_DIR, championship_id, 'races.csv')
    
    # Gerar ID único
    race_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Verificar se o arquivo já existe
    file_exists = os.path.exists(races_file)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(races_file), exist_ok=True)
    
    with open(races_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'name', 'date', 'track']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Escrever cabeçalho se o arquivo for novo
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'id': race_id,
            'name': name,
            'date': date,
            'track': track
        })
    
    return race_id

def get_race_results(championship_id, race_id):
    """Retorna os resultados de uma corrida"""
    results_file = os.path.join(DATA_DIR, championship_id, f'results_{race_id}.csv')
    
    if not os.path.exists(results_file):
        return []
    
    results = []
    with open(results_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    
    return results

def save_race_results(championship_id, race_id, results):
    """Salva os resultados de uma corrida"""
    results_file = os.path.join(DATA_DIR, championship_id, f'results_{race_id}.csv')
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(results_file), exist_ok=True)
    
    with open(results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['driver_id', 'position']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            writer.writerow({
                'driver_id': result['driver_id'],
                'position': result['position']
            })

def get_scoring(championship_id):
    """Retorna o sistema de pontuação do campeonato"""
    scoring_file = os.path.join(DATA_DIR, championship_id, 'scoring.json')
    
    if not os.path.exists(scoring_file):
        # Criar pontuação padrão
        default_scoring = {
            'positions': {
                '1': 25,
                '2': 18,
                '3': 15,
                '4': 12,
                '5': 10,
                '6': 8,
                '7': 6,
                '8': 4,
                '9': 2,
                '10': 1
            }
        }
        
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(scoring_file), exist_ok=True)
        
        with open(scoring_file, 'w', encoding='utf-8') as f:
            json.dump(default_scoring, f, indent=4)
        
        return default_scoring
    
    with open(scoring_file, 'r', encoding='utf-8') as f:
        scoring = json.load(f)
    
    return scoring

def save_scoring(championship_id, scoring):
    """Salva o sistema de pontuação do campeonato"""
    scoring_file = os.path.join(DATA_DIR, championship_id, 'scoring.json')
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(scoring_file), exist_ok=True)
    
    with open(scoring_file, 'w', encoding='utf-8') as f:
        json.dump(scoring, f, indent=4)

def calculate_standings(championship_id):
    """Calcula a classificação atual do campeonato"""
    drivers = get_championship_drivers(championship_id)
    races = get_races(championship_id)
    scoring = get_scoring(championship_id)
    
    # Inicializar pontuação
    standings = {driver['id']: {'driver': driver, 'points': 0, 'positions': {}} for driver in drivers}
    
    # Calcular pontos para cada corrida
    for race in races:
        race_id = race['id']
        results = get_race_results(championship_id, race_id)
        
        for result in results:
            driver_id = result['driver_id']
            position = result['position']
            
            if driver_id in standings:
                # Adicionar posição ao histórico
                standings[driver_id]['positions'][race_id] = position
                
                # Adicionar pontos
                if position in scoring['positions']:
                    points = int(scoring['positions'][position])
                    standings[driver_id]['points'] += points
    
    # Converter para lista e ordenar por pontuação
    standings_list = list(standings.values())
    standings_list.sort(key=lambda x: x['points'], reverse=True)
    
    return standings_list

def calculate_global_rankings():
    """Calcula o ranking geral de todos os pilotos em todos os campeonatos"""
    championships = get_championships()
    global_drivers = get_global_drivers()
    
    # Inicializar pontuação
    global_rankings = {driver['id']: {'driver': driver, 'points': 0, 'championships': []} for driver in global_drivers}
    
    # Calcular pontos para cada campeonato
    for championship in championships:
        championship_id = championship['id']
        standings = calculate_standings(championship_id)
        
        for position in standings:
            driver_id = position['driver']['id']
            
            if driver_id in global_rankings:
                # Adicionar pontos
                global_rankings[driver_id]['points'] += position['points']
                
                # Adicionar campeonato ao histórico
                global_rankings[driver_id]['championships'].append({
                    'championship': championship,
                    'points': position['points']
                })
    
    # Converter para lista e ordenar por pontuação
    rankings_list = []
    for driver_id, data in global_rankings.items():
        if data['championships']:  # Só incluir pilotos que participaram de pelo menos um campeonato
            rankings_list.append(data)
    
    rankings_list.sort(key=lambda x: x['points'], reverse=True)
    
    return rankings_list

def get_global_drivers():
    """Retorna a lista de pilotos globais cadastrados"""
    drivers_file = os.path.join(DATA_DIR, 'global_drivers.csv')
    
    if not os.path.exists(drivers_file):
        # Criar arquivo se não existir
        os.makedirs(os.path.dirname(drivers_file), exist_ok=True)
        with open(drivers_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'created_at'])
        return []
    
    drivers = []
    with open(drivers_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            drivers.append(row)
    
    return drivers

def save_global_driver(name):
    """Salva um novo piloto global"""
    drivers_file = os.path.join(DATA_DIR, 'global_drivers.csv')
    
    # Verificar se já existe um piloto com o mesmo nome
    existing_drivers = get_global_drivers()
    for driver in existing_drivers:
        if driver['name'].lower() == name.lower():
            return None  # Piloto já existe
    
    # Gerar ID único
    driver_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Verificar se o arquivo já existe
    file_exists = os.path.exists(drivers_file)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(drivers_file), exist_ok=True)
    
    with open(drivers_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'name', 'created_at']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Escrever cabeçalho se o arquivo for novo
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'id': driver_id,
            'name': name,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return driver_id

def get_championship_drivers(championship_id):
    """Retorna a lista de pilotos associados a um campeonato"""
    drivers_file = os.path.join(DATA_DIR, championship_id, 'drivers.csv')
    
    if not os.path.exists(drivers_file):
        # Criar arquivo se não existir
        os.makedirs(os.path.dirname(drivers_file), exist_ok=True)
        with open(drivers_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['driver_id', 'team'])
        return []
    
    championship_drivers = []
    with open(drivers_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            championship_drivers.append(row)
    
    # Obter informações completas dos pilotos
    global_drivers = get_global_drivers()
    drivers_dict = {d['id']: d for d in global_drivers}
    
    # Combinar informações
    complete_drivers = []
    for cd in championship_drivers:
        if cd['driver_id'] in drivers_dict:
            driver_info = drivers_dict[cd['driver_id']]
            complete_driver = {
                'id': cd['driver_id'],
                'name': driver_info['name'],
                'team': cd['team']
            }
            complete_drivers.append(complete_driver)
    
    return complete_drivers

def add_driver_to_championship(championship_id, driver_id, team):
    """Adiciona um piloto existente a um campeonato"""
    drivers_file = os.path.join(DATA_DIR, championship_id, 'drivers.csv')
    
    # Verificar se o piloto já está no campeonato
    championship_drivers = []
    if os.path.exists(drivers_file):
        with open(drivers_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                championship_drivers.append(row)
                if row['driver_id'] == driver_id:
                    return False  # Piloto já está no campeonato
    
    # Verificar se o arquivo já existe
    file_exists = os.path.exists(drivers_file)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(drivers_file), exist_ok=True)
    
    with open(drivers_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['driver_id', 'team']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Escrever cabeçalho se o arquivo for novo
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'driver_id': driver_id,
            'team': team
        })
    
    return True

@app.route('/')
def index():
    championships = get_championships()
    return render_template('index.html', championships=championships)

@app.route('/drivers')
def drivers_list():
    drivers = get_global_drivers()
    return render_template('drivers.html', drivers=drivers)

@app.route('/drivers/new', methods=['GET', 'POST'])
def new_global_driver():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash('Por favor, informe o nome do piloto.')
            return redirect(url_for('new_global_driver'))
        
        driver_id = save_global_driver(name)
        if driver_id:
            flash('Piloto cadastrado com sucesso!')
            return redirect(url_for('drivers_list'))
        else:
            flash('Já existe um piloto com esse nome.')
            return redirect(url_for('new_global_driver'))
    
    return render_template('new_global_driver.html')

@app.route('/championship/new', methods=['GET', 'POST'])
def new_championship():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        
        if not name or not category:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('new_championship'))
        
        championship_id = save_championship(name, category)
        flash('Campeonato criado com sucesso!')
        return redirect(url_for('championship_details', championship_id=championship_id))
    
    return render_template('new_championship.html')

@app.route('/championship/<championship_id>')
def championship_details(championship_id):
    championship = get_championship(championship_id)
    drivers = get_championship_drivers(championship_id)
    races = get_races(championship_id)
    standings = calculate_standings(championship_id)
    
    return render_template('championship_details.html', 
                          championship=championship, 
                          drivers=drivers, 
                          races=races,
                          standings=standings)

@app.route('/championship/<championship_id>/driver/add', methods=['GET', 'POST'])
def add_driver_to_championship_route(championship_id):
    if request.method == 'POST':
        driver_id = request.form.get('driver_id')
        team = request.form.get('team')
        
        if not driver_id or not team:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('add_driver_to_championship_route', championship_id=championship_id))
        
        success = add_driver_to_championship(championship_id, driver_id, team)
        if success:
            flash('Piloto adicionado ao campeonato com sucesso!')
        else:
            flash('Este piloto já está neste campeonato.')
        return redirect(url_for('championship_details', championship_id=championship_id))
    
    championship = get_championship(championship_id)
    global_drivers = get_global_drivers()
    championship_drivers = get_championship_drivers(championship_id)
    
    # Filtrar pilotos que ainda não estão no campeonato
    championship_driver_ids = [d['id'] for d in championship_drivers]
    available_drivers = [d for d in global_drivers if d['id'] not in championship_driver_ids]
    
    return render_template('add_driver_to_championship.html', 
                          championship=championship,
                          drivers=available_drivers)

@app.route('/championship/<championship_id>/race/new', methods=['GET', 'POST'])
def new_race(championship_id):
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        track = request.form.get('track')
        
        if not name or not date or not track:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('new_race', championship_id=championship_id))
        
        save_race(championship_id, name, date, track)
        flash('Corrida adicionada com sucesso!')
        return redirect(url_for('championship_details', championship_id=championship_id))
    
    championship = get_championship(championship_id)
    return render_template('new_race.html', championship=championship)

@app.route('/championship/<championship_id>/race/<race_id>/results', methods=['GET', 'POST'])
def race_results(championship_id, race_id):
    championship = get_championship(championship_id)
    race = None
    races = get_races(championship_id)
    
    for r in races:
        if r['id'] == race_id:
            race = r
            break
    
    drivers = get_championship_drivers(championship_id)
    
    if request.method == 'POST':
        results = []
        for driver in drivers:
            position = request.form.get(f'position_{driver["id"]}')
            if position:
                results.append({
                    'driver_id': driver['id'],
                    'position': position
                })
        
        save_race_results(championship_id, race_id, results)
        flash('Resultados salvos com sucesso!')
        return redirect(url_for('championship_details', championship_id=championship_id))
    
    # Carregar resultados existentes
    existing_results = get_race_results(championship_id, race_id)
    results_dict = {r['driver_id']: r['position'] for r in existing_results}
    
    return render_template('race_results.html', 
                          championship=championship,
                          race=race,
                          drivers=drivers,
                          results=results_dict)

@app.route('/championship/<championship_id>/scoring', methods=['GET', 'POST'])
def scoring_settings(championship_id):
    championship = get_championship(championship_id)
    scoring = get_scoring(championship_id)
    
    if request.method == 'POST':
        positions = {}
        for i in range(1, 21):  # Permitir até 20 posições pontuadas
            position_key = str(i)
            points = request.form.get(f'points_{i}')
            if points and points.isdigit():
                positions[position_key] = int(points)
        
        new_scoring = {'positions': positions}
        save_scoring(championship_id, new_scoring)
        flash('Sistema de pontuação atualizado com sucesso!')
        return redirect(url_for('championship_details', championship_id=championship_id))
    
    return render_template('scoring.html', championship=championship, scoring=scoring)

@app.route('/championship/<championship_id>/standings')
def standings(championship_id):
    championship = get_championship(championship_id)
    standings_list = calculate_standings(championship_id)
    races = get_races(championship_id)
    
    return render_template('standings.html', 
                          championship=championship,
                          standings=standings_list,
                          races=races)

@app.route('/rankings')
def global_rankings():
    rankings = calculate_global_rankings()
    return render_template('global_rankings.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)
