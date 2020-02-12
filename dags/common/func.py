# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import psycopg2
import petl as etl


def db_connection(host, dbname, user, password, port):
    connection = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    return connection.cursor()

def check_grade_number(grade):
    number_grade = ''
    grade = str(grade)
    for i in grade:
        if i is '.' or i.isdigit() is not False:
            number_grade = number_grade + i
    return number_grade

def check_comma_number(number):
    number_not_comma = ''
    for i in number:
        if i.isdigit() is not False:
            number_not_comma = number_not_comma + i
    return number_not_comma

def convert_date_th(date):
    date = str(date)
    d = date.split(' ')
    dd = m = y = ''
    count = 0
    for i in d:
        if i == 'ม.ค.':
            m = '01'
        elif i == 'ก.พ.':
            m = '02'
        elif i == 'มี.ค.':
            m = '03'
        elif i == 'เม.ย.':
            m = '04'
        elif i == 'พ.ค.':
            m = '05'
        elif i == 'มิ.ย.':
            m = '06'
        elif i == 'ก.ค.':
            m = '07'
        elif i == 'ส.ค.':
            m = '08'
        elif i == 'ก.ย.':
            m = '09'
        elif i == 'ต.ค.':
            m = '10'
        elif i == 'พ.ย.':
            m = '11'
        elif i == 'ธ.ค.':
            m = '12'
        if i != '' and count == 0:
            dd = i
            count += 1
        elif i != '' and count == len(d):
            m = i
        elif i != '':
            y = i
    date = dd + '/' + m + '/' + y
    date = datetime.strptime(date, '%d/%m/%Y')
    date = date.date()
    return date

def change_format_date(date):
    oldformat = date
    datetimeobject = datetime.strptime(oldformat, '%Y/%m/%d')
    newformat = datetimeobject.strftime('%Y-%m-%d')
    return newformat

def change_slash_date(input):
    return datetime.strptime(input, '%m/%d/%Y')

def validate(cursor, table, constraints, task_name):
    header = etl.header(table)
    problems = etl.validate(table, constraints=constraints, header=header)
    problems = etl.addfield(problems, 'task_name', task_name)
    problems = etl.addfield(problems, 'create_date', datetime.now())

    # etl.todb(problems, cursor, 'etl_logs')
    etl.appenddb(problems, cursor, 'tetl_logs')


def cvt_buddhist_year_minus(input):
    return datetime(int(input.year) - 543, int(input.month), int(input.day))


def cvt_date_dmy_slash(input):
    return datetime.strptime(input, "%d/%m/%Y")


def cvt_date_ymd_slash(input):
    return datetime.strptime(input, "%Y/%m/%d")
