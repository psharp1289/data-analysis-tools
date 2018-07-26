#	Created by Paul Sharp 7-8-2014. Updated 7-2-2015.
#
#
#	Extract as many questionnaires from a large dataset and score them with a few user inputs.
# 	The option is given to score subscales, also.
#
#
#	This script also finds invalid data and deletes those files from the new extraced
#   and scored CSV file it creates (for the questionnaire of interest). It records
#	these invalid subject IDs in a CSV file (intuitively saved) that has the subject
#	IDs, the location of the invalid data for that subject, the original data file and
#   the questionnaire of interest.
#
#
#
import csv
import numpy as np
import pandas as pd
import os
import Data_Analysis as da
import sys

output_path='/Users/paulsharp/Documents/DATA_ANALYSIS_SCRIPTS'

#DEFINE CONSTANTS HERE AND PUT THEM IN CAPS.

print 'Have your data file open to consult for the following questions.\nThis program will extract the data correctly if you give the correct answers.\nThere are some fail-safes, but take your time and be meticulous!'

while True:
	print 'This is your current directory: {}'.format(os.path.abspath(os.curdir))
	change_path = raw_input('Do you need to change the path to get to the raw data? (y/n): \n')
	if change_path == 'y':
		ch_path = raw_input('\nType the rest of the path (to go up one directory, type two periods ("..") and hit enter): \n')
		os.chdir(ch_path)
		continue
	elif change_path == 'n':
		break
	else:
		print '\nError! Only accepts y or n as answers.'

#input CSV file and check if it exists. will only work if it exists.
while True:
	csv_file = raw_input('\nWhat CSV file would you like to extract questionnaire data from? \n')
	if os.path.isfile(csv_file) == False:
		print '\nFailed to find CSV file. Make sure you typed it in correctly, and added ''.csv'' at the end of the file name.'
	else:
		break

#input type of data (online or not online) and check if input is correct
while True:
	type_data = raw_input('\nIs this data from an online questionnaire. Hint: if yes, there should be just 0''s and 1''s? (enter y/n):  \n')
	if type_data == 'y' or type_data == 'n':
		break
	else:
		print '\nNeed to type literally ''y'' or ''n'' . Will raise error if you type anything else.'
col_headers = da.column_headers(csv_file)
subject_nums= da.get_subject_nums(csv_file,col_headers)
print 'NUMBER OF SUBS:{}\n'.format(subject_nums)
while True:
	delete_invalid_subjs = raw_input('\nWould you like to Delete invalid subjects as way to handle bad data? (enter y/n):  \n')
	if delete_invalid_subjs == 'y' or delete_invalid_subjs == 'n':
		break
	else:
		print '\nNeed to type literally ''y'' or ''n'' . Will raise error if you type anything else.'
#option to do as many questionnaires as you want
while True:
	how_many_questionnaires = int(raw_input('\n\nHow many questionnaires would you like to score? (type an integer)\n\n'))
	if type(how_many_questionnaires) == int:
		break
	else:
		print '\n NEED TO INPUT A NUMBER, THEN HIT ENTER TO MOVE ON ******** \n'


all_questionnaires=[]
acceptable_scores = np.arange(100000).tolist()+['0','1','2','3','4','5','6','7','8','9','true','false','JT'] #if output is strings or ints for original data
q_nums = 0
zero_mat_cols=[1]# zero_mat index for non-online dataset
ques_ind = 1 # zero_mat index for online dataset
q_info={} #dictionary of questionnaire info
subscale_queries=[]

