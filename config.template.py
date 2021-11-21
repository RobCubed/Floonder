# what the site is labeled as
sitename = "floonder"

# name of the local database
db = "floonder.db"

# flask secret key. generate with: python -c "import os; print(os.urandom(24))"
key = b''

# link to the rtsp server api. if on the same device, the default value is all thats necessary.
apibase = "http://127.0.0.1:9997/v1/"

# RTMP url for users to stream to. this will either be the server's IP or domain, and the port is
# from the "rtmpAddress" in rtsp-simple-server.yml
rtmpurl = "rtmp://localhost:1935"

# url for the HLS stream. This will be the domain/IP of the server, and the port is determined from
# the "hlsAddress" value in rtsp-simple-server.yml
hlsurl = "http://localhost:8888"
