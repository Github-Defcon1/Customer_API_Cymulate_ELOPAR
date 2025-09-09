# Cymulate API Data Collector

Este projeto em Python é uma ferramenta modular e orientada a objetos para coletar e exportar dados de segurança da plataforma Cymulate, consumindo diferentes dados da API.

---

## Estrutura do Projeto

A arquitetura do projeto foi pensada para ser modular, permitindo a fácil adição de novos módulos e a manutenção do código.


---    
## Como Usar

### Pré-requisitos

Certifique-se de ter o Python instalado. É recomendado usar um ambiente virtual (venv).

Instale as bibliotecas necessárias:
pip install requests

### Configurar as Chaves de API

Para manter suas chaves seguras, o projeto usa um arquivo de configuração.

- Crie a pasta config na raiz do projeto.
- Dentro dela, crie um arquivo chamado tokens.json.
- Adicione sua chave da API da Cymulate no seguinte formato:

{
    "xtoken": "SUA_CHAVE_AQUI"
}

**Importante:** Este arquivo é ignorado pelo _.gitignore_ para que suas credenciais não sejam versionadas.



## Contribuições

Sinta-se à vontade para abrir uma issue ou enviar um pull request para melhorias ou correções.
