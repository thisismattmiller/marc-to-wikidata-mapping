import pickle
import requests
import json
import re
import unidecode
import json
import time

r=requests.get("https://query.wikidata.org/sparql?query=%23Cats%0ASELECT%20%3Fitem%20%3Fo%20%0AWHERE%20%0A%7B%0A%20%20%3Fitem%20wdt%3AP244%20%3Fo.%0A%7D", headers={"Accept":"application/json"})

wikiLCIds = {}
wikiLCIdsDel = {}
wikilookup = {}

j = r.json()
for x in j['results']['bindings']:
	wikidataId = re.sub('\W+', '', x['o']['value'])
	wikilookup[wikidataId] = x['item']['value'].replace('http://www.wikidata.org/entity/','')
	wikiLCIds[wikidataId] = 1
	wikiLCIdsDel[wikidataId] = 1

del j
del r

print(len(wikiLCIds))
count = 0
lookup = {}

files = ['authoritiessubjects.madsrdf.nt','authoritiesnames.nt.both']
#files = ['authoritativeLabel.nt','authoritiessubjects.madsrdf.nt']

for a_file in files:

	with open(a_file) as auth:

		for line in auth:

			if '<http://www.loc.gov/mads/rdf/v1#authoritativeLabel>' in line and '_:bnode' not in line:
				line = line.replace('<http://www.loc.gov/mads/rdf/v1#authoritativeLabel>','')
				line = line.split('>  "')

				uri = line[0]
				name = line[1]

				uri = uri.replace('<http://id.loc.gov/authorities/','')
				id = uri.split('/')[1]

				if id in wikiLCIds:

					if id in wikiLCIdsDel:
						del wikiLCIdsDel[id]

					count+=1

					name = '"'+name[0:name.rfind('"')]+'"'
					name = json.loads(name)						
					name = unidecode.unidecode(name)
					name_stripped = re.sub(r'[^\w\s]','',name)

					# print(name, name_stripped)
					if name_stripped not in lookup:
						lookup[name_stripped] = {'lc':[],'wiki':None, 'name':name}

					if uri not in lookup[name_stripped]['lc']:
						lookup[name_stripped]['lc'].append(uri)
						lookup[name_stripped]['wiki'] = wikilookup[id]


					if len(lookup[name_stripped])>10:
						print(name_stripped,lookup[name_stripped])

					if count % 1000 == 0:
						print(count, len(wikiLCIdsDel))

						if count % 10000 == 0:
							with open('auth.pickle', 'wb') as f:
							    # Pickle the 'data' dictionary using the highest protocol available.
							    pickle.dump(lookup, f, pickle.HIGHEST_PROTOCOL)
							print('pickle done')














with open('auth.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(lookup, f, pickle.HIGHEST_PROTOCOL)

json.dump(wikiLCIdsDel,open('notfound.json','w'),indent=2)