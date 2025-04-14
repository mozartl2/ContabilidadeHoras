import requests
import json
from datetime import datetime, timedelta

class DiaSobr:
    def __init__(self, dia, horas_total, feriado):
        self.dia = dia
        self.horas_total = horas_total
        self.horasSob = None
        self.atendimentos = set()
        self.feriado = feriado
        self.valor50 = None
        self.valor75 = None
        self.valor100 = None
        self.valor_total = None
    
    def calcula():
        pass

    def mostra():
        pass

def valida_data(data_str: str) -> bool:
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data 
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
    
def listar_datas_periodo(dtInicial, dtFinal):
    datas = []
    dtAtual = dtInicial
    while dtAtual <= dtFinal:
        dtAtual_str = datetime.strftime(dtAtual, "%d/%m/%Y")
        datas.append(dtAtual_str)
        dtAtual += timedelta(days=1)
    return datas

def consulta_atendente():
    pass

#Carrega os dados armazenados no Json
with open("request_data.json", "r", encoding="utf-8") as arquivo:
    dadosJson = json.load(arquivo) 

#Input da data incial que vai ser usado para busca, verifica se a data é valida 
data_inicial = input("Qual a data inicial que deseja consulta o periodo de sobre aviso?(Formato: DD/MM/YYYY)\n")
while not valida_data(data_inicial):
    data_inicial = input("Data inválida ou inexistente, digite novamente\n")

data_final = input("Qual a data final que deseja consulta o periodo de sobre aviso?(Formato: DD/MM/YYYY)\n")
while not valida_data(data_inicial):
    data_final = input("Data inválida ou inexistente, digite novamente\n")

data_inicial_obj = datetime.strptime(data_inicial, "%d/%m/%Y")
data_final_obj = datetime.strptime(data_final, "%d/%m/%Y")

dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
datas_atendimento  = listar_datas_periodo(data_inicial_obj, data_final_obj)

periodo_atendimento = {}
#Cria um dicionário para alocar os dados DiaSobr de acordo com os horários de atendimento 
for data in datas_atendimento:
    dataObj = datetime.strptime(data, "%d/%m/%Y")
    dia_semana = dataObj.weekday()
    if 0 <= dia_semana < 5:
        horas_total = 3
        feriado = False
    elif dia_semana < 6:
        horas_total = 10
        feriado = False
    else:
        horas_total = 8
        feriado = True
    periodo_atendimento[data] = DiaSobr(dias_semana[dia_semana], horas_total, feriado)

chamados_dic = consulta_chamados(data_inicial_obj, data_final_obj)
#Valida se há dados na consulta 
if chamados_dic["data"]:
    for chamado in chamados_dic['data']:
        str_data_chamado = chamado['creation_date']
        data_chamado = datetime.strptime(str_data_chamado, "%Y-%m-%d %H:%M:%S")
        data = data_chamado.date()
        hora = data_chamado.hour
        operador = chamado['operator']['name']
else:
    print('Não foram encontrados chamados no periodo especificado')

# print(chamados_dic)