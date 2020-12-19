from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/cou_stu_del/add')
async def action_grade_add(request):
    params = await request.post()
    cou_plan_name = params.get("cou_plan_name")
    sch_term = params.get("sch_term")
    if  sch_term is None:
       return web.HTTPBadRequest(text="sch_term, must be required")
    if cou_plan_name is  None:
        return web.HTTPBadRequest(text="cou_plan_name, must be required")

    with db_block() as db:
        db.execute("""
        DELETE FROM course_grade
            WHERE cou_plan_name != %(cou_plan_name)s
        """, dict(cou_plan_name=cou_plan_name,sch_term=sch_term))
        db.execute("""
        DELETE FROM course_plan
            WHERE cou_plan_name != %(cou_plan_name)s
        """, dict(cou_plan_name=cou_plan_name,sch_term=sch_term))


    return web.HTTPFound(location="/student/course_student")

@web_routes.post('/action/student/course_student/edit/{sch_term}/{stu_sn}/{cou_sn}')
async def edit_grade_action(request):
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    sch_term = request.match_info.get("sch_term")
    if stu_sn is None or cou_sn is None or sch_term is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn,sch_term must be required")
    
    params = await request.post()
    grade = params.get("grade")
    
    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
        grade = float(grade)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    with db_block() as db:
        db.execute("""
        UPDATE course_grade SET grade=%(grade)s
        WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s AND sch_term=%(sch_term)s
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn, grade=grade,sch_term=sch_term))

    return web.HTTPFound(location="/student/course_student")
