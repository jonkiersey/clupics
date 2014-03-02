import webapp2

from google.appengine.api import users
from google.appengine.ext import db

import jinja2

from datetime import datetime, timedelta
import json
import logging
import os
import urllib2

import settings

from models import Goal, Submission

jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR))


class RequestHandler(webapp2.RequestHandler):
    """Base request handler that handles site wide handling tasks."""
    def render(self, template_name, data={}):
        """Renders the template in the site wide manner.
        
        Merges template data with template helper methods to the view and
        renders the template. Templates are retrieved from the template
        directory specified in the settings and appended with the suffix
        ".html"
        
        Arguments:
        template_name: the name of the template. this is the file name of the
                       template without the .html extension.

        data: a dictionary containing data to be passed to the template.
        """
        data['uri_for'] = webapp2.uri_for
        
        template = jinja.get_template(template_name + '.html')
        return self.response.out.write(template.render(data))


class SubmissionListHandler(RequestHandler):
    def get(self):
        return self.render('submission-list')

class GoalListHandler(RequestHandler):
    def get(self):
        return self.render('goal-list')

class PidListHandler(RequestHandler):
    def get(self):
        return self.render('pid-list')
			
class JsonPidListHandler(webapp2.RequestHandler):
    def get(self):
        submissions = []
        for submission in Submission.all().order('-post_time'):
            submissions.append({
                'name': submission.name,
                'pid': submission.pid,
                'image_url': submission.image_url,
            })
        self.response.out.write(json.dumps(submissions))

class JsonSubmissionListHandler(webapp2.RequestHandler):
    def get(self):
        submissions = []
        for submission in Submission.all().order('-post_time'):
            submissions.append({
                'name': submission.name,
                'pid': submission.pid,
                'image_url': submission.image_url,
				'post_time': str(submission.post_time),
            })
        self.response.out.write(json.dumps(submissions))

    def post(self):
        form = json.loads(self.request.get('form'))
        name = form['name']
        pid = form['pid']
        image_url = form['image-url']
        Submission(name=name, pid=pid, image_url=image_url).put()

class JsonGoalListHandler(webapp2.RequestHandler):
    def get(self):
        goals = []
        for goal in Goal.all().order('-time'):
            goals.append({
                'prompt': goal.prompt,
                'pid': goal.pid,
				'time': str(goal.time),
            })
        self.response.out.write(json.dumps(goals))

    def post(self):
        form = json.loads(self.request.get('form'))
        prompt = form['prompt']
        pid = form['pid']
        Goal(prompt=prompt, pid=pid).put()

class UpvoteHandler(webapp2.RequestHandler):
	def get(self):
		usid = self.request('usid')
		submissions = db.GqlQuery("Select * from Submission where usid = :1", usid)
		for sub in submissions:
			sub.ups += 1
			sub.put()

class DownvoteHandler(webapp2.RequestHandler):
	def get(self):
		usid = self.request('usid')
		submissions = db.GqlQuery("Select * from Submission where usid = :1", usid)
		for sub in submissions:
			sub.downs += 1
			sub.put()

app = webapp2.WSGIApplication([
    ('/', SubmissionListHandler),
    webapp2.Route(r'/pid', name='submission-list',
                  handler=PidListHandler, methods=['GET']),
    webapp2.Route(r'/json/pid', name='json-pid-list',
                  handler=JsonPidListHandler, methods=['GET']),
    webapp2.Route(r'/submission', name='submission-list',
                  handler=SubmissionListHandler, methods=['GET']),
    webapp2.Route(r'/json/submission', name='json-submission-list',
                  handler=JsonSubmissionListHandler, methods=['GET', 'POST']),
    webapp2.Route(r'/goal', name='goal-list',
                  handler=GoalListHandler, methods=['GET']),
    webapp2.Route(r'/json/goal', name='json-goal-list',
                  handler=JsonGoalListHandler, methods=['GET', 'POST']),
], debug=True)
