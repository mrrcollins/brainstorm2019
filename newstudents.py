#!/usr/bin/python

from subprocess import Popen, PIPE, call
import ConfigParser,sys,crypt,random,os,shlex,re
import MySQLdb as mdb
import smtplib

# Email Setup
server      = "MAILSERVER"
sender      = 'FROMEMAILADDRESS'
receiver    = ['TO1','TO2']
hsreceivers = ['HS1','HS2']
msreceivers = ['MS1','MS2']

# Constants

categories = { 'e': 'certified', 'l': 'classified', 's': 'subs', 'n': 'none'}
buildings = { 'CE' : 'Elementary School',
              'MS' : 'Middle School',
              'HS' : 'High School'}
ous = { 'CE' : 'EL',
        'MS' : 'MS',
        'HS' : 'HS'}
schoolyear = 2019
domain = "GOOGLEDOMAIN"
# While testing, use echo instead of gam
#gampy = "/usr/local/bin/gam"
gampy = "echo"

new = 0
reactivated = 0
deactivated = 0

# Functions

def createpw():
    words = [ "beads", "boles", "tubed", "cants", "stoic", "midst", "curse", "stack", "enemy", "hafts", "sauna", "blues", "skier", "glads", "memos", "uteri", "nifty", "harry", "began", "grits" ]

    pw = random.choice(words)
    pw+= str(random.randint(0,9))
    pw+= str(random.randint(0,9))
    pw+= str(random.randint(0,9))
    pw+= str(random.randint(0,9))

    return pw

def gam(args):
    global gampy
    cmd = shlex.split(gampy + " " + args)
    stdout,stderr = Popen(cmd,stdout=PIPE).communicate()
    return stdout.splitlines()

def status(uid):
    q = "SELECT uid,status FROM users WHERE uid = %s"
    p = (uid,)

    try:
        cur.execute(q,p)
    except:
        print(cur._last_executed)
        exit()

    if cur.rowcount == 0:
        status = 'new'
    else:
        row = cur.fetchone()
        status = row["status"]

    return status

def newstudent(s):
    global new
    student_id  = s["student_id"]
    grade       = s["grade"]
    first_name  = re.sub(r'[^a-zA-Z]','',s["first_name"])
    last_name   = re.sub(r'[^a-zA-Z]','',s["last_name"])
    b           = buildings[s["building_code"]]
    fullname    = last_name + ", " + first_name

    if grade == "KG":
        grade = "0"

    if grade !='KG' and grade != 'PS':
        grade = int(grade)
        gradyear = schoolyear+12-int(grade)

        username = str(gradyear)[2:4]
        username+= last_name[0:4].lower()
        username+= first_name.lower()

        email = username + "@" + domain

        if grade > 6:
            password = createpw()
        else:
            password = "lead" + str(student_id)[-5:]

        print "Creating " + username + " with a password of " + password + "..."
        
        if grade > 6:
            print "Need laptop for " + fullname + " (" + str(student_id) + "), " + username

        q = "INSERT INTO users (uid,username,firstname,lastname,fullname,emailaddress,password,type,building) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        p = (student_id,username,first_name,last_name,fullname,email,password,"student",b)
        try:
            cur.execute(q,p)
        except:
            print "An error occurred when saving the record to MySQL"
            print(cur._last_executed)
            exit()

        print "Creating Google account for " + first_name + "..."
        out = gam("create user " + email + " firstname " + first_name + " lastname " + last_name + " password " + password)
        out = gam("update user " + email + " ou Students/" + ous[s["building_code"]] +"/" + str(gradyear))

        new+=1
    
def reactivate(s):
    global reactivated

    student_id  = s["student_id"]
    grade       = s["grade"]
    first_name  = s["first_name"]
    last_name   = s["last_name"]
    b           = buildings[s["building_code"]]
    fullname    = last_name + ", " + first_name

    if grade == "KG":
        grade = "0"

    if grade !='KG' and grade != 'PS':
        q = "SELECT username,password FROM users WHERE uid = %s"
        p = (student_id,)
        try:
            cur.execute(q,p)
        except:
            print(cur._last_executed)
            exit()

        row = cur.fetchone()
        username = row["username"]
        password = row["password"]

        gradyear = schoolyear+12-int(grade)
        email = username + "@" + domain
        vusername = str(gradyear)[2:4]
        vusername+= re.sub(r'[^a-zA-Z]','',last_name[0:4].lower()) 
        vusername+= re.sub(r'[^a-zA-Z]','',first_name.lower())

        if (int(grade) > 6 and password[-5:] == str(student_id)[-5:]) or (password == str(student_id)):
            print "Changing password from " + password
            password = createpw()

        if vusername == username:
            print "Re-activating " + username + " with a password of " + password
        else:
            print "Student was held back..."
            username = vusername
            out = gam("update user " + email + " username " + username + " password " + password + " ou Students/" + ous[s["building_code"]] +"/" + str(gradyear) + " suspended off")
            email = username + "@" + domain

        if grade > 6:
            print "Need laptop for " + fullname + " (" + str(student_id) + "), " + username

        q = "UPDATE users SET status = %s, username = %s, password = %s, emailaddress = %s, building = %s WHERE uid = %s"
        p = ("Active",username,password,email,b,student_id)

        try:
            cur.execute(q,p)
        except:
            print "An error occurred when saving the record to MySQL"
            print(cur._last_executed)
            exit()
        print("update user " + email + " ou Students/" + ous[s["building_code"]] +"/" + str(gradyear) + " suspended off")
        out = gam("update user " + email + " ou Students/" + ous[s["building_code"]] +"/" + str(gradyear) + " suspended off")
        
        reactivated+= 1

