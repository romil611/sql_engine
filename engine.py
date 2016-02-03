import sys
import re
import csv
from collections import defaultdict
#input
query = sys.argv[1:]

select_cases = ['Select', 'select', 'SELECT']
from_cases = ['FROM', 'From', 'from']
where_cases = ['WHERE', 'where', 'Where']
distinct_cases = ['DISTINCT', 'distinct', 'Distinct']
#print query

operators = ['<', '=', '>', '<>']
query_split = query[0].split(' ')

#print query_split


def query_case1(query_split):
  flag = 0
  target = open('metadata.txt')
  target_split = target.read().splitlines()
  index = target_split.index(query_split[3])
  output = ""
  columns = []
  index = index + 1
  while target_split[index] != '<end_table>':
    if target_split[index+1] == '<end_table>':
      output += query_split[3] + "." +target_split[index]
    else:
      output += query_split[3] + "." +target_split[index] + ","
    columns.append(target_split[index])
    index = index + 1
  print output
  filename = query_split[3] + ".csv"
  fileopend = open(filename)
  print fileopend.read()


def get_column_index(column_name,query_split):

	table_name = query_split
	flag = 0
	target = open('metadata.txt')
	target_split = target.read().splitlines()
	index = target_split.index(table_name)
	columns = []
	index = index + 1
	k = 0
	try:
		while target_split[index] != column_name and target_split[index] != "<end_table>":
			k = k + 1
			index = index + 1
		return k
	except IndexError:
		print "The enterned column name doesn't exist"
		return -1
 
def query_case2_max(query_split):
	a = query_split[1]
	column_name = a[a.index("(") + 1:a.rindex(")")]
	f = open(query_split[3] + ".csv", 'rt')
	reader = csv.reader(f)
	row_list = []
	for row in reader:
		row_list.append(row)
	#print row_list
	temp = get_column_index(column_name,query_split[3])
	if temp == -1:
	  return
	i = 1
	row_list = [ map(int,x) for x in row_list ]
	maximum = row_list[0][temp]
	length = len(row_list)
	while i < length:
		if maximum < row_list[i][temp]:
			maximum = row_list[i][temp]
		i = i + 1
	print query_split[3] + "." + column_name
	print maximum

def query_case2_min(query_split):
	a = query_split[1]
	column_name = a[a.index("(") + 1:a.rindex(")")]
	f = open(query_split[3] + ".csv", 'rt')
	reader = csv.reader(f)
	row_list = []
	for row in reader:
		row_list.append(row)
	#print row_list
	temp = get_column_index(column_name,query_split[3])
	if temp == -1:
		return
	i = 1
	row_list = [ map(int,x) for x in row_list ]
	minimum = row_list[0][temp]
	length = len(row_list)
	while i < length:
		if minimum > row_list[i][temp]:
			minimum = row_list[i][temp]
		i = i + 1
	print query_split[3] + "." + column_name
	print minimum

def query_case2_sum(query_split):
	a = query_split[1]
	column_name = a[a.index("(") + 1:a.rindex(")")]
	f = open(query_split[3] + ".csv", 'rt')
	reader = csv.reader(f)
	row_list = []
	for row in reader:
		row_list.append(row)
	#print row_list
	temp = get_column_index(column_name,query_split[3])
	if temp == -1:
		return
	i = 0
	row_list = [ map(int,x) for x in row_list ]
	sum_up = 0
	length = len(row_list)
	while i < length:
		sum_up = sum_up + row_list[i][temp]
		i = i + 1
	print query_split[3] + "." + column_name
	print sum_up
	return float(sum_up/length)

