import json
import base64


all_wikidata = json.load(open('wikidata_info_with_lccn.json'))
images = json.load(open('images.with_filename.json'))

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def extract_lccn(alist):

	extracted = []
	for lccn in alist:
		if len(lccn['url']) > 0:
			url = lccn['url'][0].replace(' ','')
			if url in images:
				title = lccn['title']
				page = images[url]['about'].replace('//','http://')
				extracted.append({'t':title,'l':page,'i':url})

	return extracted
			
def hydrate_base64(alist):
	# print(alist)
	# print(len(alist), '<--list')
	for x in alist:
		print(images[x['i']]['filename'])
		img = base64.b64encode(open("images/"+images[x['i']]['filename'], "rb").read()).decode('utf-8')
		x['i'] = img

	return alist

count = 0
contributor = []
subject = []
for x in all_wikidata:
	count+=1
	if 'contributor' not in all_wikidata[x]:
		all_wikidata[x]['contributor'] = []
	if 'subject' not in all_wikidata[x]:
		all_wikidata[x]['subject'] = []


	contributor = extract_lccn(all_wikidata[x]['contributor'])
	subject = extract_lccn( all_wikidata[x]['subject'])

	if len(subject+contributor) > 0:

		contributor_chunked = list(chunks(contributor,25))
		subject_chunked = list(chunks(subject,25))


		all_wikidata[x]['totalContributorPages'] = 0
		all_wikidata[x]['totalSubjectPages'] = 0
		all_wikidata[x]['contributor'] = None
		all_wikidata[x]['subject'] = None

		print(x)
		print(len(contributor_chunked))

		if len(contributor_chunked) > 1:
			all_wikidata[x]['contributor'] = contributor_chunked.pop(0)
			all_wikidata[x]['contributor'] = hydrate_base64(all_wikidata[x]['contributor'])
			for idx, c in enumerate(contributor_chunked):
				c = hydrate_base64(c)
				json.dump(c,open('qjson/'+x+'_contributor_page_'+str(idx+1)+'.json','w'))
				del c

			all_wikidata[x]['totalContributorPages'] = len(contributor_chunked)
		elif len(contributor_chunked) > 0:
			all_wikidata[x]['contributor'] = contributor_chunked.pop(0)
			all_wikidata[x]['contributor'] = hydrate_base64(all_wikidata[x]['contributor'])


		if len(subject_chunked) > 1:
			all_wikidata[x]['subject'] = subject_chunked.pop(0)
			all_wikidata[x]['subject'] = hydrate_base64(all_wikidata[x]['subject'])
			for idx, c in enumerate(subject_chunked):
				c = hydrate_base64(c)
				json.dump(c,open('qjson/'+x+'_subject_page_'+str(idx+1)+'.json','w'))
				del c

			all_wikidata[x]['totalSubjectPages'] = len(subject_chunked)
		elif len(subject_chunked) > 0:
			all_wikidata[x]['subject'] = subject_chunked.pop(0)
			all_wikidata[x]['subject'] = hydrate_base64(all_wikidata[x]['subject'])

		# print(all_wikidata[x])
		json.dump(all_wikidata[x],open('qjson/'+x+'.json','w'))
		del all_wikidata[x]['subject']
		del all_wikidata[x]['contributor'] 
		





		print(len(subject+contributor))
	if count % 100 == 0:
		print('counter:',count)
		# json.dump(done,open('images.json','w'), indent=2)


