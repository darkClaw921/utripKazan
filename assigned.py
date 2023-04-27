import datetime
from bitrix24 import Bitrix24
from pprint import pprint
from ForWorkGSheet import Sheet
import math
import os

bit = Bitrix24(os.environ.get('webHook'))

# кто на кого меняет
menagers = {1: 9,
            9: 1}

admins = {1: 9,
          9: 1}

week = {
    1: ['B', 'C', 'D', 'E', 'F', 'G', 'H'],
    2: ['J', 'K', 'L', 'M', 'N', 'O', 'P'],
    3: ['R', 'S', 'T', 'U', 'V', 'W', 'X'],
    4: ['Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF'],
    5: ['AH', 'AI', 'AJ', 'AK', 'AL', 'AM', 'AN'],
}

today = datetime.date.today()
SHEET_NAME = 'copy_graphik'
PATH_JSON_ACCAUNT = 'kgtaprojects-8706cc47a185.json'
listName = 'Апрель'
sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)


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


def get_deals_meneger(users: list):
    col = get_col_name()
    print(f'попали в менеджеров {col} {users}')
    
    deals = bit.callMethod('crm.deal.list',
                            FILTER={'STAGE_SEMANTIC_ID': 'P',
                                    #'ASSIGNED_BY_ID': menagers[user],
                                    'CATEGORY_ID': 0,
                                    # '!STAGE_ID': 'что-то', })
                                    '!UF_CRM_1680207208770': today})
    
    try:
        count = math.ceil(len(deals) / len(users))
    except ZeroDivisionError:
        print(f'{count=}')
        return 0 

    countUpdate = 0
    #print(f'{deals=}')
    indexUser = 0
    print(f'{len(deals)=}')
    print(f'{count=}')
    
    for deal in deals:
        print(deal['CONTACT_ID'])
        print(deal['ID'])
        try:
            bit.callMethod('crm.contact.update', ID=deal['CONTACT_ID'], fields={
                'ASSIGNED_BY_ID': str(users[indexUser]),
                #'UF_CRM_1680207208770': today,
            })
        except:
            continue
        bit.callMethod('crm.deal.update', ID=deal['ID'], fields={
                'ASSIGNED_BY_ID': str(users[indexUser]),
                'UF_CRM_1680207208770': today,})
            #print(f'обновили {deal["ID"]} для {user}')
        countUpdate +=1
        if countUpdate >= count:
            print(f'{countUpdate=}')
            print(f'добавили пользователю {users[indexUser]} : {countUpdate} сделок')
            indexUser += 1
            countUpdate = 0
    try:
        print(f'сделки кончились добавили пользователю {users[indexUser]} : {countUpdate} сделок')
    except IndexError: 
        print(f'сделки кончились добавили пользователю {users[indexUser-1]} : {countUpdate} сделок')
            


def get_deals_admin_cate3(users: list):
    col = get_col_name()
    print(f'попали в admin_Cat3 {col} {users}')
    
    deals = bit.callMethod('crm.deal.list',
                            FILTER={'STAGE_SEMANTIC_ID': 'P',
                                    #'ASSIGNED_BY_ID': menagers[user],
                                    'CATEGORY_ID': 3,
                                    # '!STAGE_ID': 'что-то', })
                                    '!UF_CRM_1680207208770': today})
    
    try:
        count = math.ceil(len(deals) / len(users))
    except ZeroDivisionError:
        print(f'{count=}')
        return 0 
    countUpdate = 0
    #print(f'{deals=}')
    indexUser = 0
    print(f'{len(deals)=}')
    print(f'{count=}')

    for deal in deals:
        try:
            bit.callMethod('crm.contact.update', ID=deal['CONTACT_ID'], fields={
                'ASSIGNED_BY_ID': str(users[indexUser]),
                #'UF_CRM_1680207208770': today,
            })
        except:
            continue
        bit.callMethod('crm.deal.update', ID=deal['ID'], fields={
                'ASSIGNED_BY_ID': str(users[indexUser]),
                'UF_CRM_1680207208770': today,})
            #print(f'обновили {deal["ID"]} для {user}')
        countUpdate +=1
        if countUpdate >= count:
            print(f'{countUpdate=}')
            print(f'добавили пользователю {users[indexUser]} : {countUpdate} сделок')
            indexUser += 1
            countUpdate = 0
    try:
        print(f'сделки кончились добавили пользователю {users[indexUser]} : {countUpdate} сделок')
    except IndexError: 
        print(f'сделки кончились добавили пользователю {users[indexUser-1]} : {countUpdate} сделок')




def get_deals_admin_cate5(users: list):
    col = get_col_name()
    print(f'попали в admin_cat5 {col} {users}')
    
    deals = bit.callMethod('crm.deal.list',
                            FILTER={'STAGE_SEMANTIC_ID': 'P',
                                    #'ASSIGNED_BY_ID': menagers[user],
                                    'CATEGORY_ID': 5,
                                    # '!STAGE_ID': 'что-то', })
                                    '!UF_CRM_1680207208770': today})
    
    try:
        count = math.ceil(len(deals) / len(users))
    except ZeroDivisionError:
        print(f'{count=}')
        return 0 
        
    countUpdate = 0
    #print(f'{deals=}')
    indexUser = 0
    print(f'{len(deals)=}')
    print(f'{count=}')

    for deal in deals:
        try:
            bit.callMethod('crm.contact.update', ID=deal['CONTACT_ID'], fields={
                'ASSIGNED_BY_ID': str(users[indexUser]),
                #'UF_CRM_1680207208770': today,
            })
        except:
            continue
            
        bit.callMethod('crm.deal.update', ID=deal['ID'], fields={
                'ASSIGNED_BY_ID': str(users[indexUser]),
                'UF_CRM_1680207208770': today,
            })
            #print(f'обновили {deal["ID"]} для {user}')
        countUpdate +=1
        if countUpdate >= count:
            print(f'{countUpdate=}')
            print(f'добавили пользователю {users[indexUser]} : {countUpdate} сделок')
            indexUser += 1
            countUpdate = 0
            
    try:
        print(f'сделки кончились добавили пользователю {users[indexUser]} : {countUpdate} сделок')
    except IndexError: 
        print(f'сделки кончились добавили пользователю {users[indexUser-1]} : {countUpdate} сделок')

def get_users():
    prepareUser = []
    users = bit.callMethod('user.get', FILTER ={'ACTIVE':True})
    for user in users:
        prepareUser.append(f'[{user["ID"]}] {user["NAME"]}')
    return prepareUser

def update_user():
    users = get_users()
    listName = 'users'
    sheetUser = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)
    for i, user in enumerate(users):
        sheetUser.send_cell(f'G{i+2}', user)
    

def main():
    col = get_col_name()
    usersMenedger = get_assigned_graph_menedger()
    print(f'{usersMenedger=}')
    get_deals_meneger(usersMenedger)

    userAdmins = get_assigned_graph_admin()
    print(f'{userAdmins=}')
    get_deals_admin_cate3(userAdmins)
    get_deals_admin_cate5(userAdmins)

def handler(event, context):
    #get_assigned_graph_menedger()
    main()
    #update_user()
    
    
    #maxUser = sheet.find_cell('Админы').row - 3
    #print(f'{maxUser=}')
    return {
        'statusCode': 200,
        'body': 'Производится обновление',
    }

