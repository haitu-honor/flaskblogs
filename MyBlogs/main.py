import os
from flask import Flask, abort, render_template
from flask_sqlalchemy import SQLAlchemy

#整合MySQLdb
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='template', static_url_path="/", static_folder='resource')
app.config['SECRET_KEY'] = os.urandom(24)

#使用集成方式处理SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/myblogs?charset=utf8'
#关闭追踪数据库的追踪特性
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#实例化db对象
db = SQLAlchemy(app)

#制定错误页面
@app.errorhandler(404)
def error_404(e):
    return render_template('error-404.html')



# 定义文章类型函数，供模板页面直接调用
@app.context_processor  #context_processor这个是jinja2上下文处理器注解，该方法返回的article_type可以在html模板调用
def gettype():
    type = {
        '1': 'PHP开发',
        '2': 'Java开发',
        '3': 'Python开发',
        '4': 'Web前端',
        '5': '测试开发',
        '6': '数据科学',
        '7': '网络安全',
        '8': '蜗牛杂谈'
    }
    return dict(article_type=type)

if __name__ == '__main__':
    # 注册模块
    from controller.index import *
    app.register_blueprint(index)

    app.run(debug=True)
