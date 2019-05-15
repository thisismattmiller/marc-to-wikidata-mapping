import requests
import json
import glob
import re
from bs4 import BeautifulSoup
import base64
import hashlib
import os



def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def build_all_desc():

	all_desc = []
	for file in glob.glob("wikidata/*"):

		with open(file) as fin:
			s = fin.read()
			data = json.loads(json.loads(s))

			for e in data['entities']:
				if 'en' in data['entities'][e]['descriptions']:
					all_desc.append(data['entities'][e]['descriptions']['en']['value'])

	json.dump(all_desc,open('all_desc.json','w'),indent=2)


def build_all_desc_keys():

	all_descriptions = json.load(open('all_desc.json'))
	hits = []
	pcount = {}

	for idx, s in enumerate(all_descriptions):
		org_s = re.sub(r'[^\w\s]','',s.lower()).strip()
		s = org_s.split(' ')
	    

		all_chunks = []
		for r in range(6,0,-1):
			if len(s) >= r:
				for c in list(chunks(s, r)):
					if 'and' not in c and 'of' not in c and 'the' not in c:
						all_chunks.append(c)

		for ss in all_descriptions:
			ss = re.sub(r'[^\w\s]','',ss.lower()).strip()

			if ss == org_s:
				continue

			for a_chunk in all_chunks:
				words = " ".join(a_chunk)
				if len(words) > 3:

					if words in ss:
						if words not in pcount:
							pcount[words] = 0
						pcount[words]+=1

						if pcount[words]>700:
							if words not in hits:
								hits.append(words)

		print(len(hits),idx)
		if idx % 100:
			json.dump(sorted(hits, key=len,reverse=True), open('all_desc_keys.json','w'),indent=2)

	json.dump(sorted(hits, key=len,reverse=True), open('all_desc_keys.json','w'),indent=2)

def build_property_usage():
	plookup = {}
	pcount = {}


	properties = "https://query.wikidata.org/sparql?query=SELECT%20%3Fproperty%20%3FpropertyLabel%20WHERE%20%7B%0A%20%20%20%20%3Fproperty%20a%20wikibase%3AProperty%20.%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%0A%20%20%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20.%0A%20%20%20%7D%0A%20%7D%0A%0A&format=json"
	r = requests.get(properties)
	r= r.json()
	for p in r['results']['bindings']:
		plookup[p['property']['value'].split('/')[-1]] = p['propertyLabel']['value']


	filecount=0
	for file in glob.glob("wikidata/*"):

		with open(file) as fin:
			filecount+=1
			s = fin.read()
			data = json.loads(json.loads(s))

			for e in data['entities']:
				for p in data['entities'][e]['claims']:
					if p not in pcount:
						pcount[p] = 0

					pcount[p]+=1


		print(filecount)
	
	sorted_by_value = sorted(pcount.items(), key=lambda kv: kv[1],reverse=True)

	with open('property_usage.txt','w', encoding="utf-8") as out:
		for x in sorted_by_value:
			out.write(plookup[x[0]] + ',' + x[0] + ',' + str(x[1]) + '\n')

def build_all_labels():
	filecount=0
	all_labels =[]
	for file in glob.glob("wikidata/*"):

		with open(file) as fin:
			filecount+=1
			s = fin.read()
			data = json.loads(json.loads(s))

			for e in data['entities']:
				if 'en' in data['entities'][e]['labels']:
					all_labels.append(data['entities'][e]['labels']['en']['value'])

		print(filecount)
	json.dump(all_labels,open('all_labels.json','w'),indent=2)	

# build_all_desc()
# build_all_desc_keys()
# build_property_usage()
build_all_labels()
