from datetime import datetime
from main import app, db, bcrypt, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

memberships = db.Table('memberships',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('groups_id',db.Integer, db.ForeignKey('groups.id'))
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    bio = db.Column(db.String(255), nullable=False, default="")
    posts = db.relationship('Post', backref='author',lazy=True)
    lists = db.relationship('Lists', backref='author',lazy=True)
    groups = db.relationship('Groups', secondary=memberships, backref=db.backref('member', lazy = 'dynamic'))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.groups}')"

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(40), unique=True, nullable=False)
    group_admin = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_access = db.Column(db.Boolean, nullable=False)
    group_profilepic = db.Column(db.String(20), nullable=False, default='default_group.png')
    group_bio = db.Column(db.String(255), nullable=False, default = "")
    members = db.relationship(User)

    def __repr__(self):
        return f"Groups('{self.groupname}','{self.group_admin}',)"

class GroupRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.String(40), nullable=False)
    access_level = db.Column(db.Integer,nullable=False, default=0)

class Lists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
