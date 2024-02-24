import re
from telethon.sync import TelegramClient
from telethon import events, Button
import configparser
from t import *
import sys
import json
import os
import logging
from phone_iso3166.country import *










logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']
client = TelegramClient('ownsession/signbot', api_id, api_hash)

token = config['Token']['signbot']
#channel = config['App']['channel']
idbot =  int(token.split(':')[0])

client.start(bot_token=token)
client.connect()
dev = json.loads(config['App']['dev'])



check = [
            [Button.inline('تأكيد الحساب', "check")]
    ]
keyboard = [
                [Button.text("تسجيل حساب جديد", resize=True)],
            ]
@client.on(events.NewMessage())
async def main(event):
    chattt = await event.get_chat()
    if chattt.__class__.__name__ != 'User':
        return
        
    try:
        b = event.message.peer_id.channel_id
        b = f"-100{b}"
    except:
        pass

    ms_id = event.message.id
    text = event.raw_text.split("\n")[0]
    cleantext = event.raw_text
    fid = event.sender_id
    chat = event.chat_id
    ex = text.split("-")
    getdata = get(str(fid), "sql/cache_code.sqlite3") or 'None|None'
    data = getdata.split('|')
    if fid == idbot:
        return

    if fid not in dev:
        return

    if fid in dev:
        if text == 'c':
            await client.disconnect()
            return
    ban = read('data/ban.txt')
    ban = ban.split("\n")
    

    if str(fid) in ban:
        await event.reply('قد تم حظرك من البوت')
        return
