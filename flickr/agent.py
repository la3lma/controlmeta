
import json
import flickrapi
from pprint import pprint

json_file="/Users/rmz/Dropbox/controlmeta/flickr-secrets.json"
json_data=open(json_file).read()

data = json.loads(json_data)
api_secret = data['Secret']
api_key = data['Key']


my_userid='124348213@N07'
print "secret", api_secret
print "key", api_key

pprint(data)

flickr = flickrapi.FlickrAPI(api_key, api_secret)


flickr = flickrapi.FlickrAPI(api_key)
photos = flickr.photos_search(user_id=my_userid, per_page='10')
sets = flickr.photosets_getList(user_id=my_userid)

pprint(sets)
