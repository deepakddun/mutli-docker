from flask import Flask, render_template, redirect, url_for
from server.server import redis_subscr
import mysql.connector
from server import keys
import redis
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'


redis_client = redis.Redis(host=keys.REDIS_HOST, port=keys.REDIS_PORT,db=0,decode_responses=True)
conn = mysql.connector
sql_conn = None
pubsub = None



@app.before_first_request
def create_tables():
    print("KEYS",flush=True)
    print(keys.mysql_host,flush=True)
    print(keys.mysql_username, flush=True)
    print(keys.mysql_pass, flush=True)
    print(keys.mysql_db, flush=True)
    print(keys.myPort, flush=True)
    print('BEFORE FIRST REQUEST',flush=True)
    try:
        print('Inside try',flush=True)
        global sql_conn
        sql_conn = conn.connect(host=keys.mysql_host, user=keys.mysql_username, password=keys.mysql_pass,
                                database=keys.mysql_db, port=keys.myPort)
        my_cur = sql_conn.cursor()
        my_cur.execute("create table if not exists numbers ( num INTEGER );")
        sql_conn.commit()
        my_cur.execute("show tables;")
        myresult = my_cur.fetchall()
        print('PRINTING RESULT',flush=True)
        for res in myresult:
            print(res,flush=True)
    except conn.Error as error:
        print('Inside line 36',flush=True)
        print(error)


@app.route("/")
def index():
    return "Hi"


@app.route("/values/all")
def getAllValues():
    global sql_conn
    mycursor = sql_conn.cursor()
    mycursor.execute("SELECT * FROM numbers;")
    myresult = mycursor.fetchall()
    mycursor.close()
    return render_template("home.html", data=myresult)


class InfoForm(FlaskForm):
    breed = StringField(label='Please enter breed')
    submit = SubmitField(label='Submit')


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = InfoForm()
#
#     if form.validate_on_submit():
#         session['breed'] = form.breed.data
#         flash(f"you have entered {session['breed']}")
#
#         return redirect((url_for('index')))
#
#     return render_template('index.html', form=form)
def event_handler(msg):
    print("Handler",msg,flush=True)


@app.route('/values', methods=['GET', 'POST'])
def getCurrentValues():
    form = InfoForm()
    global sql_conn
    # resultSetfromDB = readvaluesfromDataBase()
    # resultSetfromReds = readValueFromRedis()
    print(sql_conn,flush=True)
    if form.validate_on_submit():
        value = form.breed.data
        if int(value) >= 40:
            return "index too high"

        redis_client.hset('values', value, 'Nothing yet')
        redis_client.publish("insert", value)


        #print(redis_client.memory_stats(),flush=True)

        query = f'INSERT INTO numbers (num) VALUES ({int(value)});'
        print(query,flush=True)
        mycursor = sql_conn.cursor()
        mycursor.execute(query)
        sql_conn.commit()
        print(mycursor.rowcount, "was inserted.",flush=True)
        resultSetfromDB = readvaluesfromDataBase()
        resultSetfromReds = readValueFromRedis()
        form.breed.data=""

        return render_template('index.html', form=form , db = resultSetfromDB , mem = resultSetfromReds)
        #return render_template(url_for("getCurrentValues",db = resultSetfromDB , mem = resultSetfromReds))
    resultSetfromDB = readvaluesfromDataBase()
    resultSetfromReds = readValueFromRedis()
    return render_template('index.html', form=form , db = resultSetfromDB , mem = resultSetfromReds)


def readValueFromRedis():

    #redis_client = redis.Redis(host=keys.REDIS_HOST, port=keys.REDIS_PORT, decode_responses=True, charset='utf-8')

    resultset = redis_client.hgetall('values')
    return resultset

def readvaluesfromDataBase():
    global sql_conn
    mycursor = sql_conn.cursor()
    mycursor.execute("select num from numbers;")
    resultset = mycursor.fetchall()
    for test in resultset:
        print(test,flush=True)

    # concert list of tuple(1) to list of values
    list_values = [tup[0] for tup in resultset]
    # convert list of values to string
    string_values = ' '.join(str(val) for val in list_values)
    return string_values
