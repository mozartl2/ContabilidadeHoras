import requests
import json

request = requests.get("https://api.tomticket.com/v2.0/department/category/list?department_id=0414e1bd20d6cefcd74b25436b4d4c02", headers={"Authorization": "c4e50e0862a0249d97b5de3585162d815852e1c06ab0efd55db2fc9533dae52c"})
requestJson = request.json()
jsonFormat = json.dumps(requestJson, indent=4, ensure_ascii=False)
print(jsonFormat)