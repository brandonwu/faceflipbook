"""Facebook connector glue stuff."""
from flask import Flask, request
import requests
import hashlib
import os
from facegetter import faceget, get_face
app = Flask(__name__)

app_id = '599387690117256'
app_secret = '287cac91b8ee347d1325a9dffd20fc2b'
my_uri = 'http://www.wonderboltseven.com:5000/fb-login'
my_uri_encoded = 'http%3A%2F%2Fwww.wonderboltseven.com%3A5000%2Ffb-login'

@app.route('/fb-login', methods=['GET', 'POST'])
def get_oauth_token():
	if 'code' in request.args:
		token = process_oauth_token(request.args['code'])[13:]
		graph_query = graph_api_query('me', 'name', token)
		name, uid = graph_query['name'], graph_query['id']
		result = fql_query(token, name)
		pic_urls = fetch_pic_url(result, token)
		#folder = 'images/' + hashlib.md5(uid).hexdigest()
		folder = ''
		#os.makedirs(folder)
		#for i in xrange(0, len(pic_urls)):
		for i in xrange(0, 10):
			pic = pic_urls[i]
			pic_name = folder + '/' + hashlib.md5(pic[u'src_big']).hexdigest()
			#get_face(pic[u'src_big'], pic[u'xcoord']/float(100), pic[u'ycoord']/float(100), 100, pic_name)
			get_face(pic[u'src_big'], pic[u'xcoord']/float(100), pic[u'ycoord']/float(100), pic_name)
		return str(pic_urls)
	else:
		return fb_oauth_redirect()

def process_oauth_token(code, s=requests.Session()):
	token_url = 'https://graph.facebook.com/oauth/access_token?client_id={0}' +\
				'&redirect_uri={1}&client_secret={2}&code={3}'
	url = token_url.format(app_id, my_uri_encoded, app_secret, code)
	return s.get(url).text.split('&')[0]

def fb_oauth_redirect():
	"""If there is no POST with a facebook oauth token, redirect user."""
	redirect_url = "https://www.facebook.com/dialog/oauth?client_id={0}" +\
				   "&redirect_uri={1}&scope={2}"
	redirect_js	= '<script>top.location.href="{0}"</script>'
	scope = 'user_photos,friends_photos'
	return redirect_js.format(redirect_url.format(app_id, my_uri, scope))

def graph_api_query(endpoint, fields, token):
	baseurl = 'https://graph.facebook.com/{0}'.format(endpoint)
	params = {'fields': fields, 'access_token': token}
	return requests.get(baseurl, params=params).json()

def fql_query(access_token, name):
	baseurl = 'https://graph.facebook.com/fql'
	query = 'SELECT pid, object_id, text, xcoord, ycoord '+\
			'FROM photo_tag WHERE subject=me() AND text == "{0}"'.format(name)
	params = {'q': query, 'access_token': access_token}
	return requests.get(baseurl, params=params).json()[u'data']

def fetch_pic_url(tags, token, s=requests.Session()):
	for tag in tags:
		object_id = tag[u'object_id']
		tag[u'src_big'] = get_pic_src(object_id, token, s)#superFQLjoin
	return tags

def get_pic_src(object_id, token, s):
	query = 'SELECT src_big FROM photo WHERE object_id = {0}'.format(object_id)
	baseurl = 'https://graph.facebook.com/fql'
	params = {'q': query,
			  'access_token': token}
	return s.get(baseurl, params=params).json()['data'][0][u'src_big']

if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0')