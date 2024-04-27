import requests
import json
from datetime import timedelta, datetime, date

data = {
    "username": "Sigur_api",
    "password": "h12345678"
}

Point = {'id': 46, 'name': 'Турникет 1', 'folderId': 44}  # accesspoints
departments = {'id': 2327, 'parentId': 0, 'name': 'Посетители', 'hasChildren': False, 'description': ''}, {'id': 5188,
                                                                                                           'parentId': 0,
                                                                                                           'name': 'Постетители_old',
                                                                                                           'hasChildren': False,
                                                                                                           'description': ''}

headers = {'Content-Type': 'application/json'}
url_auth = "http://176.213.100.220:8080/api/v1/users/auth"

response_auth = requests.post(url_auth, data=json.dumps(data), headers=headers)
Token = response_auth.json()
headers = {
    'Authorization': Token['token']
}
Time = datetime.now() - timedelta(hours=1)
Year = Time.strftime('%Y')
Month = Time.strftime('%m')
Day = Time.strftime('%d')
Hour = Time.strftime('%H')

# events/parsed?accessPointId=46&department_id=2327
url = f"http://176.213.100.220:8080/api/v1/events/parsed?limit=10000&startTime={Year}-{Month}-{Day}T{Hour}:00:00%2B03:00&accessPointId=46"

#url = 'http://176.213.100.220:8080/api/v1/employees/5239'
#url = 'http://176.213.100.220:8080/api/v1/employees?departmentId=2327&limit=10000'

#employees - служащие

'''Кудрявцев Антон Муж. Р.о.ня'''
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print("Запрос выполнен успешно")
    print("Ответ сервера:")
    JSON = response.json()
    print(len(JSON))
    if type(JSON) == list:
        #accessObject1 = [d['additionalData']['accessObject']['data']['id'] for d in JSON if "accessObject"  in d['additionalData'].keys() and d['data']['direction'] == 'OUT'] # id пользователей на выход
        #print(list(set(accessObject1)))
        accessObject = []
        for d in JSON:
            try:
                if ('additionalData' in d and 'accessObject' in d['additionalData'] and 'data' in d['additionalData']['accessObject'] and 'id' in d['additionalData']['accessObject']['data'] and d['data']['direction'] == 'OUT'):
                    accessObject.append(d['additionalData']['accessObject']['data']['id'])
            except:
                print('Сработало исключение')
        accessObject_list_id = list(set(accessObject))
        print(accessObject_list_id)
        url_employees = f'http://176.213.100.220:8080/api/v1/employees?id={", ".join(map(str, accessObject_list_id))}&limit=10000' # Получаем данные о пользователей
        response_employees = requests.get(url_employees, headers=headers).json()
        response_employees_List = [f for f in response_employees if 'description' in f.keys() and f['description'].find('создан роботом') != -1 and f['departmentId'] == 2327] # Список users которые созданы роботом и равняются отделу Посетители
        response_employees_List = list(set(response_employees_List))
        print(response_employees_List)
        if any(response_employees_List) == True:
            for i in response_employees_List:
                employees_id = JSON['id']
                del JSON['id']
                del JSON['isBlocked']
                JSON.update(departmentId=5188)

                headers_put = {
                    'Authorization': "Bearer " + Token['token']
                }
                response_put = requests.put(f'http://176.213.100.220:8080/api/v1/employees/{employees_id}',
                                            headers=headers_put, json=JSON)
                print(response_put.json())

else:
    print("Ошибка при выполнении запроса. Код ошибки:", response.status_code, response.json())
