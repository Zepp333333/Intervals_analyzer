from unittest import TestCase

import sys
sys.path.append('../')

from Intervals_analyzer.athlete_class import BasicAthlete

class TestBasicAthlete(TestCase):

    def setUp(self):
        self.a = BasicAthlete(123, None)

    def test_get_info(self):
        self.assertEqual(self.a.get_info(), (123, None))

    def test_is_strava_authorized(self):
        self.fail()

    def test_add_strava_auths_code(self):
        self.fail()

    def test_refresh_strava_token(self):
        self.fail()

    def test_get_strava_athlete(self):
        self.fail()

    def test_get_activities_list(self):
        self.fail()

    def test_get_activity_streams(self):
        self.fail()

    def test_get_all_activity_streams(self):
        self.fail()
