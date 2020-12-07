from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, length

app = Flask(__name__)
app.secret_key = 'test'

# 定义登录表单
class LoginForm(FlaskForm):
    # 域初始化
    user_phone = StringField('phone', validators=[DataRequired(), length(11,11),
                            Regexp('^1\d{10}$', 0, '手机号码不合法')],
                            render_kw={'placeholder': '输入手机号：'})
    verify_code = StringField('code',validators=[DataRequired('请输入验证码')],
                            render_kw={'placeholder': '输入手机号：'})

@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    
    return '登录成功'                          
    

if __name__ == "__main__":
    app.run(host='127.0.0.1',port='8080',debug=True)