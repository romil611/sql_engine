q = set(data[tables[0]])
    	for i in tables[1:]:
    		q = q.union(data[i])
    	for col in cols:
    		if col not in q:
    			raise Exception('Invalid Query: Invalid column given.')	