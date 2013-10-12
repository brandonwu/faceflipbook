"""Facebook connector glue stuff."""
from flask import Flask, request
import requests
app = Flask(__name__)

app_id = '599387690117256'
app_secret = '287cac91b8ee347d1325a9dffd20fc2b'
my_uri = 'http://www.wonderboltseven.com:5000/fb-login'
my_uri_encoded = 'http%3A%2F%2Fwww.wonderboltseven.com%3A5000%2Ffb-login'

@app.route('/fb-login', methods=['GET', 'POST'])
def get_oauth_token():
	if 'code' in request.args:
		return fql_query(process_oauth_token(request.args['code'])[13:])
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
				   "&redirect_uri={1}"
	redirect_js	= '<script>top.location.href="{0}"</script>'
	return redirect_js.format(redirect_url.format(app_id, my_uri))

def fql_query(access_token):
	baseurl = 'https://graph.facebook.com/fql'
	query = 'SELECT pid, object_id, text, xcoord, ycoord '+\
			'FROM photo_tag WHERE subject=me() AND text == "Brandon Wu"'
	params = {'q': query,
			  'access_token': access_token}
	return requests.get(baseurl, params=params).text

if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0')