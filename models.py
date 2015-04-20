from app import db
from sqlalchemy import create_engine, MetaData

class User(db.Model):
  __tablename__ = 'users'
  __table_args__ = {'extend_existing': True}
  extend_existing=True
  id = db.Column(db.Integer, primary_key=True)
  fb_id = db.Column(db.String)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  profile = db.relationship("Profile", uselist=False, backref="users")

  def __init__(self, fb_id=None, first_name=None, last_name=None):
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

recommendation_picture_table = db.Table("recommendedPicture", MetaData(),
  db.Column('recommendation_id', db.Integer, db.ForeignKey('recommendations.id')),
  db.Column('picture_id', db.Integer, db.ForeignKey('pictures.id'))) 

class Picture(db.Model):
  __tablename__ = 'pictures'
  __table_args__ = {'extend_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  file_path = db.Column(db.String, nullable=False)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
  pic_type = db.Column(db.String, nullable=False)
  recommendations = db.relationship("recommendations", secondary=recommendation_picture_table)

  def __init__(self, file_path=None, profile_id=None):
    self.file_path = file_path
    self.profile_id = profile_id

  def get_id(self):
    return unicode(self.id)

  def get_profile_id(self):
    return unicode(self.profile_id)

class Recommendation(db.Model):
  __tablename__ = 'recommendations'
  __table_args__ = {'extend_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
  pictures = db.relationship("pictures", secondary=recommendation_picture_table)

  def __init__(self, profile_id=None):
    self.profile_id = profile_id

  def get_id(self):
    return unicode(self.id)

  def get_profile_id(self):
    return unicode(self.profile_id)
  
class Profile(db.Model):
  __tablename__ = 'profiles'
  __table_args__ = {'extend_existing': True}
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  pictures = db.relationship("Picture")
  recommendations = db.relationship("Recommendation")
  pro_pic = db.Column(db.String)
  about = db.Column(db.String)
  preferences = db.Column(db.String)
  num_followers = db.Column(db.Integer)
  num_styles = db.Column(db.Integer)
  num_karma = db.Column(db.Integer)

  def __init__(self, user_id=None, pro_pic=None, about=None, preferences=None,
    num_followers=None, num_styles=None, num_karma=None):
    self.user_id = user_id
    self.pro_pic = pro_pic
    self.about = about
    self.preferences = preferences
    self.num_followers = num_followers
    self.num_styles = num_styles
    self.num_karma = num_karma

  def get_id(self):
    return unicode(self.id)

  def get_user_id(self):
    return unicode(self.user_id)