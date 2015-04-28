import boto
from boto.s3.connection import S3Connection
import boto.s3.connection

### access and secret key for connection
access_key = '<add your access key>'
secret_key = '<add your secret key>'

### establish connection to AWS S3 and mybucket
conn = boto.connect_s3(access_key, secret_key)
mybucket = conn.get_bucket('kirtikadhathathri')
print conn
print mybucket

### get file info to POST
mykey = mybucket.get_key("<add the file name>")
print mykey

### set an expiry time in seconds
expiry = 604800 # available for 7 days

### generate url
myurl = mykey.generate_url(expiry, query_auth=True, force_http=True)
print(myurl)