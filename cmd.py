from pydoc import cli
from telethon.sync import TelegramClient
import time
from t import *
import sys, os, random, requests, configparser, json

config = configparser.ConfigParser() 
config.read("config.ini")

token = config['Token']['mybot']
api_id = config['App']['id']
api_hash = config['App']['hash']

arg = sys.argv
command = arg[1]


def sendms(chat_id, text):
    URL = "https://api.telegram.org/bot"+token+"/sendmessage"
    PARAMS = {'chat_id': chat_id, 'text': text}
    requests.get(url=URL, params=PARAMS)

id = randtext(6)
sessions = os.listdir('sessions')
random.shuffle(sessions)

count = len(sessions)

if command == 'join':
    num = int(arg[2])
    user = arg[3]
    url1 = arg[4]
    url2 = arg[5]
    num_of_ac = arg[6]
    times = arg[7]
    put(id, str(num)+'|'+user+'|'+url1+'|'+url2+'|'+num_of_ac+'|'+times, "sql/cache2.sqlite3")
    join = 0
    for i in sessions:
        if join == num:
            break
        
        ses = i.split('.')[0]
        c = 'false'
        c = send_command('add_user.py', 'join', i, url1, url2)
        print(c)
        sp = c.split("\n")
        if 'true' in sp:
            if sp[0] == 'true':
                id1 = sp[1]
                id2 = sp[2]
            else:
                id1 = sp[2]
                id2 = sp[3]
            join += 1
            g = get(id)
            for_leave = ses+"|"+id1+"|"+id2
            if g == 0:
                put(id, for_leave+',')
            else:
                ss = get(id)
                put(id, ss+for_leave+',')
        else:
            pass
    sendms(user, f"""
تم تنفيذ أمر الأشتراك

عدد الحسابات المشتركة : {join}

أمر المغادرة
/left_{id}

يتم الان جلب أعضاء الكروب وتخزينها..
    """)
    get_sessions = str(get(id)).split(',')
    for ii in get_sessions:
        spl = ii.split('|')
        s = spl[0]
        ig = spl[1]
        ig2 = spl[2]
        c2 = send_command('add_user.py', 'getusers', s, ig, ig2)
        ex = c2.split("\n")
        if 'true' in ex:
            put(id, ex[1], 'sql/users.sqlite3')
            counts = len(str(ex[1]).split(','))
            sendms(user, f"""
تم تنفيذ أمر جلب الأعضاء

عدد الأعضاء : {counts}

بدء النقل
/begin_{id}

    """)
            break

if command == 'join2':
    num = int(arg[2])
    user = arg[3]
    url1 = arg[4]
    url2 = url1
    num_of_ac = arg[6]
    times = arg[7]
    ad = arg[8]
    put(id, str(num)+'|'+user+'|'+url1+'|'+url2+'|'+num_of_ac+'|'+times+'|'+ad, "sql/cache2.sqlite3")
    join = 0
    for i in sessions:
        if join == num:
            break
        
        ses = i.split('.')[0]
        c = 'false'
        c = send_command('add_user.py', 'join', i, url1, url2)
        print(c)
        sp = c.split("\n")
        if 'true' in sp:
            if sp[0] == 'true':
                id1 = sp[1]
                id2 = sp[2]
            elif sp[1] == 'true':
                id1 = sp[2]
                id2 = sp[3]
            else:
                id1 = sp[3]
                id2 = sp[4]
            join += 1
            g = get(id)
            for_leave = ses+"|"+id1+"|"+id2
            if g == 0:
                put(id, for_leave+',')
            else:
                ss = get(id)
                put(id, ss+for_leave+',')
        else:
            pass
    sendms(user, f"""
تم تنفيذ أمر الأشتراك

عدد الحسابات المشتركة : {join}

أمر المغادرة
/left_{id}

يتم الان جلب أعضاء الكروب وتخزينها..
    """)
    get_sessions = str(get(id)).split(',')
    for ii in get_sessions:
        spl = ii.split('|')
        s = spl[0]
        ig = spl[1]
        ig2 = spl[2]
        c2 = send_command('add_user.py', 'getusers2', s, ig, ig2)
        ex = c2.split("\n")
        if 'true' in ex:
            put(id, ex[1], 'sql/users.sqlite3')
            counts = len(str(ex[1]).split(','))
            sendms(user, f"""
تم تنفيذ أمر جلب الأعضاء

عدد الأعضاء : {counts}

بدء الإرسال
/beginsend_{id}

    """)
            break
    


if command == 'left':
    user = arg[2]
    id = arg[3]
    get_sessions = str(get(id)).split(',')
    #print(get_sessions)
    for ii in get_sessions:
        if ii == '':
            continue
        spl = ii.split('|')
        s = spl[0]
        ig = spl[1]
        ig2 = spl[2]
        c2 = send_command('add_user.py', 'left', s, ig, ig2)
    sendms(user, f"""
تم المغادرة بنجاح..
""")
    pass

