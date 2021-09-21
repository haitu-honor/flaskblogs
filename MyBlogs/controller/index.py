from flask import Blueprint, render_template, abort, jsonify
from module.article import Article
from module.users import Users
import math

index = Blueprint("index",__name__)

#只是第一页的数据
@index.route('/')
def home():
    article = Article()
    result = article.find_limit_with_users(0,10)
    total = math.ceil(article.get_total_count() / 10)  # 总页数
    return render_template('index-base.html',result=result,page=1,total=total)

#分页查询
@index.route('/page/<int:page>')
def paginate(page):
    start = (page - 1) * 10   # 1==>0, 2==>10
    article = Article()
    result = article.find_limit_with_users(start, 10)
    total = math.ceil(article.get_total_count() / 10)   # 总页数

    return render_template('index-base.html', result=result,page=page,total=total)

#按文章类别查询并分页
@index.route('/type/<int:type>-<int:page>')
def classify(type, page):
    start = (page - 1) * 10
    article = Article()
    result = article.find_by_type(type, start, 10)
    total = math.ceil(article.get_count_by_type(type) / 10)
    return render_template('type.html', result=result, page=page, total=total, type=type)

#模糊查询搜索文字并进行分页
@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    #搜索关键字校验
    # strip()方法用于移除字符串头尾指定的字符（默认为空格）或字符序列。
    # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword) > 10:
        abort(404)

    start = (page-1) * 10
    article = Article()
    result = article.find_by_headline(keyword, start, 10)
    total = math.ceil(article.get_count_by_headline(keyword) / 10)

    return render_template('search.html', result=result, page=page, total=total, keyword=keyword)

#侧边栏最新文章，文章推荐，最多访问
@index.route('/recommend')
def recommend():
    print('访问了我')
    article = Article()
    last, most, recommended = article.find_last_most_recommended()
    list = []
    list.append(last)
    list.append(most)
    list.append(recommended)
    return jsonify(list)    #将对象数组转成json数据格式
