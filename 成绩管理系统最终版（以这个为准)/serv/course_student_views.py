from aiohttp import web
from .config import db_block, web_routes, render_html



@web_routes.get("/student/course_student")
async def view_list_grades(request):
    with db_block() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)
        
        db.execute("""
        SELECT sn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)
   
        db.execute("""
        SELECT cou_plan_sn, sch_term ,cou_plan_name,cou_plan_time,cou_plan_place FROM course_plan ORDER BY cou_plan_name
        """)
        course_plan = list(db)

        db.execute("""
        SELECT g.stu_sn, g.cou_sn, 
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade ,
            cp.cou_plan_sn,cp.sch_term,cp.cou_plan_time,cp.cou_plan_place,cp.cou_plan_name
        FROM course_grade as g
            INNER JOIN student as s ON g.stu_sn = s.sn
            INNER JOIN course as c  ON g.cou_sn = c.sn
            INNER JOIN course_plan as cp  ON cp.cou_plan_sn = c.sn
        ORDER BY stu_sn, cou_sn;
        """)

        items = list(db)

    return render_html(request, 'course_student.html',
                       students=students,
                       courses=courses,
                       course_plan=course_plan,
                       items=items)

@web_routes.get('/student/course_student/edit/{sch_term}/{stu_sn}/{cou_sn}')
def view_grade_editor(request):
    sch_term = request.match_info.get("sch_term")
    stu_sn = request.match_info.get("stu_sn")
    cou_sn = request.match_info.get("cou_sn")
    

    with db_block() as db:
        db.execute("""
        SELECT grade FROM course_grade
            WHERE stu_sn = %(stu_sn)s AND cou_sn = %(cou_sn)s AND sch_term=%(sch_term)s;
        """, dict(stu_sn=stu_sn, cou_sn=cou_sn ,sch_term=sch_term))
    
        record = db.fetch_first()

    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sn}, cou_sn={cou_sn},sch_term={sch_term}")
    
    return render_html(request, "course_student_edit.html",
                       stu_sn=stu_sn,
                       cou_sn=cou_sn,
                       sch_term=sch_term,
                       grade=record.grade)
