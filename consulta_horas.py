import requests
import json
from datetime import datetime, timedelta

class DiaSob:
    def __init__(self, dia, horas_total, feriado):
        self.dia = dia
        self.horas_total = horas_total
        self.horasSob = None
        self.atendimentos = []
        self.feriado = feriado
        self.valor50 = None
        self.valor75 = None
        self.valor100 = None

def valida_data(data_str: str) -> bool:
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data.weekday() == 0 
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
    if len(chamados_json['data']) != 0 and chamados_json['data']:
        return chamados_json

def consulta_atendente():
    pass

#Carrega os dados armazenados no Json
with open("request_data.json", "r", encoding="utf-8") as arquivo:
    dadosJson = json.load(arquivo) 

#Input da data incial que vai ser usado para busca
data_inicial = input("Qual a data inicial que deseja consulta o periodo de sobre aviso? lembre de colocar sempre uma segunda-feira(Formato: DD/MM/YYYY)\n")
while not valida_data(data_inicial):
    data_inicial = input("Data inválida ou inexistente, digite novamente\n")

data_inicial_obj = datetime.strptime(data_inicial, "%d/%m/%Y")
data_final_obj = data_inicial_obj + timedelta(days=7)

dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
datas_atendimento  = [data_inicial_obj + timedelta(days=i) for i in range(7)]

semana_atendimento = {}

for i in range(7):
    if 0 <= i < 5:
        total_horas = 3
        feriado = False
    elif i < 6: 
        total_horas = 10
        feriado = False       
    else:
        total_horas = 8
        feriado = True
    string_data_iteracao = datetime.strftime(datas_atendimento[i], "%d/%m/%Y")
    semana_atendimento[string_data_iteracao] = DiaSob(dias_semana[i],total_horas, feriado)

chamados_dic = consulta_chamados(data_inicial_obj, data_final_obj)
if chamados_dic:
    for chamado in chamados_dic:
        print(chamado)
else:
    print('Não foram encontrados chamados no periodo especificado')