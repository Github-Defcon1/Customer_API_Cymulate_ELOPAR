import os
import json
import requests
import re
from concurrent.futures import ThreadPoolExecutor

dataInicio = "2024-09-01"  # YYYY-MM-DD
dataFim = "2024-12-31"  # YYYY-MM-DD
xtoken = "xtoken: SUA_CHAVE_AQUI"  # Cymulate API Token
module = "edr"  # immediate-threats, mail, browsing, waf, edr, dlp, hopper
payload = {}
headers = {
    'x-token': f'{xtoken}'
}

# Função para criar diretórios para cada environment name
def create_directories(env_name):
    os.makedirs(f"environments/{env_name}/{module}/history", exist_ok=True)
    os.makedirs(f"environments/{env_name}/{module}/report", exist_ok=True)

# Função para limpar o conteúdo dos diretórios
def clear_directories(env_name):
    history_dir = f"environments/{env_name}/{module}/history"
    report_dir = f"environments/{env_name}/{module}/report"

    for folder in [history_dir, report_dir]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Falha ao deletar {file_path}. Motivo: {e}")

# Função para limpar o diretório unified_reports
def clear_reports():
    reports_dir = f"unified_reports/{module}"
    if os.path.exists(reports_dir):
        for filename in os.listdir(reports_dir):
            file_path = os.path.join(reports_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Falha ao deletar {file_path}. Motivo: {e}")

# Função para processar cada ID de assessment
def process_assessment_id(assessment_id, env_name, env_id):
    url_report = f"https://api.app.cymulate.com/v1/{module}/history/executive/{assessment_id}"

    response_report = requests.request("GET", url_report, headers=headers, data=payload)
    json_report = response_report.json()

    # Adiciona os cabeçalhos JSON adicionais
    json_report.update({
        "environment_name": env_name,
        "environment_id": env_id,
        "data-range-start-search": dataInicio,
        "data-range-end-search": dataFim
    })

    arquivo = f"environments/{env_name}/{module}/report/{module}_report-{dataInicio}-{dataFim}-{assessment_id}.json"
    with open(arquivo, 'w') as json_file:
        json.dump(json_report, json_file, indent=4)

# Função para processar cada arquivo JSON
def process_file(file_path, env_name, env_id):
    if os.path.getsize(file_path) > 0:  # Verifica se o arquivo não está vazio
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                assessments = data['data']['attack']

                # Usa ThreadPoolExecutor para processar os IDs de assessment em paralelo
                with ThreadPoolExecutor() as executor:
                    list(executor.map(lambda ids: process_assessment_id(ids['ID'], env_name, env_id), assessments))
            except json.JSONDecodeError:
                print(f"Erro ao decodificar o JSON no arquivo {file_path}")
            except requests.RequestException as e:
                print(f"Falha na requisição para o arquivo {file_path}: {e}")
    else:
        print(f"O arquivo {file_path} está vazio e foi ignorado.")

# Função para unificar os arquivos JSON
def unify_json_files(env_name, env_id):
    if env_id == "default" or env_name == "Default Environment":
        return  # Pula o environment "default"

    report_dir = f"environments/{env_name}/{module}/report"
    unified_data = []

    for file_name in os.listdir(report_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(report_dir, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                unified_data.append(data)

    # Adiciona cabeçalhos JSON adicionais ao final do arquivo unificado apenas se unified_data estiver vazio
    if not unified_data:
        unified_data.append({
            "environment_name": env_name,
            "environment_id": env_id,
            "data-range-start-search": dataInicio,
            "data-range-end-search": dataFim
        })

    unified_file_path = f"unified_reports/{module}/unified_report-{dataInicio}-{dataFim}-{env_name}.json"
    os.makedirs(f"unified_reports/{module}", exist_ok=True)

    with open(unified_file_path, 'w') as unified_file:
        json.dump(unified_data, unified_file, indent=4)

# URL para obter os environments
url_environments = "https://api.app.cymulate.com/v1/environments"

# Faz a requisição para obter os environments
response_url_environments = requests.request("GET", url_environments, headers=headers, data=payload)
json_url_environments = response_url_environments.json()

# Limpa o diretório unified_reports
clear_reports()

# Cria diretórios, limpa o conteúdo e salva os arquivos de history para cada environment name
for env in json_url_environments['data']:
    env_id = env['id']
    env_name = re.sub(r'[^\w\s-]', '', env['name']).replace(' ', '_')  # Remove caracteres especiais e substitui espaços por underscores
    create_directories(env_name)
    clear_directories(env_name)

    url_history = f"https://api.app.cymulate.com/v1/{module}/history/get-ids?fromDate={dataInicio}&toDate={dataFim}&env={env_id}"

    response_history = requests.request("GET", url_history, headers=headers, data=payload)
    json_history = response_history.json()

    arquivo_history = f"environments/{env_name}/{module}/history/{module}_history-{dataInicio}-{dataFim}-{env_name}.json"
    with open(arquivo_history, 'w') as json_file:
        json.dump(json_history, json_file, indent=4)

# Usa ThreadPoolExecutor para processar os arquivos em paralelo
def process_env(env):
    env_id = env['id']
    env_name = re.sub(r'[^\w\s-]', '', env['name']).replace(' ', '_')
    file_path = f"environments/{env_name}/{module}/history/{module}_history-{dataInicio}-{dataFim}-{env_name}.json"
    process_file(file_path, env_name, env_id)

with ThreadPoolExecutor() as executor:
    executor.map(process_env, json_url_environments['data'])

# Unifica todos os arquivos JSON salvos em cada {env_name}/report em um único arquivo .json por environment name
for env in json_url_environments['data']:
    env_name = re.sub(r'[^\w\s-]', '', env['name']).replace(' ', '_')
    env_id = env['id']
    unify_json_files(env_name, env_id)

print("Processamento concluído e arquivos unificados.")