# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 下午4:05
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from exts import db
from datetime import datetime
from sqlalchemy.orm import backref

# ball_match = db.Table(
#     'ball_match',  # 表名
#     # 字段名:cms_role_id,类型,外键:cms_role.id,设置为主键
#     db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True),
#     db.Column('ball_id', db.Integer, db.ForeignKey('ball.id'), primary_key=True)
# )


# 球队
class Ball(db.Model):
    __tabelname__ = 'ball'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(50), nullable=False)  # 球队编号
    name = db.Column(db.String(50), nullable=False)  # 球队名称
    country = db.Column(db.String(50), nullable=False)  # 球队国家
    in_group = db.Column(db.String(50), nullable=False)  # 所在小组

    # integrals = db.relationship('Integral')
    create_time = db.Column(db.DateTime, default=datetime.now)

    # matchs = db.relationship('Match', secondary=ball_match, backref='balls')

    def __repr__(self):
        return '<Ball: 球队编号 %s 球队名称 %s %s>' % (
            self.number,
            self.name,
            self.in_group,
        )


# 球队积分
class Integral(db.Model):
    __tabelname__ = 'integral'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    integrals = db.Column(db.String(50), default='0')  # 积分
    goal = db.Column(db.String(50), default='0')  # 进球数
    lose = db.Column(db.String(50), default='0')  # 丢球数
    clean = db.Column(db.String(50), default='0')  # 净胜球

    ball_id = db.Column(db.Integer, db.ForeignKey('ball.id'))  # 球队id外键
    ranks = db.relationship('Ball', backref=backref('integrals', uselist=False))  # 积分对应的球队:obj=Integral.ranks

    create_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Integral: 球队id: %s 球队积分: %s  >' % (
            self.ball_id,
            self.integrals,
        )


# 赛果
class Match(db.Model):
    __tabelname__ = 'match'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_time = db.Column(db.Float)  # 比赛时间
    main_team = db.Column(db.String(50))  # 主队名称
    guest_team = db.Column(db.String(50))  # 客队名称
    z_score = db.Column(db.Integer)  # 主队进球
    k_score = db.Column(db.Integer)  # 客队进球
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Match: id: %s [%s VS %s]  %s : %s>' % (
            self.id,
            self.main_team,
            self.guest_team,
            self.z_score,
            self.k_score,
        )
