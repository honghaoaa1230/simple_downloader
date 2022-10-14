import requests
import re


url = input("url:")
wbdata = str((requests.get(url).content),'utf-8')
pattern = re.compile('((https\:\/\/post\-phinf\.pstatic\.net)[-A-Za-z0-9+&@#/%?=~_|!:,.;]+(type\=[a-z]+[0-9]+))')

links = []
for x in pattern.findall(wbdata):
    links.append(x[0].split('?')[0])

# for x in links:
#     print(x)
print(len(links))

def get_link():
    return links

#url regex
# (https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]