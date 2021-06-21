from flask import Flask, request, render_template, redirect, url_for,flash
import pymysql

global id
global password
global teacher_id
global teacher_password
global table_name
app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
#for students
def login():
    return render_template("login.html")

#for teachers
@app.route('/login_teacher')
def login_teacher():
    return render_template("login_teacher.html")

#for student
@app.route('/logout')
def logout():
    return render_template('login.html')

#for teachers
@app.route('/logout_teacher')
def logout_teacher():
    return render_template('login_teacher.html')


#for student

@app.route('/forgot_password')
def forgot_password():

   return render_template("forgot.html")

#for teachers
@app.route('/forgot_password_teacher')
def forgot_password_teacher():
    return render_template("forgot_teacher.html")

#for students
@app.route('/update_password',methods=["POST"])
def update_password():
    print("update")
    student_ids=['100','101','102','103','104','105','106','107','108','109']
    student_id=request.form['student_id1']
    upassword = request.form['password1']
    reupassword = request.form['password11']
    values=(upassword,student_id)
    if student_id not in student_ids:
        flash("Invalid Student ID!!!",  category="error")
        return render_template('forgot.html')
    elif (upassword !=reupassword):
        flash("Passwords do not match!!! Please try again", category="error")
        return render_template('forgot.html')
    else:
        try:
            db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                                 database="dbms", autocommit=True)
            cur = db.cursor()
            query = "update student_details set password=%s where student_id=%s "
            cur.execute(query, values)
            print("updated")
            flash("Password updated. Please Login", category="error")
            db.close()
            return render_template('forgot.html')
        except pymysql.err.OperationalError:
            flash("Check your internet connection!!!")
            return redirect(url_for('forgot'))
        except Exception as e:
            return "this is error page"

#for teachers
@app.route('/update_password_teacher',methods=["POST"])
def update_password_teacher():
    teacher_ids = ['1000','1001','1002','1003','1004','1005','1006','1007','1008','1009']
    teacher_id = request.form['teacher_id1']
    upassword = request.form['password1']
    reupassword = request.form['password11']
    values = (upassword, teacher_id)
    if teacher_id not in teacher_ids:
        flash("Invalid Teacher ID", category="error")
        return render_template('forgot_teacher.html')
    elif (upassword != reupassword):
        flash("Passwords do not match!!! Please try again", category="error")
        return render_template('forgot_teacher.html')
    else:
        try:
            db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                                 database="dbms", autocommit=True)
            cur = db.cursor()
            query = "update teacher_details set password=%s where teacher_id=%s "
            cur.execute(query, values)
            print("updated")
            flash("Password updated. Please Login", category="error")
            db.close()
            return render_template('forgot_teacher.html')
        except pymysql.err.OperationalError:
            flash("Check your internet connection!!!")
            return redirect(url_for('login'))
        except Exception as e:
            return "this is error page"


#home page for students
@app.route('/home',methods=["POST"])
def home():
    global id
    global password
    print("home")
    id=request.form['student_id']
    print(id)
    password=request.form['password']
    student_ids = ['100','101','102','103','104','105','106','107','108','109']
    if id not in student_ids:
        flash("Invalid Student Id!!!", category="error")
        return redirect(url_for('login'))
    else:
        try:
            db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                                 database="dbms", autocommit=True)
            cur = db.cursor()
            query = "select * from student_details"
            exe = cur.execute(query)
            data = cur.fetchall()
            db.close()
            for i in range(0, len(data)):
                if id == str(data[i][0]) and password == str(data[i][1]):
                    return render_template("home.html")

            flash("Invalid Password!!!", category="error")
            return redirect(url_for('login'))
        except pymysql.err.OperationalError:
            flash("Check your internet connection",category="error")
            return redirect(url_for('login'))

        except Exception as e:
            return "this is error page"



#home page for teachers
@app.route('/home_teacher',methods=["POST"])
def home_teacher():
    global teacher_id
    global teacher_password
    print("hometacher")
    teacher_id=request.form['teacher_id']
    teacher_password=request.form['teacher_password']
    teacher_ids=['1000','1001','1002','1003','1004','1005','1006','1007','1008','1009']
    if teacher_id not in teacher_ids:
        flash("Invalid Teacher Id!!!", category="error")
        return redirect(url_for('login_teacher'))
    else:

       db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                            database="dbms", autocommit=True)
       cur = db.cursor()
       query = "select * from teacher_details"
       exe = cur.execute(query)
       data = cur.fetchall()
       db.close()
       for i in range(0, len(data)):
           if teacher_id == str(data[i][0]) and teacher_password == str(data[i][1]):
               return render_template("home_teacher.html")

       flash("Invalid Password!!!", category="error")
       return redirect(url_for('login_teacher'))

@app.route('/home')
def home_menu():
    return render_template('home.html')



