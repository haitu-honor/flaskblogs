from sqlalchemy import Table, func
from common.database import dbconnect
from module.users import Users

dbsession,DBase,md = dbconnect()

class Article(DBase):
    __table__ = Table('article', md, autoload=True)  # autoload=True,自动提交事务

    #查询所有文章
    def find_all(self):
        result = dbsession.query(Article).all()

    #根据id查询文章
    def find_by_id(self,articleid):
        row = dbsession.query(Article).filter_by(articleid = articleid).first()
        return row

    #指定分页的limit和offset的参数值，同时与用户表做链接查询
    def find_limit_with_users(self,start,count):    #start:查询开始位置，count:查询条数
        result = dbsession.query(Article,Users).join(Users,Users.userid==Article.userid)\
            .filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1)\
            .order_by(Article.articleid.asc()).limit(count).offset(start).all()
            #asc()升序，desc()倒序
            #.filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \ 过滤条件，满足的不被隐藏的文章才会显示
        return result

    # 统计一下当前文章的总数量
    def get_total_count(self):
        count = dbsession.query(Article).filter(Article.hide == 0, Article.drafted == 0,Article.checked == 1).count()
        return count

    # 根据文章类型获取文章
    def find_by_type(self, type, start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid) \
            .filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1, Article.type == type) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类型来获取总数量
    def get_count_by_type(self, type):
        count = dbsession.query(Article).filter(Article.hide == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.type == type).count()
        return count

    # 根据文章标题进行模糊搜索
    def find_by_headline(self, headline, start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid) \
            .filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1,
                    Article.headline.like('%' + headline + '%')) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 统计模糊搜索分页总数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Article).filter(Article.hide == 0,
                                                Article.drafted == 0,
                                                Article.checked == 1,
                                                Article.headline.like('%' + headline + '%')).count()
        return count

    # 最新文章[(id, headline),(id, headline)]
    def find_last_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.articleid.desc()).limit(9).all()
        return result

    # 最多阅读
    def find_most_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.readcount.desc()).limit(9).all()
        return result

    # 特别推荐，如果超过9篇，可以考虑order by rand()的方式随机显示9篇
    def find_recommended_9(self):
        result = dbsession.query(Article.articleid, Article.headline). \
            filter(Article.hide == 0, Article.drafted == 0, Article.checked == 1, Article.recommended == 1) \
            .order_by(func.rand()).limit(9).all()
        return result

    # 一次性返回三个推荐数据
    def find_last_most_recommended(self):
        last = []
        for lAtri in self.find_last_9():
            la = list(lAtri)
            last.append(la)
        most = []
        for mAtri in self.find_most_9():
            mo = list(mAtri)
            most.append(mo)
        recommended = []
        for rAtri in self.find_recommended_9():
            re = list(rAtri)
            recommended.append(re)
        return last, most, recommended