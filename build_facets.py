import requests
import json
import glob
import re

import base64
import hashlib
import os

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def CountFrequency(my_list): 
  
    # Creating an empty dictionary  
    freq = {} 
    results = {}
    for item in my_list: 
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
  
    for key, value in freq.items(): 
        results[key] = value

    return results

# ------------------------------------------
import itertools

all_wikidata = json.load(open('wikidata_info_with_lccn_old.json'))
all_wikidata_data = {}
all_ids = []
all_keys = ['p21','birth','birthplace','deathplace','country','desc','occ','education','awards','languages']

combo_lookup = {}

counter = 0
for qid in all_wikidata:

	if qid != 'Q558104':
		continue

	print(qid)
	# if "Library of Congress Living Legend" not in all_wikidata[qid]['awards']:
	# 	continue

	print(len(all_ids))
	all_ids.append(qid)
	counter+=1
	all_terms = []

	base_set = []
	base_set_keys = []
	for k in all_keys:
		if isinstance(all_wikidata[qid][k],list) == False:
			if all_wikidata[qid][k] != None:
				base_set.append(json.dumps({k:all_wikidata[qid][k]}))
				base_set_keys.append(k)

	print(base_set)

	# for k in all_keys:
	# 	if isinstance(all_wikidata[qid][k],list):
	# 		for d in all_wikidata[qid][k]:
	# 			all_terms.append(json.dumps({k:d}))
	# 	else:
	# 		all_terms.append(json.dumps({k:all_wikidata[qid][k]}))


	# # take care of the non lists first
	# base_set = []
	# base_set_keys = []
	# for k in all_keys:
	# 	if isinstance(all_wikidata[qid][k],list) == False:
	# 		if all_wikidata[qid][k] != None:
	# 			base_set.append(json.dumps({k:all_wikidata[qid][k]}))
	# 			base_set_keys.append(k)

	# list_keys = []
	# for k in all_keys:
	# 	if k not in base_set_keys and all_wikidata[qid][k] != None:
	# 		list_keys.append(k)

	# all_base_lists = []
	# for lk in list_keys:

	# 	for pimary_list_key_term in all_wikidata[qid][lk]:



	# 		max_loops = 0
	# 		for max_loop_check_key in list_keys:

	# 			if lk != max_loop_check_key:					
	# 				if len(all_wikidata[qid][max_loop_check_key]) > max_loops:
	# 					max_loops = len(all_wikidata[qid][max_loop_check_key])



	# 		for n in range(0,max_loops):


	# 			base_set_copy = base_set.copy()
	# 			# add in the base primary term
	# 			base_set_copy.append(json.dumps({lk:pimary_list_key_term}))


	# 			for lk2 in list_keys:
	# 				if lk != lk2:
	# 					if len(all_wikidata[qid][lk2]) > n:
	# 						base_set_copy.append(json.dumps({lk2:all_wikidata[qid][lk2][n]}))



	# 			c = 0
	# 			for i in range(1,len(base_set_copy)):
	# 				for x in list(itertools.combinations(base_set_copy,i)):
	# 					skip = False
	# 					key = "~~".join(sorted(x))	
	# 					if key in combo_lookup:
	# 						continue		
	# 					for kk in all_keys:
	# 						if key.count(kk) > 1:
	# 							skip = True
	# 					if skip:
	# 						continue

	# 					c+=1
	# 					if key not in combo_lookup:					
	# 						combo_lookup[key] = [qid]
	# 					else:
	# 						if qid not in combo_lookup[key]:
	# 							combo_lookup[key].append(qid)

	# 			# print(base_set_copy)
	# 			# print(n,max_loops)
	# 			# print(len(combo_lookup))



			



	print(len(combo_lookup))

	# print(c)





combo_lookup['{"all":"all"}'] = all_ids


paths_created = {}
added_urls = {}
mapping = {}
for x in combo_lookup:
	counter+=1
	if counter % 1000 == 0:
		print(counter, counter/len(combo_lookup)*100)

	# if len(combo_lookup[x]) > 10:
		# print(x, len(combo_lookup[x]))


	url = ""
	exlude = {}
	keepFacets = {}
	names = {}
	namesSort = []
	idsSorted = []
	for s in x.split('~~'):
		s = json.loads(s)			
		key = list(s.keys())[0]
		value = s[key]
		exlude[key] = value

	for k in all_keys:
		if k in exlude:
			url = url + k + "=" + str(exlude[k]).lower().replace(' ','_').replace('"','_') + "&"

	url = url[0:-1]

	if url in added_urls:
		continue
	else:
		added_urls[url] = 1

	if 'all' in exlude:
		url = 'all'

	if url == '':
		continue






	for id in combo_lookup[x]:
		names[all_wikidata[id]['label']] = id
		namesSort.append(all_wikidata[id]['label'])
		for key in all_wikidata[id]:				
			if key in all_keys:					
				if key in exlude:
					pass
				else:


		# 			# print('keeping', key, all_wikidata_data[id][key], 'we got', exlude)
					if key not in keepFacets:
						keepFacets[key] = []

					if isinstance(all_wikidata[id][key], (list,)):
						# no empty lists
						if len(all_wikidata[id][key]) == 0:
							continue
						else:
							for f in all_wikidata[id][key]:
								keepFacets[key].append(f)									

					else:
						if all_wikidata[id][key] != None:
							keepFacets[key].append(all_wikidata[id][key])


	facet_data = {}
	for k in keepFacets:
		if k not in exlude:			
			# print(keepFacets[k])
			facet_data[k] = CountFrequency(keepFacets[k])

	# print(facet_data)

	namesSort = sorted(namesSort)
	for i in namesSort:
		idsSorted.append(names[i])

	all_idsSorted = []

	for achunk in chunks(idsSorted,25):
		all_idsSorted.append(achunk)

	# idsSorted = list()
	# print(idsSorted)


	md5 = hashlib.md5(url.encode('utf-8')).hexdigest()

	path = md5[0:1] + '/' + md5[0:2] + '/' + md5[0:3] + '/'

	if path not in paths_created:
		os.makedirs('facets/'+path, exist_ok=True)
		paths_created[path] = True

	json.dump({"count":len(namesSort),"url":url,"facets":facet_data,"pages":all_idsSorted,"pageCount":len(all_idsSorted)},open('facets/'+path+md5,'w'),indent=2)
	mapping[url] = path + md5
	# print("----")

json.dump(mapping,open('mapping.json','w'),indent=2)

