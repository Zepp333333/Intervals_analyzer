from requests import Request


username = 'ttt'
auth_url = "https://www.strava.com/oauth/authorize"
param = {'client_id':'50434',
        'redirect_uri':('http://localhost:5000/StravaAuthReturn/' + str(username)),
        'response_type':'code',
        'scope':'activity:read_all'}

req = Request('GET', auth_url, params=param).prepare().url
print(req)
