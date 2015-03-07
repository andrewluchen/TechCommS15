from app import db

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  fb_id = db.Column(db.String)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)

  def __init__(self, fb_id = None, first_name=None, last_name=None):
    self.fb_id = fb_id
    self.first_name = first_name
    self.last_name = last_name

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)