import json
import requests
import os

qids = []

with open('done/Visual.Materials.2014.part01.utf8_results.json') as f:

	for line in f:

		

		if 'hdl.loc.gov/loc.pnp' in line:

			data = json.loads(line)
			
			for key in data.keys():

				# print(key)
				if 'lccn' in key:							
					for x in data[key]:
						if len(x['url']) > 0:
							for url in x['url']:
								if 'hdl.loc.gov/loc.pnp' in url:

									if data['wiki'] not in qids:
										qids.append(data['wiki'])
										# print(url)


# print(len(qids))
# if thre is some probs
# qids.append('Q11465393')
# qids.append('Q11465393')
# qids.append('Q11515406')
# qids.append('Q11553406')
# qids.append('Q11621081')
# qids.append('Q23776845')
# qids.append('Q23787572')
# qids.append('Q461314')
# qids.append('Q55964863')
# qids.append('Q9375607')
redownload = False

for idx, q in enumerate(qids):

	if os.path.exists('wikidata/'+q) == False or redownload == True:
		r = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+q+'&languages=en&format=json')
		#try:
		print(q,str(idx),'/',len(qids))
		j = json.dump(r.text,open('wikidata/'+q,'w'),indent=2)
		#except:
		#print('error on ',q)
	else:
		print('skipping',q)