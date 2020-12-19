DELETE FROM course_grade;
DELETE FROM course;
DELETE FROM student;
DELETE FROM course_plan;

INSERT INTO student (sn, no, name)  VALUES
    (101, 'S001',  '张三'),
    (102, 'S002',  '李四'), 
    (103, 'S003',  '王五'),
    (104, 'S004',  '马六');

INSERT INTO course (sn, no, name)  VALUES 
    (101, 'C01',  '高数'), 
    (102, 'C02',  '外语'),
    (103, 'C03',  '线代');


INSERT INTO course_grade (sch_term,stu_sn, cou_sn, grade)  VALUES 
    ('2020-2021',101, 101,  0), 
    ('2020-2021',102, 101,  0),
    ('2021-2022',103, 101,  0),
    ('2021-2022',101, 102,  0);



INSERT INTO course_plan (sch_term, cou_plan_sn,cou_plan_name, cou_plan_time, cou_plan_place )  VALUES 
    ('2020-2021', 101,'高数', '周一上午第一大节','一公教A101'),
    ('2021-2022', 102,'外语', '周二上午第一大节','一公教B202');




    