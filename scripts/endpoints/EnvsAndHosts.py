import json
import requests
from scripts.auth import authenticate

class CollectEnvData():
    def __init__(self):
        self.cliente = ""
        self.payload = {}
        self.auth=authenticate()

    def agents(self, xtoken):
        headers = self.auth.create_headers(xtoken)

        url = "https://api.app.cymulate.com/v1/agents/get-all"

        response = requests.request("GET", url, headers=headers, data=self.payload)
        json_response = response.json()

        filename = f"{self.cliente}/environments/agents_list.json"
        with open(filename, 'w') as json_file:
            json.dump(json_response, json_file, indent=4)

    def envs(self, xtoken):
        headers = self.auth.create_headers(xtoken)
        
        url = "https://api.app.cymulate.com/v1/environments"

        response = requests.request("GET", url, headers=headers, data=self.payload)
        json_response = response.json()

        filename = f"{self.cliente}/environments/environments_list.json"
        with open(filename, 'w') as json_file:
            json.dump(json_response, json_file, indent=4)

    def main(self, xtoken):
        self.envs(xtoken)  
        self.agents(xtoken)
        print("[%] Lista de agentes e ambientes salvos na pasta ./environments")


# if __name__ == '__main___':
#     main()