@app.route('/home_')
def home_menu_teacher():
    return render_template('home_teacher.html')

@app.route('/queries')
def queries():
    return render_template('queries.html')

@app.route('/update')
def update():
    return render_template('update_attendence.html')



#for students
@app.route('/python_attendence',methods=["POST"])
def attendence_percentage_python():
    global table_name
    table_name = "python"
    subject_name = "PYTHON"
    print(table_name)
    student_id=id
    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)
       # db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
        #                     database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        query = "select * from python_attendence where student_id=(%s) "
        studentid = (student_id)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data,subject_name=subject_name)
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('home'))
    except Exception as e:
        return "this is error page"



#for teachers
@app.route('/python_attendence_teacher', methods=["POST"])
def attendence_percentage_python_teacher():
    global table_name
    table_name="python"
    print(table_name)

    db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                         database="dbms", autocommit=True)
    cur = db.cursor()
    q = "select sub_code from python_attendence"
    cur.execute(q)
    sub_code_tuple = cur.fetchone()
    sub_code = sub_code_tuple[0]
    query = "select * from python_attendence "
    q = cur.execute(query)
    data = cur.fetchall()
    db.close()
    return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)


#for students
@app.route('/java_attendence',methods=["POST"])
def attendence_percentage_java():
    student_id = id
    global table_name
    table_name = "java"
    subject_name = "JAVA"
    print(table_name)
    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)

        # db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
        #                     database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        query = "select * from java_attendence where student_id=(%s) "
        studentid = (student_id)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data,subject_name=subject_name)
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))
    except Exception as e:
        return "this is error page"




#for teachers
@app.route('/java_attendence_teacher', methods=["POST"])
def attendence_percentage_java_teacher():
    global table_name
    table_name = "java"
    print(table_name)
    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)

        cur = db.cursor()
        q = "select sub_code from java_attendence"
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]

        query = "select * from java_attendence "
        q = cur.execute(query)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))
    except Exception as e:
        return "this is error page"


#for students
@app.route('/javascript_attendence',methods=["POST"])
def attendence_percentage_javascript():
    global table_name
    table_name = "javascript"
    subject_name = "JAVASCRIPT"
    student_id = id
    print(table_name)
    print(student_id)

    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)

        cur = db.cursor()
        print('connected')
        query = "select * from javascript_attendence where student_id=(%s) "
        studentid = (student_id)
        print(studentid)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data, subject_name=subject_name)


    except pymysql.err.OperationalError:

        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))


    except Exception as e:
        return "this is error page"


#for teachers
@app.route('/javascript_attendence_teacher', methods=["POST"])
def attendence_percentage_javascript_teacher():
    global table_name
    table_name = "javascript"
    print(table_name)
    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)

        cur = db.cursor()
        q = "select sub_code from javascript_attendence"
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]
        query = "select * from javascript_attendence"
        q = cur.execute(query)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))
    except Exception as e:
        return "this is error page"

@app.route('/r_attendence',methods=["POST"])
def attendence_percentage_r():
    global table_name
    table_name = "r"
    subject_name = "R"
    student_id = id
    print(table_name)

    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)
        cur = db.cursor()
        query = "select * from r_attendence where student_id=(%s) "
        studentid = (student_id)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data,subject_name=subject_name)
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))
    except Exception as e:
        return "this is error page"



@app.route('/r_attendence_teacher', methods=["POST"])
def attendence_percentage_r_teacher():
    global table_name
    table_name = "r"
    print(table_name)
    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)

        cur = db.cursor()
        q = "select sub_code from r_attendence"
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]
        query = "select * from r_attendence"
        q = cur.execute(query)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))
    except Exception as e:
        return "this is error page"

#attendence details with date for students
@app.route('/attendence_details', methods=["POST"])
def attendence_details():
    print("im in")
    global id
    global table_name
    student_id=id
    table = table_name
    print(table)
    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                             database="dbms", autocommit=True)
        #db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
         #                    database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        print('connected')
        q = f"select subject_code from {table} where student_id= '{student_id}' "
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]

        query = f"select * from {table} where student_id='{student_id}'"
        cur.execute(query)
        data = cur.fetchall()

        status_list = []
        for i in data:
            for j in range(0, len(i)):
                if i[j] == None:
                    status_list.append('None')
                elif i[j].startswith('P') or i[j].startswith('p') or i[j].startswith('A') or i[j].startswith('a'):
                    status_list.append(i[j])
                else:
                    continue

        query = f"show columns from  {table}"
        cur.execute(query)
        column_names = cur.fetchall()
        db.close()
        date_list = []

        for i in column_names:
            if i[0].startswith("s"):
                continue
            else:
                inverted_comma_date = i[0][1:-1]
                date_list.append(inverted_comma_date)

        dict_details = {}

        for i in range(0, len(date_list)):
            dict_details[date_list[i]] = status_list[i]


        return render_template('attendence_details.html', data=data, Student_ID=student_id, Subject_Code=sub_code,
                               empty_dict=dict_details, len=len(date_list))
    except pymysql.err.OperationalError:
        flash("Check your internet connection",category="error")
        return redirect(url_for('login'))
    except Exception as e:
        return "this is error page"


