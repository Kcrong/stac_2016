from app import db
from datetime import datetime
from geoalchemy2.types import Geometry
from config import randomkey


#  http://stackoverflow.com/questions/4069595/flask-with-geoalchemy-sample-code

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class ArticleImage(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    article_id = db.Column(db.INTEGER, db.ForeignKey('article.id'))
    filename = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return "<ArticleImage %s>" % self.filename


class Comment(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    article_id = db.Column(db.INTEGER, db.ForeignKey('article.id'))
    playground_id = db.Column(db.INTEGER, db.ForeignKey('playground.id'))
    content = db.Column(db.TEXT, nullable=False)
    score = db.Column(db.INTEGER, nullable=False)

    def __init__(self, content, writer, score, article=None, playground=None):
        self.content = content
        self.article = article
        self.user = writer
        self.playground = playground

        score = int(score)

        if score > 5:
            score = 5
        elif score < 1:
            score = 1

        self.score = score

    def __repr__(self):
        return "<Comment %s>" % self.content


class Playground(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    # location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    text_location = db.Column(db.TEXT, nullable=False)
    comments = db.relationship(Comment, backref='playground')

    def __init__(self, title, location):
        self.title = title
        self.text_location = location
        self.location = self.text2

    def __repr__(self):
        return "<Playground %s>" % self.title


class Article(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    content = db.Column(db.TEXT, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    comments = db.relationship(Comment, backref='article')

    def __init__(self, title, content, writer):
        self.title = title
        self.content = content
        self.user = writer

    def __repr__(self):
        return "<Article %s>" % self.title

    @property
    def base_info(self):
        return dict(
            id=self.id,
            user=self.user.nickname,
            title=self.title,
            content=self.content
        )


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    userid = db.Column(db.String(30), unique=True, nullable=False)
    userpw = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(20), nullable=False, unique=True)
    image = db.Column(db.String(60), unique=True)
    created_at = db.Column(db.DATETIME, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DATETIME, default=datetime.now(), nullable=False, onupdate=datetime.now())
    articles = db.relationship(Article, backref='user')
    comments = db.relationship(Comment, backref='user')

    def __init__(self, userid, userpw, nickname):
        self.userid = userid
        self.userpw = userpw
        self.nickname = nickname

    def __repr__(self):
        return "<User %s>" % self.userid

    @property
    def base_info(self):
        return dict(
            id=self.id,
            userid=self.userid,
            nickname=self.nickname,
            created=self.created_at,
            updated=self.updated_at
        )

    def add_profile(self, image):
        random_filename = randomkey(60)
        image.save('../static/' + random_filename)
        self.image = random_filename
        db.session.commit()
