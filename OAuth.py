import rauth, json
import sys, pprint

def user_input(qn):
	if hasattr(__builtins__, 'raw_input'):
		return raw_input(qn)
	else:
		return input(qn)

#Get Auth params fromt the user
name = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]

#Initialize OAuth Service
service = rauth.OAuth2Service(
           name=name,
           client_id=client_id,
           client_secret=client_secret,
           access_token_url='https://secure.meetup.com/oauth2/access',
           authorize_url='https://secure.meetup.com/oauth2/authorize',
           base_url='https://api.meetup.com')
print('\n'+'=> OAuth Service Object Initialized'+'\n')

#Step 1: Get Authorize URL to Endpoint
params = {'redirect_uri': 'www.dummy.com',
          'response_type': 'code'}
url = service.get_authorize_url(**params)

#Step 2: Ask the user to authorize the access & provide the authorize_token
print('=> Type this URL in the browser & you will be asked for permission & once you grant permission, you will see "code=<auth_code>" in the Address Bar '+'\n'+url)
auth_code = user_input('Enter that auth_code here - ')

#Step 3: Now, get the session
data = {'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'www.dummy.com'}
session = service.get_auth_session(
	data = data, 
	decoder = lambda resp:json.loads(resp.decode(encoding='utf-8')))
print('=> Session Created '+'\n')

#Step 4: Run a sample API Request - 
r = session.get('/2/open_events', 
		params={'country':'uk',
				'city': 'london', 
				'topic':'salesforce',
				'time':'0d,1d'}
	)
print('=> Sample API Response for Open Events '+'\n')	
pp = pprint.PrettyPrinter()
pp.pprint(r.json()['results'][0])
