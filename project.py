from flask import Flask, render_template, redirect, jsonify, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, length
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbase_setup import Base, UserInfo, UserBuy, UserInvite


# 链接数据库
engine = create_engine('sqlite:///LoginExample.db', connect_args={'check_same_thread': False})
# 用bind将engine与Base绑定在一起
Base.metadata.bind = engine
# 创建一个session，与数据库进行会话
DBsession = sessionmaker(bind=engine)
# 实例化session
# 我们可以使用session进行CRUD操作，但之后需要使用commit进行确认
db_session = DBsession()


app = Flask(__name__)
app.secret_key = 'test'

login_manager = LoginManager()
login_manager.init_app(app)
# 验证登陆失败时，跳转的网页
login_manager.login_view = 'index'

@login_manager.user_loader
def user_loader(phone):
    user = db_session.query(UserInfo).filter_by(phone=phone).first()
    return user

# 获取验证码
@app.route('/<user_phone>/get_code')
def get_phone_code(user_phone):
    user_phone = int(user_phone)
    if user_phone == 18629577951:
        verify_code = '1126'
    else:
        verify_code = '0701'
    
    user_query = db_session.query(UserInfo).filter_by(phone=user_phone)
    if db_session.query(user_query.exists()).scalar() == 0:
        update_code = UserInfo(phone=user_phone,code=verify_code)
        
    else:
        update_code = user_query.one()
        update_code.code = verify_code

    db_session.add(update_code)
    db_session.commit()
    return verify_code
    # print('验证码：',verify_code)

# 检查验证码
@app.route('/<user_phone>/<code>/check_code')
def go_check_code(user_phone,code):
    
    user_phone = int(user_phone)
    code = str(code)
    user = db_session.query(UserInfo).filter_by(phone=user_phone).first()
    correct_code = user.code

    if correct_code == code:
        login_user(user)
        flash('验证码输入正确')
        return redirect(url_for('login'))
    
    flash('验证码输入错误')
    return jsonify({'result':False})


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')
    
        


@app.route('/login',methods=['GET','POST'])
@login_required
def login():
    user_phone = current_user
    return render_template('login.html',user_phone=user_phone)                   
    

if __name__ == "__main__":
    app.run(host='127.0.0.1',port='8080',debug=True)