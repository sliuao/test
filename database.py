import test
from test import db
from test import User
from test import employment
from sqlalchemy import text
from flask_login import login_manager

def insert_user():
	x = User('0','0','0','0','0','0','0','0','0','0')
	db.session.add(x)
	db.session.commit()

	return x.id

def update_user(userid, column, data):
	sql = text("update User set " + column +" = '"+data+"' where id="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def get_user(userid, column):
	sql = text("select " + column +" from User where id="+str(userid))
	result = db.engine.execute(sql)
	x = []
	for row in result:
		x.append(row[0])
	return x


def get_user_state(userid):
	state = get_user(userid, "state")
	state = int(state[0])
	return state

def insert_employment(userid):
	x = employment(userid,'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0')
	db.session.add(x)
	db.session.commit()

	return x.id

def update_employment(userid, column, data):
	sql = text("update employment set " + column +" = '"+data+"' where userid="+str(userid))
	db.engine.execute(sql)
	db.session.commit()

def update_employment_info(userid, state, message):
	if state==1:
		update_employment(userid, "employee_name", message)
	elif state==2:
		update_employment(userid, "employer_name", message)
	elif state==3:
		update_employment(userid, "company_name", message)
	elif state==4:
		update_employment(userid, "company_address", message)
	elif state==5:
		update_employment(userid, "employee_address", message)
	elif state==6:
		update_employment(userid, "job", message)
	elif state==7:
		update_employment(userid, "duty", message)
	elif state==9:
		update_employment(userid, "work_hour", message)
	elif state==10:
		update_employment(userid, "salary", message)
	elif state==11:
		update_employment(userid, "annual_leave", message)
	elif state==12:
		update_employment(userid, "commence", message)
	elif state==13:
		update_employment(userid, "ddl", message)
	elif state==15:
		update_employment(userid, "work_place", message)
	elif state==17:
		update_employment(userid, "duration", message)
	elif state==18:
		update_employment(userid, "advance", message)
	elif state==19:
		update_employment(userid, "insurance", message)
	elif state==20:
		update_employment(userid, "commission", message)
	else:
		print("error!!!!!")

def get_employment(userid):
	sql = text("select * from employment where userid = "+str(userid))
	result = db.engine.execute(sql)
	db.session.commit()
	x = []
	for row in result:
		x.append(row)
	print(x)
	y = []
	y.append(x[0].employee_name)
	y.append(x[0].employer_name)
	y.append(x[0].company_name)
	y.append(x[0].company_address)
	y.append(x[0].employee_address)
	y.append(x[0].job)
	y.append(x[0].duty)
	y.append(x[0].full)
	y.append(x[0].work_hour)
	y.append(x[0].salary)
	y.append(x[0].annual_leave)
	y.append(x[0].commence)
	y.append(x[0].ddl)
	y.append(x[0].remote)
	y.append(x[0].work_place)
	y.append(x[0].probationary)
	y.append(x[0].duration)
	y.append(x[0].advance)
	y.append(x[0].insurance)
	y.append(x[0].commission)

	return y

def modify_employment(userid, num, message):
	print(message)
	num = int(num)
	if num==1:
		update_employment(userid, "employee_name", message)
	elif num==2:
		update_employment(userid, "employer_name", message)
	elif num==3:
		update_employment(userid, "company_name", message)
	elif num==4:
		update_employment(userid, "company_address", message)
	elif num==5:
		update_employment(userid, "employee_address", message)
	elif num==6:
		update_employment(userid, "job", message)
	elif num==7:
		update_employment(userid, "duty", message)
	elif num==8:
		update_employment(userid, "full", message)
	elif num==9:
		update_employment(userid, "work_hour", message)
	elif num==10:
		update_employment(userid, "salary", message)
	elif num==11:
		update_employment(userid, "annual_leave", message)
	elif num==12:
		update_employment(userid, "commence", message)
	elif num==13:
		update_employment(userid, "ddl", message)
	elif num==14:
		update_employment(userid, "remote", message)
	elif num==15:
		update_employment(userid, "work_place", message)
	elif num==16:
		update_employment(userid, "probationary", message)
	elif num==17:
		update_employment(userid, "duration", message)
	elif num==18:
		update_employment(userid, "advance", message)
	elif num==19:
		update_employment(userid, "insurance", message)
	elif num==20:
		update_employment(userid, "commission", message)
	else:
		print("error!!!!!")