def query_case2_average(query_split):
	a = query_split[1]
	column_name = a[a.index("(") + 1:a.rindex(")")]
	f = open(query_split[3] + ".csv", 'rt')
	reader = csv.reader(f)
	row_list = []
	for row in reader:
		row_list.append(row)
	#print row_list
	temp = get_column_index(column_name,query_split[3])
	if temp == -1:
		return
	i = 0
	row_list = [ map(int,x) for x in row_list ]
	sum_up = 0
	length = len(row_list)
	while i < length:
		sum_up = sum_up + row_list[i][temp]
		i = i + 1
	print query_split[3] + "." + column_name
	average = sum_up/float(length)
	print average


def query_case3(query_split):
	tables = query_split[3].split(',')
	target = open('metadata.txt')
	target_split = target.read().splitlines()
	output = ""
	columns = defaultdict(list)
	for table in tables:
		try:
			index = target_split.index(table)
			index = index + 1
			while target_split[index] != '<end_table>':
				if target_split[index+1] == '<end_table>':
					output += table + '.' + target_split[index]
				elif target_split[index+1] != '<end_table>':
					output += table + '.' + target_split[index] + ','
				columns[table].append(target_split[index])
				index = index + 1
		except ValueError:
			print "No such table exists"
			return
	#print output
	target.close()
	#print columns
	output_columns = query_split[1].split(',')
	list1 = []
	final_output = []
	for x in output_columns:
		temp_values_list = columns.values()
		#print temp_values_list
		try:
			for temp in temp_values_list:
				if x in temp:
					final_output.append(columns.keys()[columns.values().index(temp)] + "." + x)
					list2 = []
					f = open(columns.keys()[columns.values().index(temp)] + '.csv', 'rt')
					reader = csv.reader(f)
					row_list = []
					for row in reader:
						row_list.append(row)
					row_list = [ map(int,y) for y in row_list ]
					#print columns.keys()[columns.values().index(temp)]
					#print get_column_index(x, 'table1')
					index = get_column_index(x,columns.keys()[columns.values().index(temp)])
					#print index
					
					i = 0
					length = len(row_list)
					while i < length:
						list2.append(row_list[i][index])
						i = i + 1
					f.close()
					list1.append(list2)
		except IndexError:
			print "Column doesn't exist!"
			return
	#print list1
	#print final_output
	output = ""
	for temp in final_output:
		if temp != final_output[len(final_output)-1]:
			output = output + temp + ','
		else:
			output = output + temp
	print output

	i = 0
	try:
		while i < len(list1[0]):
			row_output = ""
			j = 0
			while j < len(list1):
				if j != len(list1)-1:
					row_output = row_output + str(list1[j][i]) + ","
				else:
					row_output = row_output + str(list1[j][i])
				j = j + 1
			print row_output
			i = i + 1
	except IndexError:
		print "column doesn't exists"
		return


def query_case4(query_split):
	tables = query_split[4].split(',')
	target = open('metadata.txt')
	target_split = target.read().splitlines()
	output = ""
	columns = defaultdict(list)
	for table in tables:
		index = target_split.index(table)
		index = index + 1
		while target_split[index] != '<end_table>':
			if target_split[index+1] == '<end_table>':
				output += table + '.' + target_split[index]
			elif target_split[index+1] != '<end_table>':
				output += table + '.' + target_split[index] + ','
			columns[table].append(target_split[index])
			index = index + 1
	#print output
	target.close()
	#print columns
	output_columns = query_split[2].split(',')
	list1 = []
	final_output = []
	for x in output_columns:
		temp_values_list = columns.values()
		#print temp_values_list
		for temp in temp_values_list:
			if x in temp:
				final_output.append(columns.keys()[columns.values().index(temp)] + "." + x)
				list2 = []
				f = open(columns.keys()[columns.values().index(temp)] + '.csv', 'rt')
				reader = csv.reader(f)
				row_list = []
				for row in reader:
					row_list.append(row)
				row_list = [ map(int,y) for y in row_list ]
				#print columns.keys()[columns.values().index(temp)]
				#print get_column_index(x, 'table1')
				index = get_column_index(x,columns.keys()[columns.values().index(temp)])
				#print index
				i = 0
				length = len(row_list)
				while i < length:
					list2.append(row_list[i][index])
					i = i + 1
				f.close()
				list1.append(list2)
	#print list1
	#print final_output
	output = ""
	for temp in final_output:
		if temp != final_output[len(final_output)-1]:
			output = output + temp + ','
		else:
			output = output + temp
	print output

	unique_data = [list(k) for k in set(tuple(k) for k in list1)]
	#print unique_data

	i = 0
	while i < len(unique_data[0]):
		row_output = ""
		j = 0
		while j < len(unique_data):
			if j != len(unique_data)-1:
				row_output = row_output + str(unique_data[j][i]) + ","
			else:
				row_output = row_output + str(unique_data[j][i])
			j = j + 1
		
		i = i + 1
	print row_output

