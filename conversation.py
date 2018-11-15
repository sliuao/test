import user
#import chatbot
import datetime
from fpdf import FPDF
import database
import nltk
from nltk.corpus import names

import pdf_employment
import pdf_divorce

import test
import webbrowser

from flask import send_file

response_all = ["Hi, what can I help you?\n",
			"Sorry, I can't understand what you want, please tell me what you want to do?\n",
			"here is the contract you want, please have a look. Do you want to modify something? (Y/N)\n",
			"Do you need more help?\n",
			"Bye, hope to see you again.\n"]

response_divorce = [
			"What's the name of mother?\n",
			"What's the name of father?\n",
			"What's the HKID of mother?\n",
			"What's the address of mother?\n",
			"What's the HKID of father?\n",
			"What's the address of father?\n",
			"What's mother's age?(please input a number)\n",
			"What's father's age?(please input a number)\n",
			"What's your marriage date?\n",
			"How many children do you have?(please input a number)\n",
			"What's your children's name?(split by ;)\n",
			"What date are your children born?(split by ;)\n",
			"Who will adopt the children?(input father or mother and split by ;)\n",
			"Who will pay the children maintenance?(father or mother)\n",
			"who will pay the spousal maintenance?(father or mother)\n",
			"How much will be the spousal maintenance per month?(input a number)\n",
			"How long will the spousal maintenance continue?(input a number whose unit is year)\n",
			"Please input the asset that will go to mother(split by ;)\n",
			"please input the asset that will go to father(split by ;)\n"
			]

response_employment = ["What's employee's name?(please input a name begin with capital letter)\n",
						"What's employer's name?(please input a name begin with capital letter)\n",
						"What's the company's name?(please input a name begin with capital letter)\n",
						"What's the registered office address of the company?\n",
						"What's the address of employee?\n",
						"What's the job title?\n",
						"What's the duty job?(split by ;)\n",
						"Is the job full-time or part-time?\n",
						"How many hours per week the employee required to work? (please input a number)",
						"What's the monthly salary?(by HKD)\n",
						"How many days of annual leave?\n",
						"On what date will the employment commence?\n",
						"What's the deadline of receive this letter?\n",
						"Will the employee be required to work from a specific location or be allowed to work remotely or online?\n",
						"What's the specific location that the employee will be expected to work?\n",
						"Is there a probationary period?(Y/N)\n",
						"What's the duration of the probationary period?(input a number whose unit is week)\n",
						"How much advance notice is required for either party to terminate the employment?(input a number whose unit is week)\n",
						"Will the employee be entitled to join the company's health insurance?(Y/N)\n",
						"Will the employee be paid commission?(Y/N)\n"
						]
employment = ["employee_name", "employer_name", "company_name", "company_address", "employee_address", "job", "duty","full-time or part-time"]

def determine_type(input):
	try:
		x = int(input)
		return 1
	except:
		return 0


def getresponse(goal,state):
	#get the response from response DB by using user state
	if goal == 1:
		#get from divorce DB
		response = response_divorce[state]
	else:
		#get from employment DB
		response = response_employment[state]
	return response


def determine_goal(user,goal):
	if goal.find("divorce")!=-1 or goal.find("marry")!=-1:
		user.update_user_data("goal", 1)
		return 1
	elif goal.find("employ")!=-1 or goal.find("labor")!=-1 or goal.find("labour")!=-1 or goal.find("hire")!=-1:
		user.update_user_data("goal", 2)
		return 2
	else:
		return 0

def collect_divorce(user):
	answer = []
	i = 0
	child = False;
	#get user state from user DB
	#according to user state, get response from response DB
	while i < len(response_divorce):
		#user.update_user_data...   add the answer to DB
		response = raw_input(response_divorce[i])
		if i==10 or i==11 or i==12 or i==17 or i==18:
			#add to DB
			answer.append(response.split(';'))
			user.update_user_data("state", i)
			i = i+1
			continue
		#add to DB
		answer.append(response)
		#update 
		user.update_user_data("state", i)
		if i==9:
			if response == '0':	
				i = 14
				continue
			else:
				child = True
				i = i+1
				continue
		i = i+1

	return answer

#for employment, 0->12, 14, 161718, 13->2 choice, 141718->y/n
def collect_employment(user):
	answer = []
	i = 0
	while i < len(response_employment):
		#user.update_user_data...   add the answer to DB
		response = raw_input(response_employment[i])
		if i==12:
			if response.find("remote")!=-1:
				i = i+2
				response = 0
				answer.append(0)
				answer.append(0)
				user.update_user_data("state", i)
				continue
			else:
				answer.append(1)
				i = i+1
				user.update_user_data("state", i)
				continue
		if i==14:
			if determine_yn(response)==0:
				response = 0
				i = i+2
				answer.append(0)
				answer.append(0)
				user.update_user_data("state", i)
				continue
			else:
				answer.append(1)
				i = i+1
				user.update_user_data("state", i)
				continue
		if i==17 or i==18:
			response = determine_yn(response)
		answer.append(response)
		i = i+1
		user.update_user_data("state", i)
	return answer


