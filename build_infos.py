import requests
import json
import glob
import re
from bs4 import BeautifulSoup
import base64
import hashlib
import os

labels = {}
def label_service(q):

	if q in labels:
		return labels[q]

	label='unknown'
	data = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids='+q+'&languages=en&format=json').json()
	for e in data['entities']:
		if 'en' in data['entities'][e]['labels']:
			label = data['entities'][e]['labels']['en']['value']


	labels[q] = label
	return labels[q]


def build_wikidata_info():

	filecount=0
	all_descriptions = json.load(open('all_desc_keys.json'))
	all_out = {}
	for file in glob.glob("wikidata/*"):

		with open(file) as fin:
			filecount+=1
			s = fin.read()
			data = json.loads(json.loads(s))

			qid = None
			p21 = None
			birth = None
			occ = []		
			country = None
			place_of_birth = None
			place_of_death = None
			languages = []
			education = []
			awards = []
			image = None
			my_desc = []
			full_desc = None
			label = None

			for e in data['entities']:
				qid = e

				if 'en' in data['entities'][e]['labels']:
					label = data['entities'][e]['labels']['en']['value']

				if 'en' in data['entities'][e]['descriptions']:
					desc_og = data['entities'][e]['descriptions']['en']['value']
					full_desc = desc_og
					desc = re.sub(r'[^\w\s]','',desc_og.lower()).strip()
					for d in all_descriptions:
						if d in desc:

							if d == 'america' and 'american' in my_desc:
								continue

							my_desc.append(d)
							desc = desc.replace(d.title(),'')
					


				for p in data['entities'][e]['claims']:


					if p == 'P569':
						
						birth = re.findall('[\-+][0-9]{3,}\-[0-9]{2}-[0-9]{2}',json.dumps(data['entities'][e]['claims'][p][0]))
						if len(birth) > 0:
							birth = int(birth[0][0:5])
							birth = birth - (birth%10)				

							
					if p == 'P19':					
						if 'datavalue' in data['entities'][e]['claims'][p][0]['mainsnak']:
							place_of_birth = label_service(data['entities'][e]['claims'][p][0]['mainsnak']['datavalue']['value']['id'])
					if p == 'P20':					
						if 'datavalue' in data['entities'][e]['claims'][p][0]['mainsnak']:
							place_of_death = label_service(data['entities'][e]['claims'][p][0]['mainsnak']['datavalue']['value']['id'])

					if p == 'P21':					
						if 'datavalue' in data['entities'][e]['claims'][p][0]['mainsnak']:
							p21 = label_service(data['entities'][e]['claims'][p][0]['mainsnak']['datavalue']['value']['id'])
					if p == 'P106':
						for s in data['entities'][e]['claims'][p]:						
							if 'datavalue' in s['mainsnak']:
								occ.append(label_service(s['mainsnak']['datavalue']['value']['id']))

					if p == 'P1412':
						for s in data['entities'][e]['claims'][p]:						
							if 'datavalue' in s['mainsnak']:
								languages.append(label_service(s['mainsnak']['datavalue']['value']['id']))

					if p == 'P69':
						for s in data['entities'][e]['claims'][p]:						
							if 'datavalue' in s['mainsnak']:
								education.append(label_service(s['mainsnak']['datavalue']['value']['id']))


					if p == 'P166':
						for s in data['entities'][e]['claims'][p]:						
							if 'datavalue' in s['mainsnak']:
								awards.append(label_service(s['mainsnak']['datavalue']['value']['id']))
																				
					if p == 'P27':
						if 'datavalue' in data['entities'][e]['claims'][p][0]['mainsnak']:
							country = label_service(data['entities'][e]['claims'][p][0]['mainsnak']['datavalue']['value']['id'])
					if p == 'P18':
						if 'datavalue' in data['entities'][e]['claims'][p][0]['mainsnak']:
							image = data['entities'][e]['claims'][p][0]['mainsnak']['datavalue']['value']


				all_out[qid] ={'label': label,'qid': qid, 'p21': p21, 'birth': birth, 'birthplace': place_of_birth, 'deathplace': place_of_death, 'languages': languages, 'occ': occ, 'country': country, 'image': image, 'desc':my_desc, 'education': education, 'awards':awards, 'full_desc':full_desc}

		print(filecount)
		if filecount % 100 == 0:
			json.dump(all_out,open('wikidata_info.json','w'),indent=2)
	json.dump(all_out,open('wikidata_info.json','w'),indent=2)




def build_wikidata_info_with_lccns():
	all_wikidata = json.load(open('wikidata_info.json'))
	with open('done/Visual.Materials.2014.part01.utf8_results.json') as f:
		for line in f:
			if 'hdl.loc.gov/loc.pnp' in line:
				data = json.loads(line)

				added_urls = []
				for key in data.keys():
					if 'lccn' in key:		
						

						for x in data[key]:
							if len(x['url']) > 0:
								
								for url in x['url']:
									if 'hdl.loc.gov/loc.pnp' in url:

										if url not in added_urls:

											if 'contributor' not in all_wikidata[data['wiki']]:
												all_wikidata[data['wiki']]['contributor'] = []

											if 'subject' not in all_wikidata[data['wiki']]:
												all_wikidata[data['wiki']]['subject'] = []

											if 'all_added_urls' not in all_wikidata[data['wiki']]:
												all_wikidata[data['wiki']]['all_added_urls'] = []											

											x_copy = {**x}
											x_copy['url'] = [url]

											if data['wiki'] == 'Q317436':
												print(url)
												print(all_wikidata[data['wiki']]['all_added_urls'])
												print("~~~~~~~~~~~~~~~~~~")

											if url not in all_wikidata[data['wiki']]['all_added_urls']:

												all_wikidata[data['wiki']]['all_added_urls'].append(url)

												if '100' in key:
													all_wikidata[data['wiki']]['contributor'].append(x_copy)
												if '700' in key:
													all_wikidata[data['wiki']]['contributor'].append(x_copy)
												if '600' in key:
													all_wikidata[data['wiki']]['subject'].append(x_copy)
												if '610' in key:
													all_wikidata[data['wiki']]['subject'].append(x_copy)
												if '611' in key:
													all_wikidata[data['wiki']]['subject'].append(x_copy)



										# print(all_wikidata[data['wiki']])
	json.dump(all_wikidata,open('wikidata_info_with_lccn.json','w'),indent=2)



# build_wikidata_info()
build_wikidata_info_with_lccns()