import json

# todo add logging

# CONSTANTS todo need to be converted into configurable parameters
project_root = '/Users/Sergey/Documents/OneDrive/Coding/Projects/Cycling_Intervals_parser/'

def read_json_from_file(file_name):
	with open(project_root + file_name, "r") as read_file:
		return json.load(read_file)

def write_json_to_file(data, file_name):
	with open(file_name, "w") as write_file:
		json.dump(data, write_file, indent=4)

activities = read_json_from_file("activities_short2.json")
# write_json_to_file(activities, "activities_short2.json")

def remove_pages_from_activities_list(data):
	clean_activities = []
	for page in data:
		for activity in page:
			clean_activities.append(activity)
	return clean_activities

# for a in range(len(activities)):
# 	print(activities[a]['id'])