#get questionnaire name and get the necessary reverse scoring, scoring rubric, and # of questions
for current_questionnaire_number in range(how_many_questionnaires):
	while True:
		print '\n\n **********\n\nTHIS IS FOR QUESTIONNAIRE NUMBER {}\n**********\n'.format(current_questionnaire_number+1)
		answer = raw_input('\nNotice which questionnaire you are on. If you''ve read this, type ''yes'' then hit return/enter to move on\n')
		if answer == 'yes':
			break
		else:
			print 'Need to type ''yes'' all lower case!!!'

	questionnaire,reverse_score_items, scoring_rubric, questions = da.get_questionnaire_info()
	all_questionnaires.append(questionnaire)
	q_info['questionnaire_{}_questions'.format(current_questionnaire_number+1)] = questions
	q_info['questionnaire_{}_name'.format(current_questionnaire_number+1)] = questionnaire
	q_info['questionnaire_{}_reverse_score_items'.format(current_questionnaire_number+1)] = reverse_score_items
	q_info['questionnaire_{}_scoring_rubric'.format(current_questionnaire_number+1)] = scoring_rubric



	row_num = subject_nums+1 # This adds a row for column headers
	invalid_subject_IDs = []
	#see if user wants a subscale
	while True:
		subscale_query = raw_input('\n\nWould you like subscales? (y/n) \n')
		if subscale_query == 'y' or subscale_query == 'n':
			break
		else:
			print '\n\nError! Can only enter ''y'' or ''n'' '

	if subscale_query == 'y':
		subscale_names,subscales = da.get_subscales(questionnaire)
		subscale_queries.append('y')
		q_info['questionnaire_{}_subscalenames'.format(current_questionnaire_number+1)]=subscale_names
		q_info['questionnaire_{}_subscale_dict'.format(current_questionnaire_number+1)]=subscales
	else:
		subscale_queries.append('n')

	col_num = questions+1

	#Matrix of zeros that will be a template for new CSV file of JUST questionnaire of interest scores
	if current_questionnaire_number==0:
		zero_mat = np.zeros((row_num,col_num), dtype=int)
		print '\nthis is the blank matrix template:'
		print 'size of matrix: {}'.format(zero_mat.shape)


	else:
		prev_cols=np.size(zero_mat,1)
		row_num_consistent=0 # 5 bad subjects are 5 bad rows NEED TO CHANGE FOR EACH SCRIPT
		temp_add_rows= np.zeros((row_num_consistent,prev_cols), dtype=int)
		zero_mat = np.concatenate((zero_mat,temp_add_rows), axis=0)
		new_zero_mat=np.zeros((row_num,col_num-1), dtype=int)
		print 'size of zero_mat is {}'.format(zero_mat.shape)
		print zero_mat
		print 'size of new_mat is {}'.format(new_zero_mat.shape)
		print new_zero_mat
		zero_mat = np.concatenate((zero_mat,new_zero_mat), axis=1)
	while True:
		try:
			column_start = raw_input('\n\nWhat column index (e.g. A, B, D, F -- Alphabetical column title in spreadsheet) does the data begin? \n')
			data_start = da.column_key(column_start)
			question_number = int(raw_input('What question number (type an integer!) does your questionnaire begin in the dataset?\n IF IT IS AN ONLINE QUESTIONNAIRE, IT ASSUMES THE COLUMN HEADERS ARE ''Q1, Q2''\n AND includes ALL questions in test set including SUBJECT ID q''s\n'))
			if type_data == 'y':
				df = pd.read_csv(csv_file)
				columns = df.columns
				index = 0
				for name in columns: #once column header has the question number, this gives the accurate index
					if 'Q{}:'.format(question_number) in name: #because q1 is SUBJECT ID
						index_start = index
						print 'index start = {}'.format(index_start)
						break
					index+=1
			else:
				index_start = (question_number-1) + data_start
			break
		except:
			print 'Error! Need to input a valid column index (e.g. 1 is A, 4 is D, etc.): \n'
	while True:
		try:
			subject_id = raw_input('\n\nWhat column index (e.g. A, B, D, F -- Alphabetical column title in spreadsheet) in the CSV file is the subject ID? \n')
			subject_id_index = da.column_key(subject_id)
			break
		except:
			print 'Error! Need to input a valid column header (e.g. 1 is A, 4 is D, etc.): \n'

	##iterates through the questionnaire questions, and places in new 'zero_mat' matrix the corresponding lichert value
	##for each question.
	if type_data == 'n':
		index_end = index_start + questions #this is actually the index of the last questionnaire question plus 1, because the for loop range function takes this input, e.g. range(1,4) ends on 3.
		print '\nThis is index start: {}'.format(index_start)
		print '\nThis is index end: {}'.format(index_end)
		with open(csv_file, 'rU') as f:
			r = csv.reader(f)
			lines = [line for line in r]
			zero_mat_row_index=1 #row number for new matrix
			if col_headers=='y':
				for row_data in range(1, subject_nums+1):
					zero_mat_col_index=zero_mat_cols[current_questionnaire_number]
					for col_data in range(index_start,index_end):
						lines[row_data][col_data]=int(lines[row_data][col_data])
						if lines[row_data][col_data] not in acceptable_scores:
							if delete_invalid_subjs == 'y':
								print 'Deleting subject number: {} from analysis'.format(lines[row_data][0]) #write log to exteranl text file
								invalid_subject_IDs.append(lines[row_data][subject_id_index])
								invalid_subject_IDs.append('Row:{} Col:{}'.format(row_data+1,col_data+1))
								zero_mat = np.delete(zero_mat,zero_mat_row_index,0) #deletes this row from new matrix. invalid data b/c of missing value.
								row_num -=1 #delete a row in variable that represents how many rows are in new matrix.
								zero_mat_row_index-=1
								break
							else:
								zero_mat[zero_mat_row_index,zero_mat_col_index] = 9
								zero_mat_col_index +=1
						else:
							zero_mat[zero_mat_row_index,zero_mat_col_index] = lines[row_data][col_data]
							zero_mat_col_index +=1
					zero_mat_row_index+=1
			else:
				for row_data in range(subject_nums):
					zero_mat_col_index=zero_mat_cols[current_questionnaire_number]
					for col_data in range(index_start,index_end):
						lines[row_data][col_data]=int(lines[row_data][col_data])
						if lines[row_data][col_data] not in acceptable_scores:
							if delete_invalid_subjs == 'y':
								print 'Deleting subject number: {} from analysis'.format(lines[row_data][0]) #write log to exteranl text file
								invalid_subject_IDs.append(lines[row_data][subject_id_index])
								invalid_subject_IDs.append('Row:{} Col:{}'.format(row_data+1,col_data+1))
								zero_mat = np.delete(zero_mat,zero_mat_row_index,0) #deletes this row from new matrix. invalid data b/c of missing value.
								row_num -=1 #delete a row in variable that represents how many rows are in new matrix.
								zero_mat_row_index-=1
								break
							else:
								zero_mat_col_index +=1
						else:
							zero_mat[zero_mat_row_index,zero_mat_col_index] = lines[row_data][col_data]
							zero_mat_col_index +=1
					zero_mat_row_index+=1

			print '\n DONE READING FILE\n'


	elif type_data == 'y':
		stop = int(raw_input('How many options are there to answer each question for the {}?\n'.format(questionnaire)))
		index_end = index_start + (questions * stop) # gives number of options for each question. E.g. on a lichert scale of 5, you have 5 options for each question. This is how online data is saved to CSV file (a column for each option)
		print '\nThis is index start: {}'.format(index_start)
		print '\nThis is index end: {}'.format(index_end)
		with open(csv_file, 'rU') as f:
			r = csv.reader(f)
			lines = [line for line in r]
			zero_mat_row_index =1
			for subject in range(1,subject_nums+1):
				if current_questionnaire_number==0:
					ques_ind=1
				else:
					ques_ind=q_nums+1
				score=1
				sub_count=subject-1
				for question_option in range(index_start,index_end):
					if lines[subject][question_option] == '1':
						zero_mat[zero_mat_row_index,ques_ind] = score
						#print '\nthe subject {}, question number {} = {}\n'.format(subject,ques_ind,zero_mat[zero_mat_row_index,ques_ind])
						ques_ind +=1
						sub_count+=1
						if score == stop:
							score = 1
						else:
							score+=1
					elif score < stop:
						score+=1
					else:
						if sub_count < subject:
							print 'Deleting subject number: {} from analysis'.format(lines[subject][subject_id_index]) #write log to exteranl text file
							invalid_subject_IDs.append(lines[subject][subject_id_index])
							invalid_subject_IDs.append('Row:{} Col:{}'.format(subject,question_option))
							zero_mat = np.delete(zero_mat,zero_mat_row_index,0) #deletes this row from new matrix. invalid data b/c of missing value.
							row_num -=1 #delete a row in variable that represents how many rows are in new matrix.
							zero_mat_row_index-=1
							score =1
							break
						else:
							score =1
				zero_mat_row_index+=1
	q_nums+=questions

	# zero_mat_col_index_dict = {'questionnaire_1':1}
	# zero_mat_cols.append(zero_mat_col_index)
	# zero_mat_col_index_dict['questionnaire_{}'.format(current_questionnaire_number+1)] = zero_mat_col_index
	# ques_ind+=1