def determine_yn(answer):
	if answer.find("Y")!= -1 or answer.find("y") != -1:
		return 1
	else:
		return 0


# def sequense(user):
# 	goal = raw_input(response_all[0])
# 	x = determine_goal(user,goal)
# 	answer = []
# 	while x==0:
# 		goal = raw_input(response_all[1])
# 		x = determine_goal(user, goal)
# 	if x==1:
# 		answer = collect_divorce(user)
# 	elif x==2:
# 		answer = collect_employment(user)
# 	return answer,x


def modify_divorce(user, answer):
	modify = raw_input(response_all[2]);
	while modify.find('Y')!=-1 or modify.find('y')!=-1:
		x1 = raw_input("what do you want to modify? mother, father or children?\n")
		x2 = raw_input("what item do you want to modify? name, HKID, address or age?\n")
		x3 = raw_input('please just input the information that you want to replace the previous one.\n')
		if x1.find("mother")!=-1:
			if x2.find("name")!=-1:
				answer[0] = x3
			elif x2.find("HKID")!=-1:
				answer[2] = x3
			elif x2.find("address")!=-1:
				answer[3] = x3
			elif x2.find("age")!=-1:
				answer[6] = x3
			else:
				print('I cannot modify the things you want, please try again.\n')
		elif x1.find("father")!=-1:
			if x2.find("name")!=-1:
				answer[1] = x3
			elif x2.find("HKID")!=-1:
				answer[4] = x3
			elif x2.find("address")!=-1:
				answer[5] = x3
			elif x2.find("age")!=-1:
				answer[7] = x3
			else:
				print('I cannot modify the things you want, please try again.\n')
		elif x1.find("child")!=-1:
			if x2.find("name")!=-1:
				answer[9] = x3.split(";")
			else:
				print('I cannot modify the things you want, please try again.\n')
		else:
			print('I cannot modify the things you want, please try again.\n')

		modify = raw_input('Do you want to modify something else? (Y/N)\n');

	return answer


def modify_employment(user, answer):
	modify = raw_input(response_all[2]);
	while modify.find('Y')!=-1 or modify.find('y')!=-1:
		x1 = raw_input("What do you want to modify? About employee, employer, or others?\n")
		if x1.find("employee")!=-1:
			x2 = raw_input("What item do you want to modify? name, job, duty or address?\n")
			x3 = raw_input("please just input the information that you want to replace the previous one.\n")
			if x2.find("name")!=-1:
				answer[0] = x3
			elif x2.find("job")!=-1:
				answer[5] = x3
			elif x2.find("duty")!=-1:
				answer[6] = x3
			elif x2.find("address")!=-1:
				answer[4] = x3
			else:
				print('I cannot modify the things you want, please try again.\n')

		elif x1.find("employer")!=-1:
			x2 = raw_input("What item do you want to modify? name, company name, or address?\n")
			x3 = raw_input("please just input the information that you want to replace the previous one.\n")
			if x2.find("name")!=-1:
				answer[1] = x3
			elif x2.find("job")!=-1:
				answer[2] = x3
			elif x2.find("duty")!=-1:
				answer[3] = x3
			else:
				print('I cannot modify the things you want, please try again.\n')

		elif x1.find("other")!=-1:
			x2 = raw_input("What item do you want to modify? salary, leave days, commence date, or deadline?\n")
			x3 = raw_input("please just input the information that you want to replace the previous one.\n")
			if x2.find("salary")!=-1:
				answer[8] = x3
			elif x2.find("leave")!=-1:
				answer[9] = x3
			elif x2.find("commence")!=-1:
				answer[10] = x3
			elif x2.find("deadline")!=-1:
				answer[11] = x3
			else:
				print('I cannot modify the things you want, please try again.\n')

		else:
			print('I cannot modify the things you want, please try again.\n')

		modify = raw_input('Do you want to modify something else? (Y/N)\n');

	return answer

