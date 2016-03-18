import pystache
import json
import sys
import os.path
import os

with open('langs.json', 'r') as f:
    langs_list = [l for l in reversed(json.loads(f.read()))]
    langs_mapper = {lang['locale'].replace('-', '_'): lang['crowdin_code'] for lang in langs_list}

def get_lang(lang):
    return [l for l in langs_list if l['crowdin_code'] == lang][0]

langs_args = sorted(sys.argv[1].split(',') + ['en_US'])
used_langs = [get_lang(langs_mapper[lang]) for lang in langs_args]

#get list of current deployed releases including 'master'
def listdirs(folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

# get list of versions
vers_list = (listdirs("deploy/"))
list.sort(vers_list, reverse=True)
#remove unwanted dirs from list as we don't need them
vers_list.remove("master")
vers_list.remove(".git")
vers_list.remove("_static")
# result: verslist = ['2.1.0','3.0.0','master']

newlist = []
# step 1: create a dictionary out of the list for every list item
# step 2: parse all dictionaries into a list
for i in vers_list:
    create_dicts = {'apiversion': i}
    newlist.append(create_dicts)
# result: newlist = [{'apiversion': '3.0.0'},{'apiversion': '2.1.0'},{'apiversion': 'master'}]

# write to file
with open('etc/home.html', 'r') as f:
    tpl = f.read()

with open('dist/temp.html', 'w') as f:
    f.write(pystache.render('{{={| |}=}} ' + tpl, dict(langs=used_langs)))

with open('dist/temp.html', 'r') as f:
    tpl = f.read()

with open('dist/index.html', 'w') as f:
    f.write(pystache.render('{{={[ ]}=}} ' + tpl, dict(vers=newlist)))
