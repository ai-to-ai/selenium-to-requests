import requests

import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

print("[Log]: Scrapping App Started")

username = "energyair1@gmail.com"
password = "ub6tfiqasFCHeuWLZX88"
registarationChannel = "desktop"
lang = "de"
brand = "energy"
switchChanel = "zuerich"

s = requests.Session()
params = {
	"state": "pSbVZzy37eGg6vs5IMioMcR3nD4cJF1W",
	"nonce": "/profile",
	"client_id": "JWT9GBjMcaJ7dn8FCzZ7SVESpgYj98nq",
	"response_type": "token id_token",
	"redirect_uri": "https://energy.ch/auth/callback",
	"scope": "openid email",
	"audience": "https://api.onelog.ch/profile/v1"
}

print("[Log]: Go to login.onelog.ch")
r = s.get("https://login.onelog.ch/authorize", params = params)
r_1 = s.get(r.url)
r_2 = s.get(r_1.url)



parsed_url = urlparse(r_2.url)
interaction = parse_qs(parsed_url.query)['interaction'][0]

payload = {
	"email":username,
	"password":password,
	"registrationChannel":registarationChannel,
	"lang":lang,
	"brand":brand
	}
header = {"Content-Type": 'application/json', "pragma": 'no-cache', "cache-control": 'no-store', "X-Trace-Interaction-Id": interaction}

print("[Log]: Go to api.onelog.ch")

r_3 = s.get("https://api.onelog.ch/api/v2/logincasegames/"+brand+"/default", headers = header)

r_4 = s.get("https://api.onelog.ch/api/v2/notifications?enabled=true")


print("[Log]: Go to id.onelog.ch")

r_5 = s.get("https://id.onelog.ch/native/emails/"+username+"?brand="+brand, headers = header)

r_6 = s.post("https://id.onelog.ch/native/login", json = payload,headers = header)



response_content = json.loads(r_6.content)
ticket = response_content["ticket"]
isLinked = response_content["isLinked"]

payload = {
	"ticket": ticket,
	"isLinked": isLinked,
	"connection": "native",
	"registrationChannel": registarationChannel,
	"lang": lang,
	"webAuthnSupport": "false"
}

print("[Log]: Go to login.onelog.ch/interaction")

r_7 = s.post("https://login.onelog.ch/interaction/" + interaction, json = payload, allow_redirects=True)

parsed_url = urlparse(r_7.url.replace("#","?"))
access_token = parse_qs(parsed_url.query)['access_token'][0]
expires_in = parse_qs(parsed_url.query)['expires_in'][0]
token_type = parse_qs(parsed_url.query)['token_type'][0]

print("[Log]: Get access_token")


r_8 = s.post(r_7.url)

data = {"authorization": token_type + " " + access_token}

cookies = { "access_token" : access_token}

print("[Log]: Redirect to energy.ch")

r_9 = s.get("https://energy.ch/profile", headers = data, cookies = cookies)

print("[Log]: Get user info from onelog.ch")

r_10 = s.get("https://login.onelog.ch/userinfo", headers = data)

response_content = json.loads(r_10.content)
sub = response_content["sub"]
email_verified = response_content["email_verified"]
email = response_content["email"]

r_11 = s.get("https://api.onelog.ch/api/v2/users/" + sub + "?brand="+ brand, headers = data)

r_12 = s.get("https://energy.ch/api/quiz/question")

r_13 = s.post("https://energy.ch/api/switch-channel", data = switchChanel)

r_14 = s.get("https://energy.ch/api/authorize?redirect_page=%2Fschlaumeier", headers = data)

print("[Log]: Schlaumeier page saving...")
try: 
	with open('Schlaumeier.html', 'w', encoding='utf-8') as file:
	    file.write(r_14.content.decode('utf-8'))
	file.close()
except error:
	print(error)
print("[Log]: Schlaumeier page saved")
	

print("=========User Info=========")
print("[Log]: "+r_11.content.decode('utf-8'))
print("===========================")

print("[Log]: Scrapping App Finished.")


# Total 130 lines of code with Requests.