def sequence(userid, state ,message):
	    #######NLP using nltk test here!!!!
    if state==1 or state==2 or state==3:
        s1 = nltk.sent_tokenize(message)
        s2 = [nltk.word_tokenize(i) for i in s1]
        s3 = [nltk.pos_tag(sent) for sent in s2]

        s4 = []
        for i in range(len(s3[0])):
            if s3[0][i][1]=='NNP' and s3[0][i][0]!='Hi' and s3[0][i][0]!='Hello':
                s4.append(s3[0][i][0])

        if len(s4)==0:
            reply_message = "Please input a reasonable name!"
            return reply_message

        message = ''
        for i in range(len(s4)):
            if i!=0:
                message = message + ' ' +s4[i]
            else:
                message = s4[i]

    #full time or part time
    if state==8:
        if message.find("full")==-1 and message.find("part")==-1:
            reply_message = "Please input full-time or part-time!"
            return reply_message

    #number
    if state==10 or state==11 or state==17 or state==18:
        if determine_type(message)==0:
            reply_message = "Error input type! please input a number!"
            return reply_message
            
    if state <= 19:

        #part time have another question
        if state == 8:
            if message.find("full")!=-1:
                state += 1
                #write something to work hours into db to skip that question! connect db here
                database.update_employment(userid, "full", message)

        #specific have another question
        if state == 14:
            if message.find("remote")!=-1:
                state += 1
                #write sth, skip question! connect db here
                database.update_employment(userid, "remote", message)

        if state == 16:
            if message.find("n")!=-1 or message.find("N")!=-1:
                state += 1
                #write sth, skip question, connect db here
                database.update_employment(userid, "probationary", message)


        reply_message = response_employment[state]


    #modify part ! not finished yet!
    

    elif state == 21:
        if message.find("n")!=-1 or message.find("N")!=-1:
            reply_message = "Thanks! You have already finish your employment letter!"
            database.update_user(userid,"state","999")
            return jsonify({"status":"success","response":reply_message})
        else:
            reply_message = "What do you want to modify?(please input a number)\n"+"1. employee's name\n"+"2. employer's name\n" + "3. company name\n"+"4. company address\n"+"5. employee address\n"+"6. job\n"+"7. duty\n"+"8. full-time or part-time\n"+"9. work hour\n"+"10. salary\n"+"11. annual leave\n"+"12. commence date\n"+"13. deadline of accept the letter\n"+"14. remote or specific place\n"+"15. work place\n"+"16. probationary or not\n"+"17. duration of probationary\n"+"18. advance week of terminate employment\n"+"19. health insurance or not\n"+"20. commission or not"
            database.update_user(userid,"state","100")
            return reply_message

    if state==999:
        reply_message = "You have already finished the letter!"
        return reply_message
        
    elif state==100:
        if determine_type(message)==0:
            reply_message = "Error input type! please input a number!"
            return reply_message
        else:
            reply_message = "Please input the message which you want to replace the original one."
            print("message: " + message)
            database.update_user(userid,"modify",message)
            database.update_user(userid, "state", "200")
            return reply_message

    elif state==200:
        x = database.get_user(userid,"modify")
        print(x[0])
        database.modify_employment(userid,x[0],message)
        print("test here !!!state 200")
        reply_message = "Already modify? anything else?(y/n)"
        database.update_user(userid, "state", "22")
        return reply_message

    elif state == 22:
        if message.find("n")!=-1 or message.find("N")!=-1:
            reply_message = "Thanks! You have already finish your employment letter!"
            database.update_user(userid,"state","999")
            info = database.get_employment(userid)

            if info[13].find("remote")!=-1:
                info[13]=0
                info[14]=0
            else:
                info[13]=1

            if info[15].find('n')!=-1 or info[15].find("N")!=-1:
                info[15]=0
                info[16]=0
            else:
                info[15]=1

            if info[18].find('n')!=-1 or info[18].find("N")!=-1:
                info[18]=0
            else:
                info[18]=1

            if info[19].find('n')!=-1 or info[19].find("N")!=-1:
                info[19]=0
            else:
                info[19]=1


            pdf_employment.generate_pdf_employment(info)

            webbrowser.open_new_tab("http://ec2-18-223-100-211.us-east-2.compute.amazonaws.com/docs")
            
            return reply_message

        else:
            reply_message = "What do you want to modify?(please input a number)\n"+"1. employee's name\n"+"2. employer's name\n" + "3. company name\n"+"4. company address\n"+"5. employee address\n"+"6. job\n"+"7. duty\n"+"8. full-time or part-time\n"+"9. work hour\n"+"10. salary\n"+"11. annual leave\n"+"12. commence date\n"+"13. deadline of accept the letter\n"+"14. remote or specific place\n"+"15. work place\n"+"16. probationary or not\n"+"17. duration of probationary\n"+"18. advance week of terminate employment\n"+"19. health insurance or not\n"+"20. commission or not"
            database.update_user(userid,"state","100")
            return reply_message



    #connect to employment db! write info into it!
    database.update_employment_info(userid,state,message)


    print("state: "+str(state))

    #connect to user db and update user's state
    database.update_user(userid,"state",str(state+1))

    if state == 20:
        #connect to employment db ! get all the info and store them into an array!
        #postprocess some info here!
        info = database.get_employment(userid)
        
        if info[13].find("remote")!=-1:
            info[13]=0
            info[14]=0
        else:
            info[13]=1

        if info[15].find('n')!=-1 or info[15].find("N")!=-1:
            info[15]=0
            info[16]=0
        else:
            info[15]=1

        if info[18].find('n')!=-1 or info[18].find("N")!=-1:
            info[18]=0
        else:
            info[18]=1

        if info[19].find('n')!=-1 or info[19].find("N")!=-1:
            info[19]=0
        else:
            info[19]=1

        print(info)

        pdf_employment.generate_pdf_employment(info)
        
        reply_message = "Now the pdf file is downloaded, please have a look\n"+"Do you want to modify something?(y/n)"

        webbrowser.open_new_tab("http://ec2-18-223-100-211.us-east-2.compute.amazonaws.com/docs")

    return reply_message










