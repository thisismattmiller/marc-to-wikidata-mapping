import requests
import re
import json

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


r=requests.get("https://query.wikidata.org/sparql?query=%23Cats%0ASELECT%20%3Fitem%20%3Fo%20%0AWHERE%20%0A%7B%0A%20%20%3Fitem%20wdt%3AP244%20%3Fo.%0A%7D", headers={"Accept":"application/json"})

lookup = {}
all_wiki_ids = []

j = r.json()
for x in j['results']['bindings']:
	lcId = re.sub('\W+', '', x['o']['value'])
	qid = x['item']['value'].replace('http://www.wikidata.org/entity/','')
	all_wiki_ids.append(qid)
	lookup[qid] = {'lc':lcId}



all_chunks = list(chunks(all_wiki_ids,125))

urlTemplate = "https://query.wikidata.org/sparql?query=%23Cats%0ASELECT%20%3Fitem%20%3FitemLabel%20%0AWHERE%20%0A%7B%0A%0A%20%20VALUES%20%3Fitem%20%7B<REPLACE>%7D%0A%20%20%0A%20%20%3Fitem%20wdt%3AP244%20%3Fo.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%2Cen%22.%20%7D%0A%7D"


for idx, c in enumerate(all_chunks):

	ids = 'wd%3A' + "%20wd%3A".join(c)
	url = urlTemplate.replace('<REPLACE>',ids)

	r=requests.get(url, headers={"Accept":"application/json"})
	j = r.json()
	for x in j['results']['bindings']:
	
		qid = x['item']['value'].replace('http://www.wikidata.org/entity/','')
		label = None
		if 'itemLabel' in x:
			if 'value' in x['itemLabel']:
				label = x['itemLabel']['value']

		lookup[qid]['label'] = label
	
	print(f'{idx}/{len(all_chunks)}')
	# print(j)

	if idx % 1000 == 0:
		json.dump(lookup,open('wikidata_with_lccns_with_labels.json','w'),indent=2)


json.dump(lookup,open('wikidata_with_lccns_with_labels.json','w'),indent=2)