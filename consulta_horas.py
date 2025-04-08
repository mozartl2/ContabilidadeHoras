import requests
import json
from datetime import datetime, timedelta

def valida_data(data_str):
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def consulta_chamados(data_inicial_dt, data_final_dt):
    data_inicial_string = data_inicial_dt.strftime("%Y-%m-%d %H:%M:%S") + "-0300"
    data_final_string = data_final_dt.strftime("%Y-%m-%d ") + "23:59:59-0300"

    url = (
        f"{dadosJson['UrlConsultaChamado']}?"
        f"customer_id={dadosJson['custumer_id']}&"
        f"department_id={dadosJson['id_departamento_suporte']}&"
        f"category_id={dadosJson['id_categoria_saviso']}&"
        f"creation_date_ge={data_inicial_string}&"
        f"creation_date_le={data_final_string}"
    )

    headers = {
        "Authorization": dadosJson["Authorization"]
    }

    lista_chamados = requests.get(url, headers=headers)
    chamados_json = lista_chamados.json()
    if len(chamados_json['data']) != 0:
        return chamados_json
    else: 
        return False


def consulta_atendente():
    pass

#Carrega os dados armazenados no Json
with open("request_data.json", "r", encoding="utf-8") as arquivo:
    dadosJson = json.load(arquivo) 

data_inicial = input("Qual a data inicial que deseja consulta o periodo de sobre aviso? lembre de colocar sempre uma segunda-feira(Formato: DD/MM/YYYY)")
if not valida_data(data_inicial):
    print("Data inválida ou inexistente, digite novamente")
else:
    data_inicial_obj = datetime.strptime(data_inicial, "%d/%m/%Y")
    data_final_obj = data_inicial_obj + timedelta(days=7)

    chamados_dic = consulta_chamados(data_inicial_obj, data_final_obj)
    jsonformat = json.dumps(chamados_dic, indent=4, ensure_ascii="utf-8")
    print(jsonformat)

