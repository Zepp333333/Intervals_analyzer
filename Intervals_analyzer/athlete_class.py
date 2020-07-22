import json_ops
import strava_ops
from importlib import reload
reload(strava_ops)
reload(json_ops)


class BasicAthlete:
	def __init__(self, athlete_id, athlete_strava_id):
		assert athlete_id is not None
		assert type(athlete_id) == int
		assert (athlete_strava_id == None or type(athlete_strava_id) == int)

		self.id = athlete_id
		self.strava_id = athlete_strava_id
		self.info = []
		self.strava_info = None
		self.strava_auths_code = None
		self.strava_auth_json = None
		self.activities = None


	def __str__(self):
		if self.info != []:
			return self.info['name']
		else:
			return "Athlete with unknown name, yet"

	def get_info(self):
		pass #todo

	def is_strava_authorized(self):
		pass #todo not sure I need it

	def add_strava_auths_code(self, code):
		# BasicAthlete String -> None
		# add strava_auth_code to self, calls strva_ops to get and add strava_auth_json to self
		#   - code is a string (token) received from Strava after user has authorized an app
		self.strava_auths_code = code
		self.strava_auth_json = strava_ops.get_access_token(self.strava_auth_json, self.strava_auths_code)

	def refresh_strava_token(self):
		if self.strava_auth_json == None:
			### STUB # todo somehow change to redirect user to strava to authorize the application
			raise Exception("strava_auth_json is None, but I " \
			                "don't yet know how to redirect user to get the app authorized")
			### STUB
		elif strava_ops.is_strava_token_expired(self.strava_auth_json):
			return strava_ops.refresh_expired_token(self.strava_auth_json)
		else:
			return self.strava_auth_json

	def get_strava_athlete(self):
		self.strava_info = strava_ops.get_athlete(self.strava_auth_json)

	def get_activities_list(self):
		self.activities = strava_ops.get_athlete_activities_list_all(self.strava_auth_json)

	def get_activity_streams(self, activity):
		activity['streams'] = strava_ops.get_activity_streams(activity['id'], self.strava_auth_json)

	def get_all_activity_streams(self):
		if self.activities == None:
			raise Exception("get_all_activity_streams called wile activities list was empty")
		for activity in self.activities:
			self.get_activity_streams(activity)



