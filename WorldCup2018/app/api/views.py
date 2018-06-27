# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 下午4:03
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : views.py
# @Software: PyCharm


from flask import Blueprint, jsonify, request
from app.api.models import Ball, Integral, Match
from exts import db
from sqlalchemy import func, text
import time

bp = Blueprint('api', __name__, url_prefix='/api')


class ApiResult(object):
    def formattingData(self, status, msg, data):
        return jsonify(
            {
                "status": status,
                "msg": msg,
                "data": data
            }
        )


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


@bp.route('/test')
def test():
    # a = Ball(number='A1', name='俄罗斯', country='俄罗斯', in_group='A组')
    # a1 = Ball(number='A2', name='沙特阿拉伯', country='沙特阿拉伯', in_group='A组')
    # a2 = Ball(number='A3', name='埃及', country='埃及', in_group='A组')
    # a3 = Ball(number='A4', name='乌拉圭', country='乌拉圭', in_group='A组')

    # i = Integral(integrals='5', goal='8', lose='3', clean='5')
    # i2 = Integral(integrals='0', goal='2', lose='7', clean='0')
    # i3 = Integral(integrals='0', goal='2', lose='5', clean='0')
    # i4 = Integral(integrals='5', goal='5', lose='0', clean='5')

    # a.integrals = i
    # a1.integrals = i2
    # a2.integrals = i3
    # a3.integrals = i4
    # db.session.add_all([a, a1, a2, a3])
    # db.session.commit()

    # a = Ball.query.filter(Ball.id == 1).first()
    # a = Ball.query.all()
    # print(a)
    # print(a.id)
    # r = a.integrals
    # print(r)

    # """
    # SELECT ball.in_group,max(integral.clean)
    # FROM ball JOIN integral ON ball.id = integral.ball_id
    # WHERE ball.id = integral.ball_id GROUP BY ball.in_group
    # :return:
    # """

    # result = db.session.query(Ball, func.max(Integral.clean)).join(Integral).group_by(Ball.in_group).order_by(
    #     func.count(Integral.id).desc())
    # print(result)

    # result3 = Ball.query.join(Integral, Ball.id == Integral.ball_id).group_by(
    #     Ball.id).add_entity(Integral)
    # print(result3)
    # for res in result:
    #     # print(res)
    #     zu = res.Ball.in_group
    #     qiu = res.Ball.integrals
    #     # print(qiu)
    #     for i in qiu:
    #         print(zu, i.clean)
    """
    match_time = db.Column(db.Float)  # 比赛时间
    main_team = db.Column(db.String(50))  # 主队名称
    guest_team = db.Column(db.String(50))  # 客队名称
    z_score = db.Column(db.Integer)  # 主队进球
    k_score = db.Column(db.Integer)  # 客队进球
    create_time = db.Column(db.DateTime, default=datetime.now)

    ball_id = db.Column(db.Integer, db.ForeignKey('ball.id'))  # 球队id外键
    balls = db.relationship('Ball', backref='matchs')
    """
    # t = time.time()
    # a = Ball.query.filter(Ball.id == 2).first()
    # b = Ball.query.filter(Ball.id == 3).first()
    #
    # m = Match(match_time=t,
    #           main_team=a.id,
    #           guest_team=b.id,
    #           z_score=2,
    #           k_score=1)
    # db.session.add(m)
    # db.session.commit()
    # print(m.id)

    # now_time = "2018-06-14 23:00:00"
    a = "2018-06-15 20:00:00"
    a1 = "2018-06-20 2:00:00"
    a2 = "2018-06-20 23:00:00"
    a3 = "2018-06-25 22:00:00"
    l = [a, a1, a2, a3]
    for i in l:
        x = time.mktime(time.strptime(time.strftime(i), "%Y-%m-%d %H:%M:%S"))
        print(x)

    return 'ok!'


# 球队列表
@bp.route('/ball_list')
def ball_list():
    # api/ball_list?pageIndex=1&per_page=5
    arr = []
    page = request.args.get('pageIndex', 1, type=int)
    per_page = request.args.get('per_page')
    pagination = Ball.query.order_by('create_time').paginate(page, per_page=int(per_page), error_out=False)
    p = pagination.items
    t = pagination.total
    for i in p:
        arr.append(row2dict(i))
    return ApiResult().formattingData(status=200, msg='', data={
        'records': arr,
        'now_page': page,
        'totalAmount': t

    })


# 每个小组净胜球最多的球队
@bp.route('/ball_MaxClean')
def get_max_clean():
    d = {}
    result = db.session.query(Ball, func.max(Integral.clean)).join(Integral).group_by(Ball.in_group).order_by(
        func.count(Integral.id).desc()).all()
    print(result)
    for res in result:
        # assert isinstance(res, Ball)
        zu = res.Ball.in_group
        qiu = res.Ball.name
        d[zu] = qiu
    print(d)
    return ApiResult().formattingData(status=200, msg='', data=d)


# 比分差距最大的3场比赛记录(按照比赛日期逆序排序)
@bp.route('/ball_MaxScore')
def get_max_score():
    d = {}
    # m = db.session.query(Match).order_by(func.count(Match.z_score - Match.k_score).desc())
    # print(m)

    # db_engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    # db_conn = db_engine.connect()
    # x = db_conn.execute("SELECT * FROM match ORDER BY match.z_score - match.k_score DESC").fetchall()
    # print(x)

    r = db.session.query(Match).from_statement(
        text("SELECT * FROM match ORDER BY match.z_score - match.k_score DESC,MATCH.match_time DESC")).all()
    # assert isinstance(r, Match)
    # print(r[0:3])
    # print(r.main_team)
    # print(r.guest_team)
    # print(r.z_score)
    # print(r.k_score)

    for i in r[0:3]:
        # print(i)
        b1 = Ball.query.filter(Ball.id == i.main_team).first()
        b2 = Ball.query.filter(Ball.id == i.guest_team).first()

        d['{}vs{}'.format(b1.name, b2.name)] = '分差:{}'.format(i.z_score - i.k_score)
        # print(b1.name)
        # print(b2.name)

    return ApiResult().formattingData(status=200, msg='', data=d)


# 每个小组晋级的两只球队(排名优先级：积分、净胜球、球队名)
@bp.route('/ball_Promotion')
def ball_promotion():
    pass