#attendence details with date for teachers
@app.route('/attendence_details_teacher',methods=["POST"])
def attendence_details_teacher():
    global table_name
    student_id=request.form['stud_id']
    table = table_name

    print("kekekek")
    #try:
    db = pymysql.connect(host="localhost", user="root", password="keekkeek",
                         database="dbms", autocommit=True)
    # db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
    #                    database="sujithkh_maxo_project", autocommit=True)
    cur = db.cursor()
    q = f"select subject_code from {table} where student_id= '{student_id}' "
    cur.execute(q)
    sub_code_tuple = cur.fetchone()
    sub_code = sub_code_tuple[0]

    query = f"select * from {table} where student_id='{student_id}'"
    cur.execute(query)
    data = cur.fetchall()
    status_list = []
    for i in data:
        for j in range(0, len(i)):
            if i[j] == None:
                status_list.append('None')
            elif i[j].startswith('P') or i[j].startswith('p') or i[j].startswith('A') or i[j].startswith('a'):
                status_list.append(i[j])
            else:
                continue

    query = f"show columns from {table}"
    cur.execute(query)
    db.close()
    column_names = cur.fetchall()
    date_list = []

    for i in column_names:
        if i[0].startswith("s"):
            continue
        else:
            inverted_comma_date = i[0][1:-1]
            date_list.append(inverted_comma_date)

    dict_details = {}

    for i in range(0, len(date_list)):
        print(len)
        dict_details[date_list[i]] = status_list[i]
    print("keeeeeeeeeek")

    return render_template('attendence_details_teacher.html', data=data, Student_ID=student_id, Subject_Code=sub_code,
                           empty_dict=dict_details, len=len(date_list))


@app.route('/up_attendance')
def up_attendance():
    return render_template('update_attendence.html')


@app.route('/update_attendence', methods=['POST'])
def update_attendence():

    sub = request.form['subn']
    date = request.form['date']
    s0 = request.form['s0']
    s1 = request.form['s1']
    s2 = request.form['s2']
    s3 = request.form['s3']
    s4 = request.form['s4']
    s5 = request.form['s5']
    s6 = request.form['s6']
    s7 = request.form['s7']
    s8 = request.form['s8']
    s9 = request.form['s9']

    table_name = sub
    corr_table = f"{sub}_attendence"
    date = date.split('-')
    date = date[::-1]
    date = date[0] + "-" + date[1] + "-" + date[2]

    details = {'100':s0, '101':s1, '102':s2,'103':s3, '104':s4, '105':s5, '106':s6, '107':s7, '108':s8, '109':s9}

    try:
        db = pymysql.connect(host="localhost", user="root", password="keekkeek", database="dbms", autocommit=True)
        cur = db.cursor()
        print("connected")


        query = f"alter table {table_name} add column(`%s` varchar(20))"

        cur.execute(query,(date))

        date=f"'{date}'"

        print(date)

        for id, status in details.items():
            print(status, id)
            values = (status, id) #    print(values)
            update = f"update {table_name} set `{date}`=%s where student_id=%s "
            cur.execute(update, values)
            print("1 done")
        print(cur.fetchall())

        #updating the percentage table
        query = f"show columns from {table_name}"
        cur.execute(query)
        aa = cur.fetchall()
        no_of_classes_conducted = len(aa) - 2
        print(no_of_classes_conducted)
        student_ids = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109']
        for i in range(0, len(student_ids)):
            print(i)
            bb = f"select * from {table_name} where student_id='{student_ids[i]}'"
            cur.execute(bb)
            val = cur.fetchall()
            print( val)
            print(val[0])
            no_of_classes_attended = val[0].count('P' or 'p')
            print(no_of_classes_attended)
            attendence_percent =round((no_of_classes_attended / no_of_classes_conducted) * 100)
            print(attendence_percent)
            query = f"""update {corr_table} set No_of_classes_conducted='{no_of_classes_conducted}',
            No_of_classes_attended='{no_of_classes_attended}',
            percentage='{attendence_percent}'
            where student_id='{student_ids[i]}' """
            cur.execute(query)
            bbd=cur.fetchall()
            print(bbd)
            q=f"select * from {corr_table}"
            cur.execute(q)
            print(cur.fetchall())
        db.close()
        flash("Attendence Updated Sucessfully", category="error")
        return render_template('update_attendence.html')

    except Exception as e:
        return f"this is error page  {e}"
    #return "keekkekekekekke"


if __name__ =='__main__':
    app.run(debug=True, host="localhost", port=4001)