from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode

from .config import db_block, web_routes

@web_routes.post('/action/grade/add')
async def action_grade_ad(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    if stu_sn is None :
        return web.HTTPBadRequest(text="stu_sn must be required")   

    with db_block() as db:
        db.execute("""
        DELETE FROM course_grade
            WHERE stu_sn != %(stu_sn)s
        """, dict(stu_sn=stu_sn))



    return web.HTTPFound(location="/student/grade")