# start
    resatart = [
                [Button.text("إلغاء العملية", resize=True)]
            ]

    sms = [
                [Button.inline('إضغط لإرسال الكود برسالة sms',"sms")]
            ]
  
    usersbot = read('data/memberssignbot.txt')
    usersbot = usersbot.split("\n")
    if str(fid) not in usersbot:
        file_append('data/memberssignbot.txt', str(fid) + "\n")  

    if fid in dev:
        exx = text.split(' ')
        if text == '/admin':
            luser = len(usersbot)
            allaccount = len(read('data/all.txt').split("\n")) - 1
            await event.reply(f"""
أهلا بك

عدد المشتركين : {luser}
عدد الأرقام في السيرفر : {allaccount}

لإرسال رسالة جماعية :
/send مرحبا بكم

عضوية
/pro id_user

إلغاء عضوية
/del id_user

تعيين رسالة اسعار الدول
/ms abc def.....
            """)

        if exx[0] == '/send':
            r = cleantext.replace('/send', '').replace("\n", 'BBBBBCCCC')
            await event.reply('جار الإرسالٍ')
            send_shell('loopsendsignbot.py', r)
        
        if exx[0] == '/ms':
            r = cleantext.replace('/ms ', '')
            file_put('ms.txt', r)
            await event.reply('تم الحفظ')
            return


        
        if exx[0] == '/pro' and exx[1] != '':
            put(str(exx[1]), 'pro', "sql/users.sqlite3")
            await event.reply('تم ترقية العضو')
            await client.send_message(int(exx[1]), "تمت ترقية حسابك")
            return

        if exx[0] == '/del' and exx[1] != '':
            put(str(exx[1]), 'None', "sql/users.sqlite3")
            await event.reply('تم إلغاء ترقية العضو')
            await client.send_message(int(exx[1]), "تمت إلغاء ترقية حسابك")
            return

        if exx[0] == '/ban':
            file_append('data/c.txt', exx[1]+',')
            await event.reply('تم')
            return
        if exx[0] == '/unban':
            r = read('data/c.txt')
            file_put('data/c.txt', r.replace(exx[1]+',', ''))
            await event.reply('تم')
            return

            
    if text == 'c' and fid in dev:
        await event.reply('ok')
        await client.disconnect()
    is_pro = get(str(fid), "sql/users.sqlite3")

        
    if text == '/start':
        await event.reply(f"""
مرحباً بك في بوت التسليم

        """, buttons=keyboard)
        return

    if text == 'إلغاء العملية':
        try:
            numbb = 5290173737
            numb = numbb[-7:]
            try:
                os.remove('ses/'+data[1]+'.session')
            except:
                pass
            ev = read('data/numbers.txt').replace(numb, '')
            file_put('data/numbers.txt', ev)
        except:
            pass
        put(str(fid), 'None|None', "sql/cache_code.sqlite3")
        await event.reply('''
مرحباً بك في بوت التسليم

        ''', buttons=keyboard)
        return


    if text == 'تسجيل حساب جديد':
        put(str(fid), 'new|', "sql/cache_code.sqlite3")
        await event.reply(""""
ارسل الرقم مسبوقا بنداء الدولة
        
مثال :
+963951674345
        
        """ , buttons=resatart)
        return


    if text and data[0] == 'new':
        checknumber = read('data/numbers.txt').split("\n")
        text = '+' + text.replace(' ', '').replace('-', '').replace(')', '').replace('(', '').replace('.', '').replace('+00', '').replace('+0', '').replace('+', '')
        fone = text.replace(' ', '').replace('-', '').replace(')', '').replace('(', '').replace('.', '').replace('+00', '').replace('+0', '').replace('+', '')
        tel = text[-7:]
        if not is_int(fone):
            await event.reply('يرجى إرسال رقم صحيح')
            return
        if tel in checknumber:
            await event.reply('الرقم مسجل مسبقا!، ارسل رقم آخر…')
            return
        if is_pro != 'pro' and fid not in dev:
            if phone_country(fone) in read('data/c.txt').split(','):
                await event.reply('هذه الدولة محظورة، لا يمكنك تفعيل الأرقام من هذه الدولة..')
                return
        if cleantext[0] != '+':
            await event.reply("""
يرجى ارسال الرقم مسبوقا بنداء الدولة و +

مثال :
+967737669980
            """) 
            return
        await event.reply('انتظر قليلا جار المعالجة...')
        send_shell('py', 'sign.py', 'new', text, str(fid))
    
    if text and data[0] == 'code':
        if not is_int(text):
            await event.reply('أرقام فقط...')
            return
        c = text.replace('a', '1').replace('b', '2').replace('c', '3').replace('d', '4').replace('e', '5').replace('f', '6').replace('g', '7').replace('h', '8').replace('i', '9').replace('j', '0')
        await event.reply('سيتم التحقق من الكود انتظر قليلا...')
        put(str(fid), 'addcode|'+c, "sql/cache_code.sqlite3")
        return

    if text and data[0] == 'pass':
        await event.reply('سيتم التحقق من كلمة المرور انتظر قليلا...')
        put(str(fid), 'addpass|'+text, "sql/cache_code.sqlite3")
        return

    if text == '/check' and data[0] == 'checking':
        await event.reply('انتظر قليلا...')
        return

    if text == '/check' and data[0] == 'check':
        #put(str(fid), 'checking|None', "sql/cache_code.sqlite3")
        await event.reply('سيتم التحقق من الحساب انتظر قليلا...')
        send_shell('python3', 'check.py', data[1], str(fid), data[2])
        #put(str(fid), 'addpass|'+text, "sql/cache_code.sqlite3")
        return


# تحديد المسار الصحيح للمجلد
path_to_sessions_folder = os.path.join(os.getcwd(), 'sessions')

# إنشاء المجلد
# عدد الملفات الموجودة في المجلد
c = len(os.listdir(path_to_sessions_folder))

config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']
session_name = 'add_user.session'
client = TelegramClient(session_name, api_id, api_hash)

token = config['Token']['mybot']
#channel = config['App']['channel']
idbot =  int(token.split(':')[0])

client.start(bot_token=token)
dev = json.loads(config['App']['dev'])

arg = sys.argv

start = [
            [Button.inline('بدء عملية نقل جديدة', "start")],
            [Button.inline('بدء رسائل إزعاج', "ms")],
    ]
back = [
            [Button.inline('إلغاء ورجوع', "back")]
    ]

sub = [
            [Button.inline('بدء', "sub")]
]
sub2 = [
            [Button.inline('بدء', "sub2")]
]
sub.append(back[0])


