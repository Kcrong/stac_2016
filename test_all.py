import unittest

from flask.ext.testing import TestCase

from app import app
from app.models import *

user_account_url = '/user/account'
user_session_url = '/user/session'
board_article_url = '/board/article'
board_comment_url = '/board/comment'

test_user_ID = 'testid'
test_user_PASSWORD = 'userpw'
test_user_NICKNAME = 'testnick'

test_article_TITLE = 'test_article_title'
test_article_CONTENT = 'test_article_content'

test_comment_CONTENT = 'test_comment_content'
test_comment_SCORE = 1


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['SECRET_KEY'] = 'development-test-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class UserTestCase(BaseTestCase):
    def __userinfo(self):
        return self.client.get(user_account_url,
                               query_string=dict(
                                   userid=test_user_ID
                               ))

    def __useradd(self):
        return self.client.post(user_account_url,
                                data=dict(
                                    userid=test_user_ID,
                                    userpw=test_user_PASSWORD,
                                    nickname=test_user_NICKNAME
                                ))

    def __userdel(self):
        return self.client.delete(user_account_url,
                                  data=dict(
                                      userid=test_user_ID,
                                      userpw=test_user_PASSWORD
                                  ))

    def __login(self):
        return self.client.post(user_session_url,
                                data=dict(
                                    userid=test_user_ID,
                                    userpw=test_user_PASSWORD
                                ))

    def __logout(self):
        return self.client.delete(user_session_url,
                                  data=dict(
                                      userid=test_user_ID
                                  ))

    def test_account(self):
        self.assert200(self.__useradd())

        res = self.__userinfo()
        self.assert200(res)
        self.assertEqual(res.json['userid'], test_user_ID)
        self.assertEqual(res.json['nickname'], test_user_NICKNAME)

        self.assertEquals(self.__userdel().json, dict(code=200, status='Success'))

    def test_session(self):
        self.__useradd()

        self.assertEquals(self.__login().json, dict(code=200, status='Success'))

        self.assertEquals(self.__logout().json, dict(code=200, status='Success'))


class ModelTestCase(BaseTestCase):
    @staticmethod
    def __useradd():
        u = User(test_user_ID, test_user_PASSWORD, test_user_NICKNAME)
        db.session.add(u)
        db.session.commit()

        return u

    @staticmethod
    def __write_article(user):
        a = Article(test_article_TITLE, test_comment_CONTENT, user)
        db.session.add(a)
        db.session.commit()

        return a

    @staticmethod
    def __write_comment(article, user):
        c = Comment(test_comment_CONTENT, user, test_comment_SCORE, article=article)
        db.session.add(c)
        db.session.commit()

        return c

    def test_user_model(self):
        u = self.__useradd()
        a = self.__write_article(u)
        c = self.__write_comment(a, u)

        assert u in db.session
        assert a in db.session
        assert c in db.session

        new_u = User.query.filter_by(userid=test_user_ID).first()
        new_a = Article.query.filter_by(title=test_article_TITLE).first()
        new_c = Comment.query.filter_by(user=u, article=a).first()

        assert new_u.userpw == test_user_PASSWORD
        assert new_u.articles[0] == new_a

        assert new_a.user == new_u

        assert new_c.user == new_u
        assert new_c.article == new_a


if __name__ == '__main__':
    unittest.main()