if command == 'begin':
    added = 0
    added_ok = 0
    ban_ac = []
    p_user = 0
    user = arg[2]
    id = arg[3]
    try:
        client = TelegramClient('ownsession/'+id, api_id, api_hash)
        client.start(bot_token=token)
        ms = client.send_message(int(user), 'بدأ النقل سأخبرك بهذه الرسالة جميع التفاصيل..')
    except Exception as er:
        print(er, 'Error Bot')
        pass
    get_sessions = str(get(id)).split(',')
    #put(id, str(num)+'|'+user+'|'+url1+'|'+url2+'|'+num_of_ac+'|'+times, "sql/cache2.sqlite3")
    get_info = str(get(id, "sql/cache2.sqlite3")).split("|")
    id_g = get_info[3]
    num_of_ac = get_info[4]
    times = get_info[5]
    all_users = str(get(id, 'sql/users.sqlite3')).split(',')
    dis = False
    while True:
        for ii in get_sessions:
            if ii == '':
                continue
            spl = ii.split('|')
            s = spl[0]
            ig = spl[1]
            ig2 = spl[2]
            add = send_command('add_user.py', 'adduser', s, ig2, all_users[added]) 
            print(add)
            exp = add.split("\n")
            if exp[0] == 'true':
                added_ok += 1
                added += 1
            if exp[0] == 'flood':
                #added +=1
                if exp[1] not in ban_ac:
                    ban_ac.append(exp[1])
                continue
            if exp[0] == 'continue':
                added +=1
                p_user += 1
                continue

            if exp[0] not in ['true', 'flood', 'continue']:
                added +=1
                p_user += 1
                continue
            
            time.sleep(int(times))

            
            if len(all_users) == (added + 1):
                dis = True
                break
            
            if added_ok == int(num_of_ac):
                dis = True
                break
            if len(ban_ac) == int(num_of_ac):
                dis = True
                break
        client.edit_message(ms, f"""
العدد الكلي : {len(all_users)}
نم نقل حتى الان : {added_ok}

وصل إلى العدد : {added}

عدد الأعضاء التي لا يمكن إضافتها : {p_user}
عدد الحسابات التي انحظرت مؤقتا : {len(ban_ac)}


{dis}
آخر خطأ
{add}
        """+randtext(3))
        if dis:
            client.edit_message(ms, f"""
انتهى النقل..
العدد الكلي : {len(all_users)}
نم نقل حتى الان : {added_ok}

وصل إلى العدد : {added}

عدد الأعضاء التي لا يمكن إضافتها : {p_user}
عدد الحسابات التي انحظرت مؤقتا : {len(ban_ac)}

{dis}
            """+randtext(3))
            client.disconnect()
            break



if command == 'beginsend':
    added = 0
    added_ok = 0
    ban_ac = []
    p_user = 0
    user = arg[2]
    id = arg[3]
    try:
        client = TelegramClient('ownsession/'+id, api_id, api_hash)
        client.start(bot_token=token)
        ms = client.send_message(int(user), 'بدأ الإرسال.. سأخبرك بهذه الرسالة جميع التفاصيل..')
    except Exception as er:
        print(er, 'Error Bot')
        pass
    get_sessions = str(get(id)).split(',')
#put(id, str(num)+'|'+user+'|'+url1+'|'+url2+'|'+num_of_ac+'|'+times+'|'+ad, "sql/cache2.sqlite3")
    get_info = str(get(id, "sql/cache2.sqlite3")).split("|")
    id_g = get_info[2]
    num_of_ac = get_info[4]
    times = get_info[5]
    ad = get_info[6]
    all_users = str(get(id, 'sql/users.sqlite3')).split(',')
    dis = False
    while True:
        for ii in get_sessions:
            if ii == '':
                continue 
            spl = ii.split('|')
            s = spl[0]
            ig = spl[1]
            ig2 = spl[2]
            add = send_command('add_user.py', 'send', s, ad, all_users[added])
            print(add)
            exp = add.split("\n")
            if exp[0] == 'true':
                added_ok += 1
            if exp[0] == 'flood':
                if exp[1] not in ban_ac:
                    ban_ac.append(exp[1])
                continue
            if exp[0] == 'continue':
                p_user += 1
                continue
            time.sleep(int(times))

            added +=1
            if len(all_users) == (added + 1):
                dis = True
                break
            
            if added_ok == int(num_of_ac):
                dis = True
                break
            if len(ban_ac) == int(num_of_ac):
                dis = True
                break
        client.edit_message(ms, f"""
العدد الكلي : {len(all_users)}
نم الإرسال حتى الان إلى : {added_ok}

وصل إلى العدد : {added}

عدد الأعضاء التي لا يمكن إضافتها : {p_user}
عدد الحسابات التي انحظرت مؤقتا : {len(ban_ac)}

{dis}
        """)
        if dis:
            client.edit_message(ms, f"""
انتهى الإرسال..
العدد الكلي : {len(all_users)}
نم الإرسال حتى الان إلى : {added_ok}

وصل إلى العدد : {added}

عدد الأعضاء التي لا يمكن إضافتها : {p_user}
عدد الحسابات التي انحظرت مؤقتا : {len(ban_ac)}

{dis}
            """)
            client.disconnect()
            break

if command == 'check':
    ok = 0
    er = ''
    user = arg[2]
    for i in os.listdir('sessions'):
        add = send_command('add_user.py', 'check', i)
        exp = add.split("\n")
        if 'true' in exp:
            ok +=1
        else:
            if er not in er.split("\n"):
                er += exp[0]+"\n"
        pass
    
    sendms(user, f"""
انتهى الفحص..

عدد الحسابات الكلي : {len(os.listdir('sessions'))}

عدد الحسابات السليمة : {ok}

أخطاء الحسابات التي لا تعمل :

{er}
""")