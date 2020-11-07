from Web_Application import db
from datetime import datetime


# Create DataBase
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # TODO: making original_text unique requires exception handling, for simplicity is omitted so far
    # path to file
    original_text = db.Column(db.Text, nullable=False)

    # original_text = db.Column(db.Text, unique=False, nullable=False)
    summary = db.Column(db.Text)

    def __repr__(self):
        return f"Post('{self.original_text[:50]}', '{self.summary}', '{self.date_posted}')"