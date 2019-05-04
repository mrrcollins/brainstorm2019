select uid as `SIS Primary Key`,
    concat(username,"@highschool") AS `username`,
    concat(upper(substr(firstname,1,1)),lower(substr(firstname,2))) AS `first name`,
    concat(upper(substr(lastname,1,1)),lower(substr(lastname,2))) AS `last name`,
    `password` as `password`,
    31-substr(username,1,2) AS `grade`
from users 
where building='High School' 
AND type='student' 
AND status='Active'