@client.on(events.NewMessage())
async def main(event):
    chattt = await event.get_chat()
    if chattt.__class__.__name__ != 'User':
        return
        
    try:
        b = event.message.peer_id.channel_id
        b = f"-100{b}"
    except:
        pass

    ms_id = event.message.id
    text = event.raw_text.split("\n")[0]
    cleantext = event.raw_text
    fid = event.sender_id
    chat = event.chat_id
    ex_text = text.split("_")
    try:
        sql_data = get(str(fid))
        ex = sql_data.split('|')
    except:
        ex = [None, None]
    if fid == idbot:
        return

    if fid not in dev:
        return
    
    if text == '/start':
        put(str(fid), 'None|None')
        await event.reply('أهلا بك', buttons=start)
        return
    #command|url1|num of account|url2|time|num of members

    if text and ex[0] == 'start':
        if is_urls(text):
            if is_tele(text):
                put(str(fid), 'start2|'+text)
                c = len(os.listdir('sessions'))
                await event.reply(f'ارسل عدد الحسابات.. \n\n عدد الحسابات الحالي تقريبا : {c}', buttons=back)
            else:
                await event.reply('أرسل روابط تليجرام حصرا..', buttons=back)
        else:
            await event.reply('أرسل روابط حصرا..', buttons=back)
            return
    
    if text and ex[0] == 'start2':
        if is_int(text):
            put(str(fid), 'start3|'+ex[1]+'|'+text)
            await event.reply('أرسل رابط القروب للنقل إليه', buttons=back)
            return
        else:
            await event.reply('أرسل أرقاما حصرا..', buttons=back)
            return


    if text and ex[0] == 'start3':
        if is_urls(text):
            if is_tele(text):
                put(str(fid), 'start4|'+ex[1]+'|'+ex[2]+'|'+text)
                await event.reply(f'أرسل التوقيت بين الإضافة والأخرى بالثواني حصرا\n\nتجنب الأرقام العشرية : 0.2', buttons=back)
            else:
                await event.reply('أرسل روابط تليجرام حصرا..', buttons=back)
        else:
            await event.reply('أرسل روابط حصرا..', buttons=back)
            return
    

    if text and ex[0] == 'start4':
        if is_int(text):
            put(str(fid), 'start5|'+ex[1]+'|'+ex[2]+'|'+ex[3]+'|'+text)
            await event.reply("""
أرسل عدد الأعضاء التي تريد نقلها..

من أجل الحد الأقصى أرسل عددا كبيرا: 1000000
            """, buttons=back)
        else:
            await event.reply('أرسل أرقاما حصرا..', buttons=back)
            return

    #command|url1|num of account|url2|time|num of members
    if text and ex[0] == 'start5':
        if is_int(text):
            put(str(fid), 'sub|'+ex[1]+'|'+ex[2]+'|'+ex[3]+'|'+ex[4]+'|'+text)
            await event.reply(f"""
هل تريد بدء اشتراك الحسابات..؟؟

نقل من : {ex[1]}
نقل إلى : {ex[3]}
عدد الحسابات : {ex[2]}
وقت الإضافة : {ex[4]}
عدد الأعضاء المراد نقلها : {text}
            """, buttons=sub)
        else:
            await event.reply('أرسل أرقاما حصرا..', buttons=back)
            return
    
    if text == '/check':
        await event.reply('جار التحقق من الحسابات..')
        send_shell('python', 'command.py', 'check', str(fid))

        return
    if ex_text[0] == '/left':
        send_shell('python3', 'command.py', 'left', str(fid), ex_text[1])
        await event.reply('جار المغادرة..')
        return
    
    if ex_text[0] == '/begin':
        send_shell('python', 'command.py', 'begin', str(fid), ex_text[1])
        await event.reply('ok_>>')
        return

    if ex_text[0] == '/beginsend':
        send_shell('python3', 'command.py', 'beginsend', str(fid), ex_text[1])
        await event.reply('ok_>>')
        return


    if text and ex[0] == 'ms':
        if is_urls(text):
            if is_tele(text):
                put(str(fid), 'ms2|'+text)
                c = len(os.listdir('sessions'))
                await event.reply(f'ارسل عدد الحسابات.. \n\n عدد الحسابات الحالي تقريبا : {c}', buttons=back)
            else:
                await event.reply('أرسل روابط تليجرام حصرا..', buttons=back)
        else:
            await event.reply('أرسل روابط حصرا..', buttons=back)
            return

    if text and ex[0] == 'ms2':
        if is_int(text):
            put(str(fid), 'ms3|'+ex[1]+'|'+text)
            await event.reply('أرسل عدد الثواني sleep', buttons=back)
            return
        else:
            await event.reply('أرسل أرقاما حصرا..', buttons=back)
            return

    if text and ex[0] == 'ms3':
        if is_int(text):
            put(str(fid), 'ms4|'+ex[1]+'|'+ex[2]+'|'+text)
            await event.reply('أرسل عدد الأعضاء لإرسال الرسالة لهم', buttons=back)
            return
        else:
            await event.reply('أرسل أرقاما حصرا..', buttons=back)
            return

    if text and ex[0] == 'ms4':
        if is_int(text):
            put(str(fid), 'ms5|'+ex[1]+'|'+ex[2]+'|'+ex[3]+'|'+text)
            await event.reply('ارسل الإعلان ، نص فقط', buttons=back)
            return
        else:
            await event.reply('أرسل أرقاما حصرا..', buttons=back)
            return

    if text and ex[0] == 'ms5':
        put(str(fid), 'sub2|'+ex[1]+'|'+ex[2]+'|'+ex[3]+'|'+ex[4]+'|'+cleantext)
        await event.reply(f'''
هل تريد بدء اشتراك الحسابات..؟؟

الرابط: {ex[1]}
عدد الحسابات: {ex[2]} 
عدد الثواني: {ex[3]}
عدد الأعضاء: {ex[4]}
الرسالة : {cleantext}

        ''', buttons=sub2)
        return


