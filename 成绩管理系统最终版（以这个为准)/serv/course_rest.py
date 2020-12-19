import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps

from .config import db_block, web_routes


@web_routes.get("/api/course/list")
async def get_course_list(request):
    with db_block() as db:
        db.execute("""
        SELECT sch_term, cou_plan_sn ,cou_plan_name, cou_plan_time, cou_plan_place
        FROM course_plan as g
            INNER JOIN course as c  ON g.cou_plan_sn = c.sn
        ORDER BY cou_plan_sn;
        """)     
        data = list(asdict(r) for r in db)
        
    return web.Response(text=json_dumps(data), content_type="application/json")


@web_routes.get("/api/course/{cou_plan_sn:\d+}")
async def get_course_profile(request):
    cou_plan_sn = request.match_info.get("cou_plan_sn")

    with db_block() as db:
        db.execute("""
        SELECT cou_plan_sn ,sch_term,   cou_plan_name, cou_plan_time, cou_plan_place FROM course_plan
        WHERE cou_plan_sn=%(cou_plan_sn)s
        """, dict(cou_plan_sn=cou_plan_sn))
        record = db.fetch_first()

    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")

@web_routes.post("/api/course")
async def new_course(request):
    course_plan = await request.json()
    sch_term = course_plan.get("sch_term")
    cou_plan_name = course_plan.get("cou_plan_name")
    cou_plan_time = course_plan.get("cou_plan_time")
    cou_plan_place = course_plan.get("cou_plan_place")
    with db_block() as db:
        db.execute("""
        SELECT sn FROM course
        WHERE name=%(cou_plan_name)s
        """, dict(cou_plan_name=cou_plan_name))
        record = db.fetch_first()
    with db_block() as db:     
        db.execute("""
        INSERT INTO course_plan (cou_plan_sn,sch_term, cou_plan_name, cou_plan_time,cou_plan_place)
        VALUES(%(sn1)s,%(sch_term)s,  %(cou_plan_name)s, %(cou_plan_time)s,%(cou_plan_place)s) RETURNING cou_plan_sn;
        """, dict(sn1=record.sn,sch_term=sch_term,cou_plan_name=cou_plan_name,cou_plan_time=cou_plan_time,cou_plan_place=cou_plan_place))
        record = db.fetch_first()

        course_plan["cou_plan_sn"] = record.cou_plan_sn
    
    print(course_plan)

    return web.Response(text=json_dumps(course_plan), content_type="application/json")


@web_routes.put("/api/course/{cou_plan_sn:\d+}")
async def update_course(request):
    cou_plan_sn = request.match_info.get("cou_plan_sn")

    course_plan = await request.json()

    course_plan["cou_plan_sn"] = cou_plan_sn

    with db_block() as db:
        db.execute("""
        UPDATE course_plan SET
            sch_term=%(sch_term)s, cou_plan_name=%(cou_plan_name)s, cou_plan_time=%(cou_plan_time)s, cou_plan_place=%(cou_plan_place)s
        WHERE cou_plan_sn=%(cou_plan_sn)s;
        """, course_plan)

    return web.Response(text=json_dumps(course_plan), content_type="application/json")



@web_routes.delete("/api/course/{cou_plan_sn:\d+}/{sch_term:\d+}")
async def delete_course(request):
    cou_plan_sn = request.match_info.get("cou_plan_sn")
    sch_term = request.match_info.get("sch_term")

    with db_block() as db:
        db.execute("""
        DELETE FROM course_plan WHERE cou_plan_sn=%(cou_plan_sn)s AND sch_term=%(sch_term)s;
        """, dict(cou_plan_sn=cou_plan_sn,sch_term=sch_term))
    with db_block() as db:
        db.execute("""
        DELETE FROM course_grade WHERE cou_sn=%(cou_plan_sn)s AND sch_term=%(sch_term)s;
        """, dict(cou_plan_sn=cou_plan_sn,sch_term=sch_term))

    return web.Response(text="", content_type="text/plain")