def sendemail(s,g,name,laptopid):

    if g >= 9:
        to = hsreceivers
    elif g >= 7:
        to = msreceivers
    else:
        to = receiver
        
    if s == "new":
        subject = "Laptop for " + name
    else:
        subject = "Retrieve laptop " + laptopid + " from " + name + " (if assigned)"

    text = "Thanks!"

    message = """\
    FROM: %s
    TO: %s
    SUBJECT: %s

    %s
    """ % (sender, ", ".join(to),subject,text)

    email = smtplib.SMTP(server)
    email.sendmail(sender,to,message)
    email.quit()

def procoreemail(g,name,sid):

    to = "PROCOREEMAIL"
    subject = "New student, " + name + " (" + str(sid) + ") in grade " + str(g) 
    text = "\nTerm, School, Class Name, Class ID, Class Period, Teacher Code\n" 

    # Get schedule
    q = "SELECT term,building_code,class_name,class_code,period,teacher_code FROM studentschedule WHERE student_id = %s"
    p = (sid)
    cur.execute(q,p)
    result = cur.fetchall()

    for row in result:
        text = text + row["Term"]+", "+row["School"]+", "+row["Class Name"]+", "+row["Class ID"]+", "+row["Class Period"]+", "+row["teacher_code"]+"\n"
        
    
    text = text + "\n\nThanks!"

    message = """\
    FROM: %s
    TO: %s
    SUBJECT: %s

    %s
    """ % (sender, ", ".join(to),subject,text)
    
    cmd = shlex.split("sendEmail -f " + sender + " -t " + to + " -u \"" + subject + "\"  -m \"" + text + "\"")
    stdout,stderr = Popen(cmd,stdout=PIPE).communicate()
    # print text


# Connection to MySQL

config = ConfigParser.ConfigParser()
config.read('mysql.cfg')

dbhost = config.get('mysql','host')
dbuser = config.get('mysql','user')
dbpass = config.get('mysql','pass')
db = config.get('mysql','db')

m = mdb.connect(dbhost,dbuser,dbpass,db)
m.autocommit(True)
cur = m.cursor(mdb.cursors.DictCursor)

# Main Loop

q = "SELECT student_id, grade, first_name, last_name, building_code FROM newstudents"
cur.execute(q,)
numrows = cur.rowcount

if numrows == 0:
    print "No new students."
else:
    result = cur.fetchall()

    for row in result:

        student_id  = row["student_id"]
        grade       = row["grade"]
        first_name  = row["first_name"]
        last_name   = row["last_name"]
        b           = row["building_code"]

        #if grade != "PS":
        #    procoreemail(grade,first_name + " " + last_name,student_id)

        if status(student_id) == "new":
            #print "New student " + first_name + " " + last_name + "..."
            newstudent(row)
            #sendemail
            #sendemail("new",grade,first_name + " " + last_name + " @ " + b,"0")
        elif status(student_id) == "inactive":
            #print "Re-activating " + first_name + " " + last_name + "..."
            reactivate(row)
            #sendemail("new",grade,first_name + " " + last_name + " @ " + b,"0")
        else:
            print "There is a problem with " + first_name + " " + last_name + "..."


## Deactivate students

q = "SELECT student_id,username FROM leftstudents"
cur.execute(q,)

if cur.rowcount == 0:
    print "No withdrawals."
else:
    result = cur.fetchall()

    for row in result:
        student_id  = row["student_id"]
        username    = row["username"]

        q = "SELECT asset FROM chromebooks WHERE uid = %s"
        p = (student_id,)
        cur.execute(q,p)

        r = cur.fetchone()
        try:
            asset = r["asset"]
        except:
            asset = "none assigned"

        print "De-activating " + username + " with a laptop of " + str(asset) + "..."
        print "Collect laptop " + str(asset) + " from " + username + "(" + str(student_id) + ")"

        #sendemail("left",grade,first_name + " " + last_name + " @ " + b,str(asset))

        out = gam("update user " + username + " suspended on")
        
        q = "UPDATE users SET status = %s WHERE uid = %s"
        p = ("inactive",student_id)
        cur.execute(q,p)
        deactivated+=1

print "Created " + str(new) + " students, reactivated " + str(reactivated) + " students, and deactivated " + str(deactivated) + "."

cur.close()
