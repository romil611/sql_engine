#!/bin/python
import os
import sys
import string
import csv

data = {}
def parse_data ():
    temp = []
    metadata = open('metadata.txt') 
    temp = metadata.readlines()
    content = []
    for i in temp:
    	a = i.strip()
    	if(a != '<end_table>'):
    		content.append(a)
    del content[0]
    content = '\n'.join(content).split('<begin_table>')
    
    content2 = []
    for i in content:
    	content2.append(i.split())
    
    for i in content2:
        data[i[0]] = i[1:]

def init ():
    parse_data()
    for table in data:
        t = list(data[table])
        data[table]={}
        i=0
        for col in t:
            inp = []
            for r in csv.reader(open(table+'.csv'),delimiter=','): inp.append(r[i])
            data[table][col] = list(inp)
            i+=1

def query_preprocessing (query):
    q = query
    q = q.replace (', ',',').replace(' , ',',').replace(' ,',',')
    q = q.replace(' = ','=')
    q = q.replace('= ','=')
    q = q.replace(' =','=')
    q = q.replace(' > ','>')
    q = q.replace('> ','>')
    q = q.replace(' >','>')
    q = q.replace(' < ','<')
    q = q.replace('< ','<')
    q = q.replace(' <','<')
    q = q.replace(' AND ','&').replace(' OR ','|')
    q = q.replace(' and ','&').replace(' or ','|')
    return q

