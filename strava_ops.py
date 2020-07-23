import pandas as pd
import requests
import datetime
import json_ops
# from importlib import reload
# reload(json_ops)

# CONSTANTS todo need to be converted into configurable parameters
project_root = "/Users/Sergey/Documents/OneDrive/Coding/Projects/Cycling_Intervals_parser/"
auth_url = "https://www.strava.com/oauth/"
athlete_url = "https://www.strava.com/api/v3/athlete"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
activity_url_base = "https://www.strava.com/api/v3/activities/"
stream_ulr_base = "https://www.strava.com/api/v3/activities/"
app_client_id = 50434
app_client_secret = '1ac85eaaa5fcf4a1b4efa75197a81bc4b00464db'
app_redirect_uri = "http://localhost"


# Initializeing variables
access_token = None

#constants for test purposes
# athlete_auth_code = 'f32ee76ff598e6060c78e7a386f477713317911a'  # SS
athlete_auth_code = '15d4435ae72bb6f56afc2f7eed5cdaf18d5fefdf'    # test guy
# Manual
# from https://www.youtube.com/watch?v=sgscChKfGyg&list=PLO6KswO64zVvcRyk0G0MAzh5oKMLb6rTW

# 1) Getting Authorization code from authorization page. This is one time step (manual?)
# https://www.strava.com/oauth/authorize?client_id=50434&redirect_uri=http://localhost&response_type=code&scope=activity:read_all
# returned code is for SS: f32ee76ff598e6060c78e7a386f477713317911a
# returned code is for test guy: 3a9835d4e49bb2544cc478601163056b6fb63ec4

# 2) Exchange authorization code for access token & refresh tocken
# https://www.strava.com/oauth/token?client_id=50434&client_secret=1ac85eaaa5fcf4a1b4efa75197a81bc4b00464db&code=f32ee76ff598e6060c78e7a386f477713317911a&grant_type=authorization_code
# returned:
#   access token  : 56981dcee5d5df70de37498b1bf37ede4b08d4bc
#   refresh token : 13a0bbf5bdb97246f56c486c55b6cd25268d4a46

# 3) View your activities using the access token just recieved
# https://www.strava.com/api/v3/athlete/activities?access_token=b08e880eec242815ebef3937711a9084fe382862

# 4) Use refresh token to get new access tokens
# https://www.strava.com/oauth/token?client_id=50434&client_secret=1ac85eaaa5fcf4a1b4efa75197a81bc4b00464db&refresh_token=6456bccc36c32019000f8f4ff449830ebfe93d3e&grant_type=refresh_token


def is_strava_token_expired(strava_auth_json):
    if datetime.datetime.fromtimestamp(strava_auth_json['expires_at']) < datetime.datetime.now():
        return True
    else:
        return False

def get_athlete_authorization_code():
    ### STUB ###
    return athlete_auth_code ### STUB todo get the function done as soon as we have web app
    ### STUB - pieces of real code -> below
    url = auth_url + "authorize"
    param = {'client_id': app_client_id, 'redirect_uri': app_redirect_uri, 'response_type':'code', 'scope':'activity:read_all'}
    r = requests.get(url, params=param)
    return r

# print(get_athlete_authorization_code())

def refresh_expired_token(access_token):
    # https://www.strava.com/oauth/token?client_id=50434&client_secret=1ac85eaaa5fcf4a1b4efa75197a81bc4b00464db&refresh_token=6456bccc36c32019000f8f4ff449830ebfe93d3e&grant_type=refresh_token
    url = auth_url + "token"
    param = {'client_id': app_client_id, 'client_secret': app_client_secret, 'refresh_token': access_token['refresh_token'],
             'grant_type': 'refresh_token'}
    # req = requests.Request('POST', url, params=param)
    # r = req.prepare()
    try:
        r = requests.post(url, params=param)
    except Exception:
        print("ERROR: Token request failed in get_first_access_token")

    if r.status_code == 200:
        return r.json()
    else:
        print("ERROR: Failed to get HTTP 200 response from Strva in get_first_access_token")
        return "ERROR: Failed to get HTTP 200 response from Strva in get_first_access_token"




def get_access_token(strava_auth_json, strava_auths_code):

    if strava_auth_json == None:
        if strava_auths_code == None: raise Exception("get_access_token got both token and auth_code as None")

        url = auth_url + "token"
        param = {'client_id': app_client_id, 'client_secret':app_client_secret, 'code':strava_auths_code, 'grant_type':'authorization_code'}
        # req = requests.Request('POST', url, params=param)
        # r = req.prepare()
        # print(r.url)

        try:
            r = requests.post(url, params=param)
        except Exception:
            print("ERROR: Token request failed in get_first_access_token")

        if r.status_code == 200:
            return r.json() #todo - check validity of the json before returning
        else:
            print("ERROR: Failed to get HTTP 200 response from Strva in get_first_access_token")
            return r
    elif is_strava_token_expired(strava_auth_json):
        return refresh_expired_token(strava_auth_json)
    else:
        return strava_auth_json



# print(get_access_token(json_ops.read_json_from_file('token.json')))
# access_token = "56981dcee5d5df70de37498b1bf37ede4b08d4bc"

def get_athlete_activities_list_1_page(access_token):

    # construct the URL

    param = {'access_token':access_token, 'per_page': 50, 'page':1}
    return requests.get(activities_url, params=param).json()

def get_athlete_activities_list_all(strava_auth_json):
    # Initialize the dataframe
    col_names = ['id','type']
    activities = pd.DataFrame(columns=col_names)
    result = []
    page = 1
    while True:
        # get page of activities from Strava
        param = {'access_token': strava_auth_json['access_token'], 'per_page': 50, 'page': page}
        r = requests.get(activities_url, params=param).json()
        result.append(r)


        # if no results then exit loop
        if not r:
            break

        #otherwise: add new data to dataframe
        # for x in range(len(r)):
        # 	activities.loc[x + (page - 1) * 50, 'id'] = r[x]['id']
        # 	activities.loc[x + (page - 1) * 50, 'type'] = r[x]['type']
        # 	activities.append(activity)

        page += 1
    return json_ops.remove_pages_from_activities_list(result)

def get_activity_streams(id, strava_auth_json):
    #todo add docstring, assetions, try
    keys = "time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth" # array[String] | Desired stream types.
    keyByType = 'true'  # Boolean | Must be true. (default to true)
    url = stream_ulr_base + str(id) + '/streams'
    param = {'keys':keys, 'key_by_type': keyByType}
    headers = {"Authorization": "Bearer " + strava_auth_json['access_token']}
    r = requests.get(url, params=param, headers=headers).json()
    return r

def get_athlete(strava_auth_json):
    # todo add docstring, assetions, try
    url = athlete_url
    headers = {"Authorization": "Bearer " + strava_auth_json['access_token']}
    r = requests.get(url, headers=headers).json()
    return r


# streams = get_activity_streams(3691689393, access_token)
# json_ops.write_json_to_file(streams, "streams.json")

# with open("activities_short.json", "w") as write_file:
# 	json.dump(get_athlete_activities_list_all(access_token), write_file)
# print(get_athlete_activities_list_all(access_token))

# Initialize the dataframe
# col_names = ['id','type']
# activities = pd.DataFrame(columns=col_names)
# activities = get_athlete_activities_list_1_page(access_token)
# print(activities)

# activities = get_athlete_activities_list_1_page(access_token)
# print(activities)


# Get activity stream
#0    3691689393  Ride








