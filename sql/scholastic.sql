select 
    username as USER_NAME,
    password as PASSWORD,
    uid as SIS_ID,
    firstname as FIRST_NAME,
    lastname as LAST_NAME,
    if((31-substr(username,1,2)) = 0, 'K', (31-substr(username,1,2))) AS GRADE,
    "Elementary School" AS SCHOOL_NAME,
    studentschedule.teacher_code AS CLASS_NAME
from studentschedule
INNER JOIN users ON studentschedule.student_id = users.uid
where
    users.type='student' AND users.status='Active'
    AND users.building LIKE '%Elementary%'
    AND
    (
    `studentschedule`.class_name LIKE '%Lang% Arts%'
        OR
    `studentschedule`.`class_name` LIKE '%CC-ELA 4-6%'
    )

