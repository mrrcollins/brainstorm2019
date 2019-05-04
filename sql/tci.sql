select
    substr(firstname,1,1) AS first_initial,
    lastname AS last_name,
    username as username,
    password as password,
    password as password_confirmation,
    "" as teacher_email,
    CASE
        WHEN studentschedule.grade = "08" AND class_name = 'Social Studies' THEN 'MS9398'
        WHEN studentschedule.grade = "07" AND class_name = 'Social Studies' THEN 'MS2061'
        WHEN studentschedule.grade = "06" AND class_name = 'Social Studies' THEN 'MS2047'
        WHEN studentschedule.grade = "05" AND class_name = 'Science' THEN 'EL9817'
        WHEN studentschedule.grade = "05" AND class_name = 'Social Studies' THEN 'ELOH5T'
        WHEN studentschedule.grade = "04" AND class_name = 'Science' THEN 'EL9763'
        WHEN class_name = 'WORLD STUDIES' THEN 'HS9459'
        WHEN class_name = 'U.S. STUDIES' THEN 'HS0854'
    END AS program_code,
    cast(period as signed) as class_period
from users,studentschedule
where
    users.type='student' AND users.status='Active'
    AND users.uid=`studentschedule`.`student_id`
    AND
        (
            (`studentschedule`.`class_name` = 'Social Studies' AND studentschedule.grade = "06")
            OR
            (`studentschedule`.`class_name` = 'Social Studies' AND studentschedule.grade = "05")
            OR
            (`studentschedule`.`class_name` = 'Science' AND studentschedule.grade = "05")
            OR
            (`studentschedule`.`class_name` = 'Social Studies' AND studentschedule.grade = "08")
            OR
            (`studentschedule`.`class_name` = 'Social Studies' AND studentschedule.grade = "07")
            OR
            (`studentschedule`.`class_name` = 'Science' AND studentschedule.grade = "04")
            OR
            (`studentschedule`.`class_name` = 'WORLD STUDIES')
            OR
            (`studentschedule`.`class_name` = 'U.S. STUDIES')
         )

