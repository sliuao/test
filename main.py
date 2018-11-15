import user
#import chatbot
import conversation
import pdf_divorce
import pdf_employment

"""
when complete the python files, remember to generate the requirements.txt
pipreqs /Users/liushuyue/Desktop/FYP-chatbot --force
"""


if __name__ == "__main__":
    #for every new user, insert one line in DB and create a new class
    test1 = user.USER(1,'1234','mary',0,0)
    answer, goal = conversation.sequense(test1)

	if goal == 1:
		pdf_divorce.generate_pdf_divorce(answer)
		answer = conversation.modify_divorce(test1, answer)
	else:
		pdf_employment.generate_pdf_employment(answer)
		answer = conversation.modify_employment(test1, answer)


	if goal == 1:
		pdf_divorce.generate_pdf_divorce(answer)
	else:
		pdf_employment.generate_pdf_employment(answer)

	response = raw_input("Do you need more help? (Y/N)")

	while response.find('Y')!=-1 or response.find('y')!=-1:
		answer, goal = conversation.sequense(test1)

		if goal == 1:
			pdf_divorce.generate_pdf_divorce(answer)
			answer = conversation.modify_divorce(test1, answer)
		else:
			pdf_employment.generate_pdf_employment(answer)
			answer = conversation.modify_employment(test1, answer)

		reponse = raw_input("Do you need more help? (Y/N)")

	print("Bye, hope to see you again.")