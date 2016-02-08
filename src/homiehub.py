import os, json, threading
from pubnub import Pubnub
from influxdb import InfluxDBClient

# Get PubNub settings from ENV
pnpubkey = os.environ['PN_PUBKEY']
pnsubkey = os.environ['PN_SUBKEY']
pnaction = os.environ['PN_ACTION']
pnstatus = os.environ['PN_STATUS']

# Get InfluxDB settings from ENV
idbhost = os.environ['IDB_HOST']
idbport = os.environ['IDB_PORT']
idbuser = os.environ['IDB_USER']
idbpass = os.environ['IDB_PASS']
idbusedb = os.environ['IDB_USEDB']

# PubNub Client Connection
pubnub = Pubnub(publish_key=pnpubkey, subscribe_key=pnsubkey)

# InfluxDB Client Connection
client = InfluxDBClient(idbhost, idbport, idbuser, idbpass, idbusedb)

# Publish readSensors action to imp on the action channel
def readSensors():
    pubnub.publish(channel=pnaction, message='{"imp":"readSensors"}')
    threading.Timer(300, readSensors).start()

# Unsubscribe from the status channel
def pnUnsubscribe():
    pubnub.unsubscribe(channel=pnstatus)

def _callback(message, channel):
    if 'measurement' in message:
        try:
            client.write_points(json.loads('['+json.dumps(message)+']'))
        except:
            None

def _error(message):
    print("ERROR")

def _connect(message):
    print("Connected")
    readSensors()

def _reconnect(message):
    print("Reconnected")

def _disconnect(message):
    print("Disconnected")

# Subscribe to the status channel to watch for log events
pubnub.subscribe(channels=pnstatus, callback=_callback, error=_callback, connect=_connect, reconnect=_reconnect, disconnect=_disconnect)