def output (distinct, c, tables, where=''):
    # number of tables that can be given rioght now is 1
    # if len(tables) > 1: raise Exception('Invalid Query: Join tables not yet supported.')
    cols = []
    com = []
    if c is '*': 
    	#cols = [i for i in data[tables[0]]]
    	for table in tables:
    		if table in data:
    			for i in data[table]:
    				cols.append([table,i,0])
    		else:
    			raise Exception('Invalid Query: Invalid table given.')
    else: 
    	com = c.split(',')
        com2 = list(com)
    	for table in tables:
    		for col in com:
    			cul = col.split('.')
    			if len(cul) > 1:
    				if cul[0] == 'max':
    					num = 1
    				elif cul[0] == 'min':
    					num = 2
    				elif cul[0] == 'avg':
    					num = 3
    				elif cul[0] == 'distinct':
    					num = 4
    				elif cul[0] == 'sum':
                        num = 5
    				else:
    					raise Exception('Invalid Query: unknown function given')
    			    coli = cul[1]
    			else:
    				num = 0
    			    coli = cul[0]
    			if coli in data[table]:
    				cols.append([table,coli,num])
    				com2.remove(coli)
        if len(com2):
        	raise Exception('Invalid Query: columns not given properly')
    cols.sort(key = lambda x:x[0])
    where = where.replace('>','_>_').replace('<','_<_').replace('|','_|_').replace('&','_&_').replace('=','_=_')
    where = where.split('_')
    if len(where) != 3 or len(where) !=7:
        raise Exception('Invalid Query: where condition not given properly')
    if (where[1] not in ['=','<','>']) :
        raise Exception('Invalid Query: where condition not given properly')
    where[0] = str(where[0]).split('.')
    where[2] = str(where[2]).split('.')
    if len(where[0])>1:
        tbl = where[0][0]
        clm = where[0][1]
        if tbl not in data.keys():
            raise Exception('Invalid Query: where condition not given properly')

        if clm not in data[tbl].keys():
            raise Exception('Invalid Query: where condition not given properly')
            
        clm1 = data[tbl][clm]
    else:
        for tbl in tables:
            if tbl not in data.keys():
                raise Exception('Invalid Query: where condition not given properly')

            if where[0][0] not in data[tbl].keys():
                raise Exception('Invalid Query: where condition not given properly')
            clm1 = data[tbl][where[0][0]]  
    if len(where[2])>1:
        tbl = where[2][0]
        clm = where[2][1]
        if tbl not in data.keys():
            raise Exception('Invalid Query: where condition not given properly')

        if clm not in data[tbl].keys():
            raise Exception('Invalid Query: where condition not given properly')
        clm2 = data[tbl][clm]
    else:
        if type(clm2) != int:
            for tbl in tables:
            if tbl not in data.keys():
                raise Exception('Invalid Query: where condition not given properly')

            if where[2][0] not in data[tbl].keys():
                raise Exception('Invalid Query: where condition not given properly')
                clm2 = data[tbl][where[2][0]]  
        else:
            clm2 = where[2][0]
       
    if len(where) == 7:
        if where[3] not in ['&','|']:
            raise Exception('Invalid Query: where condition not given properly')
        if (where[1] not in ['=','<','>']) or (where[5] not in ['=','>','<'] ):
            raise Exception('Invalid Query: where condition not given properly')
        where[4] = str(where[4]).split('.')
        where[6] = str(where[6]).split('.')
        if len(where[4])>1:
            tbl = where[4][0]
            clm = where[4][1]
            if tbl not in data.keys():
                raise Exception('Invalid Query: where condition not given properly')
            elif clm not in data[tbl].keys():
                raise Exception('Invalid Query: where condition not given properly')
            else:
                clm3 = data[tbl][clm]
        else:
            for tbl in tables:
                if tbl not in data.keys():
                    raise Exception('Invalid Query: where condition not given properly')
                elif where[4][0] not in data[tbl].keys():
                    raise Exception('Invalid Query: where condition not given properly')
                else:
                    clm3 = data[tbl][where[4][0]]  
        if len(where[6])>1:
            tbl = where[6][0]
            clm = where[6][1]
            if tbl not in data.keys():
                raise Exception('Invalid Query: where condition not given properly')
            elif clm not in data[tbl].keys():
                raise Exception('Invalid Query: where condition not given properly')
            else:
                clm4 = data[tbl][clm]
        else:
            if type(where[6][0]) != int:
                for tbl in tables:
                    if tbl not in data.keys():
                        raise Exception('Invalid Query: where condition not given properly')
                    elif where[6][0] not in data[tbl].keys():
                        raise Exception('Invalid Query: where condition not given properly')
                    else:
                        clm4 = data[tbl][where[6][0]]  
            else:
                 clm4 = where[6][0]
    

    for i in cols:
        if i[2] == 0:
            i.append(list(data[i[0]][i[1]]))
        elif i[2] == 1:
            temp = list(data[i[0]][i[1]])
            i.append([max(temp)])
        elif i[2] == 2:
            temp = list(data[i[0]][i[1]])
            i.append([min(temp)])
        elif i[2] == 3:
            temp = reduce(lambda x, y: int(x) + int(y), data[i[0]][i[1]]) / len(data[i[0]][i[1]])
            i.append([temp])
        elif i[2] == 4:
            temp = list(set(data[i[0]][i[1]]))
            i.append(temp)
        elif i[2] == 5:
            temp = reduce(lambda x, y: int(x) + int(y), data[i[0]][i[1]])
            i.append([temp])

    mins = {}
    for i in cols:
        if i[0] not in mins.keys(): mins[i[0]] = len(i[3])
        else: mins[i[0]] = min (mins[i[0]], len(i[3]))
    for i in cols:
        t = list (i[3][0:mins[i[0]]])
        i[3] = t
        
    print cols
    
    # number of elements in a single column
#   n = len(data[tables[0]][cols[0]])
#   
#   op = []
#   for i in xrange(n):
#       a = []
#       for j in cols:
#   		if(j[2]==0)	
#           	a.append(data[j[0]][j[1]][i])
#           #else if (j[2] == 1)
#           #	find max
#       op.append(a)
#   for i in op:
#       s='  '.join(i)
#       print s

def process (query):

    distinct = False

    q = query_preprocessing (query)
    init()
    q = q.split(' ')
    #print q
    if len(q) < 4 or len(q) > 7: raise Exception('Invalid Query: Check select statement')
    if q[0].lower() != 'select': raise Exception('Invalid Query: Check select statement')
    del q[0]
    #if q[0].lower() in ['distinct','max','min','avg']:
    #    distinct = True
    #    del q[0]
    cols = str (q[0])
    del q[0]
    #print q
    #print
    if q[0].lower() != 'from': raise Exception('Invalid Query: Check from expression')
    del q[0]
    tables = q[0].split(',')
    del q[0]
    if len(q) > 0 and q[0].lower() != 'where': raise Exception('Invalid Query: check where expression')
    elif len(q) == 0:
        output (distinct, cols, tables)
        exit (0)
    del q[0]
    if len(q) != 1: raise Exception('Invalid Query: Check where expression')
    output (distinct, cols, tables, q[0])
    #return 0
