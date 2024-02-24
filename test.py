from pyrogram import Client

api_id =  23400083
api_hash = '0e74273597062392e2132f1f0e1edd9e'
app = Client('sessions/aeoenzbxsx', api_id=api_id, api_hash=api_hash)
app.connect()

app.send_message('@vvu1l', 'hello')

app.disconnect()