@client.on(events.CallbackQuery)
async def callback(event):

    try:
        chat = event.original_update.peer.user_id
        dataa = event.data
        data = dataa.decode("utf-8")
        ex = data.split("-")
    except:
        data = False
    fid = event.sender_id

    try:
        sql_data = get(str(fid))
        print(sql_data)
        ex = sql_data.split('|')
    except Exception as es:
        print(es)
        ex = [None, None]

    

    if data == 'back':
        put(str(fid), 'None|None')
        await event.edit('أهلا بك', buttons=start)

    if data == 'start':
        put(str(fid), 'start|')
        await event.edit('أرسل رابط القروب للنقل منه..', buttons=back)

    if data == 'sub' and ex[0] == 'sub':
        #command|url1|num of account|url2|time|num of members
        url1 = ex[1]
        num_of_ac = ex[5]
        url2 = ex[3]
        times = ex[4]
        num = ex[2]
        await event.answer('جار دخول الحسابات', alert=True, cache_time=100)
        send_shell('python', 'command.py', 'join', num, str(fid), url1, url2, num_of_ac, times)
        pass

    if data == 'sub' and ex[0] != 'sub':
        await event.answer('بيانات خاطئة', alert=True)
        pass



    if data == 'sub2' and ex[0] == 'sub2':
        #command | url1 | num of ac | sec | num numbers | ad
        url1 = ex[1]
        num_of_ac = ex[4]
        url2 = url1
        times = ex[3]
        num = ex[2]
        ad = randtext(5)
        put(ad, ex[5])
        await event.answer('جار دخول الحسابات', alert=True, cache_time=100)
        send_shell('python3', 'command.py', 'join2', num, str(fid), url1, url2, num_of_ac, times, ad)
        pass

    if data == 'sub2' and ex[0] != 'sub':
        await event.answer('بيانات خاطئة', alert=True)
        pass

    
    if data == 'ms':
        put(str(fid), 'ms|')
        await event.edit('أرسل رابط القروب..', buttons=back)
    

client.run_until_disconnected()