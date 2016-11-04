from AnonBrowser import *

anon = AnonBrowser(proxies=[], user_agents=[('User-agent', 'superSecretBrowser')])
for i in range(1, 5):
    anon.anonymize()
    print('Fetching page')
    response = anon.open('http://jkdmartialscience.com')
    for c in anon.cookie_jar:
        print(c)
