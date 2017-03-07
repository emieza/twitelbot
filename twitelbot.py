#!/home/ubuntu/envTg/bin/python

from tokens import tgTokens, twitterTokens
import tweepy
import telepot
import redis, redisworks
import time, sys
from pprint import pprint

TW_ADD_STR = "/tadd @"
TW_DEL_STR = "/tdel @"
TW_LIST_STR = "/tlist"

root = redisworks.Root()
redisconn = redis.Redis()

# creem nou registre de xats actius
if not root.chats:
	root.chats = [ 0 ]

def tots_els_users():
	users = []
	if root.chats:
		for chat_id in root.chats:
			if chat_id and root[str(chat_id)]:
				for user in root[str(chat_id)]:
					users.append(user)
	return users
	
def contesta(msg):
	global stream
	content_type, chat_type, chat_id = telepot.glance(msg)
	#pprint(msg)

	# TODO: detectar si ens fan fora del xat per eliminar les dades

	# afegim el canal si cal
	chats = root.chats
	if chat_id not in chats:
		chats.append( chat_id )
		root.chats = chats
		#root[str(chat_id)] = []

	# processem comanda
	if msg["text"][0:len(TW_ADD_STR)]==TW_ADD_STR and len(msg["text"])>7:
		newuser = msg["text"][len(TW_ADD_STR):].lower()
		users = root[str(chat_id)]
		if not users:
			users = []
		if newuser in users:
			bot.sendMessage( chat_id, "@"+newuser+" ja estava subscrit" )
		else:
			users.append(newuser)
			root[str(chat_id)] = users
			bot.sendMessage( chat_id, "afegit @"+newuser)
			stream.disconnect()
			del stream
			stream = tweepy.Stream( auth=api.auth, listener=listener )
			stream.userstream( track=tots_els_users(), async=True )
	elif msg["text"][0:len(TW_DEL_STR)]==TW_DEL_STR and len(msg["text"])>7:
		newuser = msg["text"][len(TW_DEL_STR):].lower()
		users = root[str(chat_id)]
		if not users:
			users = []
		if newuser not in users:
			bot.sendMessage( chat_id, "@"+newuser+" no estava subscrit" )
		else:
			users.remove(newuser)
			if not users:
				redisconn.delete("root."+str(chat_id))
			else:
				root[str(chat_id)] = users
			bot.sendMessage( chat_id, "eliminat @"+newuser)
			stream.disconnect()
			stream.running = False
			del stream
			stream = tweepy.Stream( auth=api.auth, listener=listener )
			users = tots_els_users()
			if users:
				stream.userstream( track=users, async=True )
	elif msg["text"]==TW_LIST_STR:
		users = root[str(chat_id)]
		if not users:
			bot.sendMessage( chat_id, "Encara no segueixes cap usuari de Twitter")
		else:
			userstr = ""
			for user in users:
				#print( str(user) )
				userstr += str(user)+"\n"
			bot.sendMessage( chat_id, "Usuaris de Twitter seguits:\n"+userstr )
	else:
		bot.sendMessage( chat_id, """Comandes:
   %snomusuari : afegir un usuari de twitter
   %snomusuari : esborrar un usuari de twitter
   %s per veure els usuaris subscrits
""" % ( TW_ADD_STR, TW_DEL_STR, TW_LIST_STR ) )


class TuitListener(tweepy.StreamListener):
	def on_status(self, status):
		if not root.chats:
			return
		for chat_id in root.chats:
			if chat_id==0:
				continue
			users = root[str(chat_id)]
			if users and status.user.screen_name.lower() in users:
				#print("["+ status.user.screen_name +"]: "+ status.text)
				bot.sendMessage( str(chat_id), "[Twitter:@"+status.user.screen_name+"]\n"+status.text )


auth = tweepy.OAuthHandler( twitterTokens["consumer_key"], twitterTokens["consumer_secret"] )
auth.set_access_token( twitterTokens["access_token"],  twitterTokens["access_secret"] )
api = tweepy.API(auth)

# twitter stream
listener = TuitListener()
stream = tweepy.Stream( auth=api.auth, listener=listener )
# bot
bot = telepot.Bot(tgTokens["mybot1"])

# engeguem real-time
bot.message_loop(contesta)
# carreguem usuaris seguits inicialment
users = tots_els_users()
if users:
	stream.userstream( track=users, async=True )

# bucle infinit
while True:
	#print("...")
	sys.stdout.write(".")
	sys.stdout.flush()
	time.sleep(10)

