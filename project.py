from flask import Flask, render_template, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, length

import redis

pool = redis.ConnectionPool(host='localhost')
redis_con = redis.Redis(connection_pool=pool)

app = Flask(__name__)
app.secret_key = 'test'


# 获取验证码
@app.route('/<user_phone>/get_code')
def get_phone_code(user_phone):
    user_phone = str(user_phone)
    if user_phone == '18629577951':
        verify_code = '1126'
    else:
        verify_code = '0701'
    redis_con.set(user_phone,verify_code)
    return (verify_code)
    # print('验证码：',verify_code)

# 检查验证码
@app.route('/<user_phone>/<code>/check_code')
def go_check_code(user_phone,code):
    
    user_phone = str(user_phone)
    code = str(code)
    correct_code = bytes.decode(redis_con.get(user_phone))

    if correct_code == code:
        return jsonify({'result':True})
    else:
        return jsonify({'result':False})

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')
    
        


@app.route('/login',methods=['GET','POST'])
def login():
    
    return '登录成功'                          
    

if __name__ == "__main__":
    app.run(host='127.0.0.1',port='8080',debug=True)