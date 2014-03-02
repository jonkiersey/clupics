from google.appengine.ext import db

class Goal(db.Model):
	prompt = db.StringProperty("Prompt")
	time = db.DateTimeProperty("Time", auto_now_add=True)
	pid = db.StringProperty("Prompt ID")

class Submission(db.Model):
	name = db.StringProperty("Name")
	image_url = db.StringProperty("Image")
	post_time = db.DateTimeProperty("Time", auto_now_add=True)
	pid = db.StringProperty("Prompt ID")
	usid = db.StringProperty("User/Submission ID")
	ups = db.IntegerProperty("Upvotes")
	downs = db.IntegerProperty("Downvotes")