def query_case5(query_split):
	tables = query_split[3].split(',')
	target = open('metadata.txt')
	target_split = target.read().splitlines()
	output = ""
	columns = defaultdict(list)
	for table in tables:
		index = target_split.index(table)
		index = index + 1
		while target_split[index] != '<end_table>':
			if target_split[index+1] == '<end_table>':
				output += table + '.' + target_split[index]
			elif target_split[index+1] != '<end_table>':
				output += table + '.' + target_split[index] + ','
			columns[table].append(target_split[index])
			index = index + 1
	#print output
	target.close()
	#print columns
	output_columns = query_split[1].split(',')
	list1 = []
	final_output = []
	for x in output_columns:
		temp_values_list = columns.values()
		#print temp_values_list
		for temp in temp_values_list:
			if x in temp:
				final_output.append(columns.keys()[columns.values().index(temp)] + "." + x)
				list2 = []
				f = open(columns.keys()[columns.values().index(temp)] + '.csv', 'rt')
				reader = csv.reader(f)
				row_list = []
				for row in reader:
					row_list.append(row)
				row_list = [ map(int,y) for y in row_list ]
				#print columns.keys()[columns.values().index(temp)]
				#print get_column_index(x, 'table1')
				index = get_column_index(x,columns.keys()[columns.values().index(temp)])
				#print index
				i = 0
				length = len(row_list)
				while i < length:
					list2.append(row_list[i][index])
					i = i + 1
				f.close()
				list1.append(list2)
	#print list1
	#print final_output
	flag1 = 0
	flag2 = 1
	if len(query_split) == 12:
		pass

	if len(query_split) == 8:
		operator = query_split[7]
		left_operand = query_split[6]
		right_operand = query_split[8]
	output = ""
	for temp in final_output:
		if temp != final_output[len(final_output)-1]:
			output = output + temp + ','
		else:
			output = output + temp
	print output

	i = 0
	while i < len(list1[0]):
		row_output = ""
		j = 0
		while j < len(list1):
			if j != len(list1)-1:
				row_output = row_output + str(list1[j][i]) + ","
			else:
				row_output = row_output + str(list1[j][i])
			j = j + 1
		print row_output
		i = i + 1


def parser(query):
    if query_split[0] not in select_cases:
        print query_split[0] + ": Unknown query!"

    else:
        if query_split[1] is '*' :
          if query_split[2] in from_cases:
            if len(query_split) == 4:
              query_case1(query_split)
          else:
          	print "Invalid Format!"
          	print "Correct format: 'select/SELECT/Select * from TABLE_NAME' "

        elif query_split[1] in distinct_cases:
        	query_case4(query_split)

        elif query_split[1].startswith("max"):
					query_case2_max(query_split)

        elif query_split[1].startswith("min"):
          query_case2_min(query_split)

        elif query_split[1].startswith("avg"):
          query_case2_average(query_split)

        elif query_split[1].startswith("sum"):
          query_case2_sum(query_split)

        elif len(query_split[3].split(',')) >= 1 and len(query_split) <= 4:
        	query_case3(query_split)

        elif len(query_split) >4 and query_split[4] in where_cases:
        	query_case5(query_split)

        


parser(query)