data_set = raw_input('What data set is this from, so I know how to save the new CSV file of questionnaire scores? \n')
all_qs = '_'.join(all_questionnaires)
if subscale_query == 'n':
	scored_csv = 'scored_{}_{}.csv'.format(all_qs, data_set)
else:
	scored_csv = 'scored_{}_{}_subscales.csv'.format(all_qs, data_set)

#Save matrix containing the scored questionnaire data to new CSV file
os.chdir(output_path)
np.savetxt(scored_csv, zero_mat, delimiter=',')


#Open newly made scored csv file and create a new nested list called 'newlines' that
#will temporarily hold the final CSV file which will have the the subject numbers
#dates and correect column headers
update_qs=0
for current_questionnaire in range(how_many_questionnaires):
	with open(scored_csv, 'rb') as f:
		r = csv.reader(f)
		new_lines = [line for line in r]
		new_lines[0][0] = 'subject_id'
		#add question number headers
		if current_questionnaire_number==0:
			startcol=1
			endcol=startcol+q_info['questionnaire_{}_questions'.format(current_questionnaire+1)]
			qnum=1
		else:
			startcol=update_qs+1
			endcol=startcol+q_info['questionnaire_{}_questions'.format(current_questionnaire+1)]
			qnum=1
		for question in range(startcol,endcol):
			new_lines[0][question] = '{}_{}'.format(q_info['questionnaire_{}_name'.format(current_questionnaire+1)],qnum)
			qnum+=1
		print 'attaching headers for questions {}'.format(q_info['questionnaire_{}_name'.format(current_questionnaire+1)])
		#add subscales headers
		new_row = 1
		if col_headers == 'y':
			old_row = new_row
		else:
			old_row = new_row-1
		#add valid subject IDs
		for subject in range(subject_nums):
			if lines[old_row][subject_id_index] not in invalid_subject_IDs:
				new_lines[new_row][0] = lines[old_row][subject_id_index] #this is where the subject ID number is in original csv, column 3
				new_row+=1
			old_row+=1


		for subject in range(1,row_num):
			rs_num=1
			for data in range(startcol,endcol):
				new_lines[subject][data] = float(new_lines[subject][data])
				new_lines[subject][data] = int(new_lines[subject][data]) #converts strings of numbers into integer types
				if rs_num in q_info['questionnaire_{}_reverse_score_items'.format(current_questionnaire+1)]: #Iterates through to change the reverse score questions only.
					if new_lines[subject][data] in q_info['questionnaire_{}_scoring_rubric'.format(current_questionnaire+1)]:
						new_lines[subject][data] = q_info['questionnaire_{}_scoring_rubric'.format(current_questionnaire+1)][new_lines[subject][data]]
				rs_num+=1

		for subject in range(1,row_num): #sums up each row and appends it to a new column, TOTAL_SCORE.
			sum_row = 0
			for question in range(startcol,endcol):
				new_lines[subject][question]=int(new_lines[subject][question])
				if new_lines[subject][question] in acceptable_scores:
					sum_row += new_lines[subject][question]
				else:
					new_lines[subject][question] = 'NaN'
			new_lines[subject].append(sum_row)
		new_lines[0].append('TOTAL_SCORE_{}'.format(q_info['questionnaire_{}_name'.format(current_questionnaire+1)])) #creates a column header, TOTAL_SCORE



	#Overwrite scored Csv file with newlines which has column headers and subject info, reverse scored corrected data, and total score data.
	with open(scored_csv, 'w') as f:
		w = csv.writer(f)
		w.writerows(new_lines)

	if subscale_queries[current_questionnaire]=='y':
		with open(scored_csv, 'rU') as f:
			r = csv.reader(f)
			new_lines = [line for line in r]
			if isinstance(q_info['questionnaire_{}_subscale_dict'.format(current_questionnaire+1)],dict): #score all subscales
				nsubsc = 0
				mapping = {}
				for subsc in range(len(q_info['questionnaire_{}_subscalenames'.format(current_questionnaire+1)])):
					new_lines[0].append('{}_SCORE'.format(q_info['questionnaire_{}_subscalenames'.format(current_questionnaire+1)][nsubsc]))
					for question in q_info['questionnaire_{}_subscale_dict'.format(current_questionnaire+1)][q_info['questionnaire_{}_subscalenames'.format(current_questionnaire+1)][nsubsc]]:
						mapping['{}_{}'.format(q_info['questionnaire_{}_name'.format(current_questionnaire+1)],question)] = q_info['questionnaire_{}_subscalenames'.format(current_questionnaire+1)][nsubsc]
					nsubsc+=1
				df = pd.read_csv(scored_csv)
				by_column = df.groupby(mapping, axis=1)
				totals = by_column.sum()
				nsubsc = 0
				for subsc in range(len(q_info['questionnaire_{}_subscalenames'.format(current_questionnaire+1)])):
					op = 'totals.{}.values'.format(q_info['questionnaire_{}_subscalenames'.format(current_questionnaire+1)][nsubsc])
					vals = eval(op)
					for subject in range(1,row_num):
						new_lines[subject].append(vals[subject-1])
					nsubsc+=1



	if subscale_queries[current_questionnaire]=='y':
		with open(scored_csv, 'w') as f:
			w = csv.writer(f)
			w.writerows(new_lines)

	update_qs+=q_info['questionnaire_{}_questions'.format(current_questionnaire+1)]


os.chdir('..')
print 'Your new analysis file should not include these subject IDs who had invalid scores(with Row/Col locations):\n\n {}\n\n'.format(invalid_subject_IDs)

#updates file called 'Invalid_SubjectIDs_For_Data_Files.csv' with new invalid data.
if not invalid_subject_IDs:
	print 'Nothing to add to file holding invalid data.'
else:
	da.update_invalid_subjects_text(invalid_subject_IDs,questionnaire,csv_file)
