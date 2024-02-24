from pyrogram import Client
from pyrogram.raw import functions
import sys, os
import configparser
import asyncio
import logging
from t import is_tele
from pyrogram.errors import FloodWait, UserPrivacyRestricted, UserRestricted, PeerFlood, UserNotMutualContact, UserChannelsTooMuch
from t import get




logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

config = configparser.ConfigParser() 
config.read("config.ini")

api_id = config['App']['id']
api_hash = config['App']['hash']

arg = sys.argv
command = arg[1]
ses = arg[2].split('.')[0]


async def apicodetelegramchannel():
    try:
        app = Client('sessions/'+ses, api_id=api_id, api_hash=api_hash)
        cc = await app.connect()
        if command == 'check':
            try:
                await app.get_me()
                print('true')
            except:
                print('false')
        await app.get_me()
    except Exception as d:
        er = str(d).replace('Telegram says: ', '').split(' - ')
        if er[0] in ['[401 AUTH_KEY_UNREGISTERED]', '[401 USER_DEACTIVATED]', '[401 USER_DEACTIVATED_BAN]', '[401 SESSION_REVOKED]']:
            try:
                os.remove('sessions/'+ses+'.session')
            except:
                pass
        if command == 'check':
            print(er[0])

        print('false', d)
        cc = False
        return
    if not cc:
        print('false', 'hmmmm')
        return
    
    try:
        await app.invoke(functions.account.UpdateStatus(
            offline=False
        ))
    except:
        pass

    if command == 'join':
        url1 = is_tele(arg[3])[1]
        if arg[3] == arg[4]:
            url2 = url1
        else:
            url2 = is_tele(arg[4])[1]
        print(url1, url2)
        try:
            x1 = await app.join_chat(url1)
            if arg[3] == arg[4]:
                x2 = x1
            else:
                x2 = await app.join_chat(url2)
            print('true')
            print(x1.id)
            print(x2.id)
        except Exception as er:
            print('false', er)
            pass
    #await app.add_chat_members()
    if command == 'left':
        url1 = int(arg[3])
        url2 = int(arg[4])
        try:
            await app.leave_chat(url1)
            if arg[3] != arg[4]:
                await app.leave_chat(url2)
            print('true')
        except Exception as er:
            print('false', er)
            pass
        pass


    if command == 'getusers':
        ig = int(arg[3])
        ig2 = int(arg[4])
        #id = arg[4]
        users = ''
        users_list = []
        try:
            geting2 = app.get_chat_members(ig2)#, filter=enums.ChatMembersFilter.RECENT)
            #print(geting)
            async for m2 in geting2:
                #print(m)
                #print(m.user.phone_number)
                if m2.user.username is not None:
                    users_list.append(m2.user.username)
                else:
                    if m2.user.phone_number is not None:
                        users_list.append(m2.user.phone_number)
                pass
            
            geting = app.get_chat_members(ig)#, filter=enums.ChatMembersFilter.RECENT)
            #print(geting)
            async for m in geting:
                #print(m)
                #print(m.user.phone_number)
                if m.user.username is not None:
                    if m.user.username not in users_list:
                        users += "@"+str(m.user.username)+','
                else:
                    if m.user.phone_number is not None:
                        if m.user.phone_number not in users_list:
                            users += "+"+str(m.user.phone_number)+','
                pass

                
            print('true')
            print(users)
        except:
            print('false')

            pass

    if command == 'getusers2':
        ig = int(arg[3])
        #ig2 = int(arg[3])
        #id = arg[4]
        users = ''
        try:
            geting = app.get_chat_members(ig)#, filter=enums.ChatMembersFilter.RECENT)
            #print(geting)
            async for m in geting:
                #print(m)
                #print(m.user.phone_number)
                if m.user.username is not None:
                    users += "@"+str(m.user.username)+','
                else:
                    if m.user.phone_number is not None:
                        users += "+"+str(m.user.phone_number)+','
                pass
                
            print('true')
            print(users)
        except:
            print('false')

            pass
    #await app.add_chat_members()

    if command == 'adduser':
        id_g = arg[3]
        user_add = arg[4]
        try:
            #await app.add_contact(user_add)
            await app.add_chat_members(int(id_g), user_add)
            print('true')
        except FloodWait as e:
            print('flood')
            print(ses)
        except PeerFlood as e:
            print('flood')
            print(ses)
        except UserPrivacyRestricted as et:
            #print()
            print('continue')
        except UserNotMutualContact as et:
            print('continue')
        except UserChannelsTooMuch as et:
            print('continue')
        except Exception as er:
            print(er, 'all')
        pass


    if command == 'send':
        ad = arg[3]
        ads = get(ad)
        user_for_send = arg[4]
        try:
            #await app.add_contact(user_add)
            await app.send_message(user_for_send, ads)
            print('true')
        except FloodWait as e:
            print('flood')
            #print(ses)
        except UserRestricted as et:
            #print()
            print('continue')
        except PeerFlood as et:
            print('flood')
        except Exception as er:
            print(er, 'all')
        pass


asyncio.get_event_loop().run_until_complete(apicodetelegramchannel())