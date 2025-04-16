import requests
import json
from datetime import datetime, timedelta

class DiaSobr:
    def __init__(self, dia, horas_total, feriado):
        self.dia = dia
        self.horas_total = {'quant': horas_total,'valor': 0}
        self.atendimentos = set()
        self.feriado = feriado
        self.valores = {
            "1/3": {"quant": 0, "valor": 0},
            "50%": {"quant": 0, "valor": 0},
            "75%": {"quant": 0, "valor": 0},
            "100%": {"quant": 0, "valor": 0}
        }

    def __repr__(self):
        pass
    
    def calcula(self):
        if self.feriado == False:
            self.valores['1/3']['quant'] = self.horas_total['quant'] - len(self.atendimentos)
            if len(self.atendimentos) > 2:
                self.valores['50%']['quant'] = 2 
                self.valores['75%']['quant'] = len(self.atendimentos) - 2
            else:
                self.valores['50%']['quant'] = len(self.atendimentos)
        else:
            self.valores['100%']['quant'] = len(self.atendimentos)
            self.valores['1/3']['quant'] = self.horas_total['quant'] - len(self.atendimentos)
            
        self.valores['1/3']['valor'] = self.valores['1/3']['quant'] * valor_hora / 3
        self.valores['50%']['valor'] =  self.valores['50%']['quant'] * 1.5 * valor_hora
        self.valores['75%']['valor'] =  self.valores['75%']['quant'] * 1.75 * valor_hora
        self.valores['100%']['valor']  =  self.valores['100%']['quant'] * 2 * valor_hora
        self.horas_total['valor'] = self.valores['50%']['valor'] + self.valores['75%']['valor'] + self.valores['100%']['valor'] + self.valores['1/3']['valor']

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

def dtm_to_dta_hra(str_dia):
    if str_dia[-3] == ':':
        str_dia = str_dia[:-3] + str_dia[-2:]
    obj_dia = datetime.strptime(str_dia, "%Y-%m-%d %H:%M:%S%z")
    data = obj_dia.date()
    data_str_formatada = data.strftime("%d/%m/%Y")
    hora = obj_dia.hour
    return data_str_formatada, hora

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

salario_bruto = input("Qual o valor do sário bruto a ser levado em consideração?")
valor_hora = float(salario_bruto)/200

#Verificar se há feriado 

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
        dia, hora = dtm_to_dta_hra(chamado['creation_date'])
        operador = chamado['operator']['name']
        periodo_atendimento[dia].atendimentos.add(hora)
        # print(f"Dia: {dia}, Hora: {hora}, Operador: {operador}")
else:
    print('Não foram encontrados chamados no periodo especificado')

for indice, obj in periodo_atendimento.items():
    obj.calcula()
    print(f"ID: {indice}, Dia: {obj.dia}, Atendimentos: {len(obj.atendimentos)}")