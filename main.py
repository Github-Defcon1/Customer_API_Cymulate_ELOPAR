from scripts.app import CollectCymulateData
from scripts.endpoints.EnvsAndHosts import CollectEnvData

def run():
    data_colector = CollectCymulateData()
    env_data = CollectEnvData()

    # Data início
    print('''
        Informe aqui o inicio do range de coleta:
        Exemplo: yyyy-mm-dd
    ''')
    dt_inicio = str(input('Insira aqui: '))

    # Data fim
    print('''
        Informe aqui o fim do range de coleta:
        Exemplo: yyyy-mm-dd
    ''')
    dt_fim = str(input('Insira aqui: '))

    print(f'Range de tempo foi definido de {dt_inicio} até {dt_fim}')

    # Escolha do cliente
    print('''
        Informe qual cliente os dados serão coletados:
        1 - Ambiente01; 
        2 - Ambiente02; 
        3 - Ambiente03 
    ''')
    escolha = int(input('Insira a sua escolha aqui: '))
    # Caso tiver mais de uma API/ambiente e quiser consultar por opções, alimente as opções abaixo.
    if escolha == 1:
        data_colector.cliente = 'Ambiente01'
        xtoken = 'xtoken": "SUA_CHAVE_AQUI'
        env_data.cliente = 'Ambiente01'
    elif escolha == 2:
        data_colector.cliente = 'Ambiente02'
        xtoken = 'xtoken": "SUA_CHAVE_AQUI' 
        env_data.cliente = 'Ambiente02'
    elif escolha == 3:
        data_colector.cliente = 'Ambiente03'
        xtoken = 'xtoken": "SUA_CHAVE_AQUI' 
        env_data.cliente = 'Ambiente03'
    else:
        print('Escolha uma opção válida')
        return

    # Define variáveis globais
    data_colector.dataInicio = dt_inicio
    data_colector.dataFim = dt_fim

    module_list = ["immediate-threats", "mail", "browsing", "waf", "edr", "dlp", "hopper"]

    for module in module_list:
        data_colector.module = module
        print(f"[...] Extração do relatório de {module} em andamento...")
        data_colector.main(xtoken)
        print(f"[!] Relatório de {module} extraído com sucesso!\n\n")

    # Obter lista dos environments e agentes
    env_data.main(xtoken)

    print("[%] Os relatórios dos módulos foram salvos em ./unified_reports")
    print("[%] Os históricos dos assessments foram salvos em ./history")


if __name__ == '__main__':
    run()
