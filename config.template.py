# what the site is labeled as
sitename = "floonder"

# name of the local database
db = "floonder.db"

# flask secret key. generate with: python -c "import os; print(os.urandom(24))"
key = b''

# link to the OvenMediaEngine (OME) api
apibase = "http://127.0.0.1:9997/v1/"

# API key for OME
apikey = b""

# Application name for OME. Default is 'app'
ovenapp = "app"


# Link to the websocket host for OME to deliver video to the clients
wsurl = "ws://localhost:3333/" + ovenapp

# Link to OME's HTTP port so that a thumnail can be sent
thumbnailurl = "http://localhost:8888/" + ovenapp

# Link to the RTMP server for clients to connect to
rtmp = "rtmp://localhost:1935/app"