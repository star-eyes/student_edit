from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes



@web_routes.post('/action/choose_course/add')
async def action_cou_grade_add(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    cou_sn = params.get("cou_sn")
    sch_term = params.get("sch_term")

    if stu_sn is None or cou_sn is None :
        return web.HTTPBadRequest(text="stu_sn, cou_sn, sch_term must be required")

    try:
        stu_sn = int(stu_sn)
        cou_sn = int(cou_sn)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    try:
        with db_block() as db:
            db.execute("""
            INSERT INTO course_grade (stu_sn, cou_sn, sch_term) 
            VALUES ( %(stu_sn)s, %(cou_sn)s, %(sch_term)s)
            """, dict(stu_sn=stu_sn, cou_sn=cou_sn, sch_term=sch_term))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message": "该学生已经选了这个课",
            "return": "/student/choose"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程: {ex}")

    return web.HTTPFound(location="/student/choose")

