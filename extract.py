from pymarc import MARCReader
import pickle
import glob
import unidecode
import re
import json

lookup = None
with open('auth.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    lookup = pickle.load(f)


not_found = {}
not_found_lookup = {}
all_keys = ''.join(lookup.keys())

def extract_check(field,lccn):
    name = ""
    for x in list(field):
        if x[0] in ['a','b','c','d','q','n']:
            name = name + ' ' + x[1]

    name_decoded = unidecode.unidecode(name.strip())
    name_stripped = re.sub(r'[^\w\s]','',name_decoded).strip()

    # try:
    if name_stripped in lookup:
        return lookup[name_stripped]
    else:
       # print('---------------->',name, '(', name_stripped, ')')
        if name_stripped in all_keys:
            if len(name_stripped.split()) > 2:
                for x in lookup:
                    if name_stripped in x:
                        return lookup[x]
                        break

    # except:
    #     continue
    if name not in not_found:
        not_found[name] = 0
        not_found_lookup[name] = []

    not_found[name]+=1
    not_found_lookup[name].append(lccn)


    return False



files = glob.glob("marc/*.utf8")
for file in files:


    
    matches = {}
    record_count = 0
    not_found = {}
    not_found_lookup = {}

    print('Doing ',file)
    with open(file, 'rb') as fh:
        reader = MARCReader(fh)
        try:

            for record in reader:
                record_count+=1
               
                lccn = None            
                for tv in record.get_fields('010'):
                    lccn = tv['a'].strip()

                formatString = None            
                for tv in record.get_fields('300'):
                    if 'a' in tv:
                        formatString = tv['a'].strip()

                url = []            
                for tv in record.get_fields('856'):
                    if 'u' in tv:
                        url.append(tv['u'].strip())

                title = record.title()
                lccn = {'lccn':lccn,'title':title, 'formatString':formatString, 'url':url}
                # 100 | 600 700

                for f in record.get_fields('100'):
                    name = extract_check(f,lccn)
                    if name:
                        if name['wiki'] not in matches:
                            matches[name['wiki']] = name
                        if 'lccn100' not in matches[name['wiki']]:
                            matches[name['wiki']]['lccn100'] = []

                        matches[name['wiki']]['lccn100'].append(lccn)
                    
                for f in record.get_fields('700'):
                    name = extract_check(f,lccn)
                    if name:
                        if name['wiki'] not in matches:
                            matches[name['wiki']] = name
                        if 'lccn700' not in matches[name['wiki']]:
                            matches[name['wiki']]['lccn700'] = []

                        matches[name['wiki']]['lccn700'].append(lccn)                
                    
                for f in record.get_fields('600'):
                    name = extract_check(f,lccn)
                    if name:
                        if name['wiki'] not in matches:
                            matches[name['wiki']] = name
                        if 'lccn600' not in matches[name['wiki']]:
                            matches[name['wiki']]['lccn600'] = []

                        matches[name['wiki']]['lccn600'].append(lccn)
                for f in record.get_fields('610'):
                    name = extract_check(f,lccn)
                    if name:
                        if name['wiki'] not in matches:
                            matches[name['wiki']] = name
                        if 'lccn610' not in matches[name['wiki']]:
                            matches[name['wiki']]['lccn610'] = []

                        matches[name['wiki']]['lccn610'].append(lccn)                

                for f in record.get_fields('611'):
                    name = extract_check(f,lccn)
                    if name:
                        if name['wiki'] not in matches:
                            matches[name['wiki']] = name
                        if 'lccn611' not in matches[name['wiki']]:
                            matches[name['wiki']]['lccn611'] = []

                        matches[name['wiki']]['lccn611'].append(lccn)
                                



                # for f in record.get_fields('600'):
                #     name = extract_check(f)
                    
                if record_count % 10000 == 0:
                    print(record_count)
                # if record_count > 10000:
                #     break
        except UnicodeDecodeError:
            print('UnicodeDecodeError')

    with open(file+'_results.json','w') as results_out:
        for x in matches:
            results_out.write(json.dumps(matches[x]) + '\n')

    sort = sorted(not_found, key=lambda i: not_found[i], reverse=True)
    with open(file+'_not_found.json','w', encoding="utf-8") as o:
        
        for x in sort:
            if not_found[x] > 1:
                o.write(json.dumps({'term':x,'count':not_found[x], 'lccn':not_found_lookup[x]}) + '\n')
            