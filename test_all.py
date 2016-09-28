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


class ViewTestCase(BaseTestCase):
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

    def __write_article(self):
        return self.client.post(board_article_url,
                                data=dict(
                                    title=test_article_TITLE,
                                    content=test_article_CONTENT
                                ))

    def __write_comment(self, article):
        return self.client.post(board_comment_url,
                                data=dict(
                                    article_id=article.id,
                                    content=test_comment_CONTENT,
                                    score=test_comment_SCORE
                                ))

    def test_account(self):
        self.assert200(self.__useradd(), "회원가입 오류")

        res = self.__userinfo()
        self.assert200(res)
        self.assertEqual(res.json['userid'], test_user_ID, "잘못된 회원 정보 열람 (아이디)")
        self.assertEqual(res.json['nickname'], test_user_NICKNAME, "잘못된 회원 정보 열람 (닉네임)")

        # 중복유저 처리
        res = self.__useradd()
        self.assertEqual(res.json['status'], 'duplicated', "상태메세지 이상")
        self.assertIn(res.json['column'], ['userid', 'nickname'], "중복 칼럼 오류")

        self.__login()

        self.assertEquals(self.__userdel().json, dict(code=200, status='Success'), "계정 삭제 실패")

        self.assert401(self.__login(), "계정 삭제 후 로그인 제한 실패")

    def test_session(self):
        self.__useradd()

        self.assertEquals(self.__login().json, dict(code=200, status='Success'), "로그인 실패")
        self.assert401(self.__login(), "로그인한 유저의 재로그인 제한 실패")

        self.assertEquals(self.__logout().json, dict(code=200, status='Success'), "로그아웃 실패")
        self.assert401(self.__logout(), "로그아웃한 유저의 재로그아웃 제한 실패")

    def test_board(self):
        a = ModelTestCase.write_article(ModelTestCase.useradd())

        self.assertEquals(self.__login().json, dict(code=200, status='Success'), "로그인 실패")

        self.assertEquals(self.__write_article().json, dict(code=200, status='Success'), "게시물 작성 실패")

        self.assertEquals(self.__write_comment(a).json, dict(code=200, status='Success'), "댓글 작성 실패")


class ModelTestCase(BaseTestCase):
    @staticmethod
    def useradd():
        u = User(test_user_ID, test_user_PASSWORD, test_user_NICKNAME)
        db.session.add(u)
        db.session.commit()

        return u

    @staticmethod
    def write_article(user):
        a = Article(test_article_TITLE, test_comment_CONTENT, user)
        db.session.add(a)
        db.session.commit()

        return a

    @staticmethod
    def write_comment(article, user):
        c = Comment(test_comment_CONTENT, user, test_comment_SCORE, article=article)
        db.session.add(c)
        db.session.commit()

        return c

    def test_user_model(self):
        u = self.useradd()
        a = self.write_article(u)
        c = self.write_comment(a, u)

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
