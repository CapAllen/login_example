import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
# 导入declarative_base，用于配置和类代码
from sqlalchemy.ext.declarative import declarative_base
# 用于创建外键关系，也会在创建mapper上派上用场
from sqlalchemy.orm import relationship
# 用于文末代码（创建或链接数据库）
from sqlalchemy import create_engine

from flask_login import UserMixin

Base = declarative_base()

class UserInfo(UserMixin, Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    phone = Column(Integer, nullable=False)
    code = Column(String(6),nullable=False)
    


class UserBuy(Base):
    __tablename__ = 'user_buy'

    id = Column(Integer, primary_key=True)
    phone = Column(Integer , ForeignKey('user_info.phone'), nullable=False)
    province = Column(String(16), nullable=False)
    kelei = Column(String(8), nullable=False)
    weici = Column(Integer,nullable=False)
    have_buy = Column(Integer,default=0)

    user_info = relationship(UserInfo)

class UserInvite(Base):
    __tablename__ = 'user_invite'

    id = Column(Integer, primary_key=True)
    phone = Column(Integer, ForeignKey('user_info.phone'), nullable=False)
    invited_phone = Column(Integer, nullable=False)

    user_info = relationship(UserInfo)

# 连接数据库，这里也可以链接其他数据库，比如mysq等
engine = create_engine('sqlite:///LoginExample.db')

# 创建数据库
Base.metadata.create_all(engine)

