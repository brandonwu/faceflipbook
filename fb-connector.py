"""Facebook connector glue stuff."""
from flask import Flask, request
import requests
from urllib import urlencode
app = Flask(__name__)

app_id = '674510052574179'
app_secret = 'aaca04a3b36adde03cd2e15ec031b533'
my_uri = 'http://www.wonderboltseven.com/fb-login'


@app.route('/fb-login', methods=['GET', 'POST'])
def get_oauth_token():
	if request.method == 'POST':
		process_oauth_token(request.form['code'])
	else:
		fb_oauth_redirect()

def process_oauth_token(code, s=requests.Session()):
	token_url = 'https://graph.facebook.com/oauth/access_token?client_id={0}' +\
				'&redirect_uri={1}&client_secret={2}&code{3}'
	return s.get(token_url.format(app_id, urlencode(my_uri), app_secret, code))


def fb_oauth_redirect():
	"""If there is no POST with a facebook oauth token, redirect user."""
	redirect_url = "https://www.facebook.com/dialog/oauth?client_id={0}" +\
				   "&redirect_uri={1}"
	redirect_js	= '<script>top.location.href="{0}"</script>'
	return redirect_js.format(redirect_url.format(app_id, my_uri))

class Facebook():
	def __init__(self, app_id, app_secret, app_something):
		return None

if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0')