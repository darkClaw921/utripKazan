from bitrix24 import Bitrix24
from ForWorkGSheet import Sheet
import datetime 
import os
#print(os.environ.get('webHook'))
bit = Bitrix24(os.environ.get('webHook'))
#bit = Bitrix24(webHook)

today = datetime.date.today()
SHEET_NAME = 'copy_graphik'
PATH_JSON_ACCAUNT = 'kgtaprojects-8706cc47a185.json'
listName = 'Апрель'
sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)

def prepare_body(event):
    import base64
    from urllib.parse import unquote
    body = event['body']
    print(body)
    body = str(base64.b64decode(body))
    print(body)
    body = str(unquote(body))
    body = body.split('&')
    body[0] = body[0].split("'")[1]
    print(body)
    return body

week = {
    1: ['B', 'C', 'D', 'E', 'F', 'G', 'H'],
    2: ['J', 'K', 'L', 'M', 'N', 'O', 'P'],
    3: ['R', 'S', 'T', 'U', 'V', 'W', 'X'],
    4: ['Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'],
    5: ['AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN'],
}

def get_col_name():
    today = datetime.date.today().weekday()
    # print(today)  # 1
    today1 = datetime.date.today()

    week_number = get_week_of_day(today1)
    print('week_number: ', week_number)

    col = week[week_number][today]
    return col


def get_week_of_day(date):
    first_day = date.replace(day=1)
    iso_day_one = first_day.isocalendar()[1]
    iso_day_date = date.isocalendar()[1]
    adjusted_week = (iso_day_date - iso_day_one) + 1
    return adjusted_week

def get_assigned_graph_menedger():
    print('попали в получение менеджеров')
    col = get_col_name()
    maxMenegerStart = sheet.find_cell('Менеджеры').row + 5
    maxMenegerEnd = sheet.find_cell('Конец менеджеров').row 
    print(f'{maxMenegerStart=}')
    print(f'{maxMenegerEnd=}')
    users = []
    for i in range(maxMenegerStart, maxMenegerEnd):
        valueGraph = sheet.get_cell(row=f'{col}{i}')
        #print(f'{valueGraph=}')
        if valueGraph == 'TRUE':
            valueUsers = sheet.get_cell(row=f'A{i}')
            #print(f'{valueUsers=}')
            userID = valueUsers.split(' ')[0].replace('[', '').replace(']', '')
            users.append(int(userID))
    return users

def get_assigned_graph_admin():
    col = get_col_name()
    maxAdminStart = sheet.find_cell('Админы').row + 5
    maxAdminEnd =sheet.find_cell('Конец Админов').row
    allRows = maxAdminEnd - maxAdminStart
    users = []
    for i in range(maxAdminStart, maxAdminEnd):
        valueGraph = sheet.get_cell(row=f'{col}{i}')
        if valueGraph == 'TRUE':
            valueUsers = sheet.get_cell(row=f'A{i}')
            userID = valueUsers.split(' ')[0].replace('[', '').replace(']', '')
            users.append(int(userID))
    return users

def update_deal(users,deal,):
    bit.callMethod('crm.contact.update', ID=deal['CONTACT_ID'], fields={
                'ASSIGNED_BY_ID': str(users[0]),
                #'UF_CRM_1680207208770': today,
            })
    bit.callMethod('crm.deal.update', ID=deal['ID'], fields={
            'ASSIGNED_BY_ID': str(users[0]),
            'UF_CRM_1680207208770': today,})

def get_deal_id(prepareBody: list):
    try:
        #по роботу
        dealID = prepareBody[2].split('DEAL_')[1]
    except:
        # по кнопке
        dealID = int(eval(prepareBody[6].replace("'", '').split('=')[1])['ID'])
    return dealID


def main():
    pass

def handler(event, content):
    #event = prepare_body(event)
    #dealID = get_deal_id(event)
    dealID = 34241 
    deal = bit.callMethod('crm.deal.get', ID=dealID)
    print(f'{deal=}')
    print(f'{menedgers=}')
    if deal['CATEGORY_ID'] == '0': 
        menedgers = get_assigned_graph_menedger()
    
    elif deal['CATEGORY_ID'] == '3':
        menedgers = get_assigned_graph_admin()
    else:
        print('ID', deal['ID'])
        print('category ', deal['CATEGORY_ID'])
    

    #update_deal(menedgers,deal)

    main()

    return {"statusCode": 200, "body": "Производится обновление"}

handler(1,1)