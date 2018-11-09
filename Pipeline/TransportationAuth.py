

import urllib3
import urllib
import requests
import json
import configparser
import re
import datetime, time 
from twilio.rest import Client



main_cfg = configparser.ConfigParser()
main_cfg.read_file(open('./TransportationAnalytics/config.cfg'))
secret_path = main_cfg.get('SECRETS','tokens')


class LimeBike():
  def __init__(self):
    self.secret_path = main_cfg.get('SECRETS','tokens')
    self.phone = main_cfg.get('PHONE','number')

  def set_phone(self, newphonenum):
    self.phone = str(newphonenum)

  def get_login_code(self):
    
    url = 'https://web-production.lime.bike/api/rider/v1/login?phone={phone}'.format(phone=self.phone)
    r = requests.get(url)
    time.sleep(2)

    cfg = configparser.ConfigParser()
    cfg.read_file(open(secret_path))
    client = Client(cfg.get('TWILIO','accountsid'), cfg.get('TWILIO','auth'))
    messages = client.messages.list(
                              date_sent_after=datetime.date.today(),
                          )
    return re.match('^[0-9]*',messages[0].body)[0]

  def reauthenticate(self, login_code=None):
    if not login_code:
      login_code = self.get_login_code()
    r = requests.post('https://web-production.lime.bike/api/rider/v1/login'
                , headers={'content-type': 'application/json'}
                , data = json.dumps({"login_code": login_code, "phone": self.phone})
                 )

    try:
      assert int(r.status_code) == 200
      cookie = r.cookies['_limebike-web_session']
      token = json.loads(r.content.decode('utf-8'))['token']
      #TODO: Can't keep this storage token

      json.dump({
      "cookie": cookie,
      "token" : token
      },open('/tmp/limeauth.json','w'))

      return token, cookie
    
    except AssertionError:
      print(r.status_code)
      print(r.content)

    except:
      print(r.status_code)
      print(r.content)
      return None


    

    
  def get_bikes(self, latitude, longitude):
    
    #try with the original authentication
    try:
      j = json.load(open('/tmp/limeauth.json'))
      cookie  = j['cookie']
      token   = j['token']

      limeurl = 'https://web-production.lime.bike/api/rider/v1/views/main?' \
            'map_center_latitude={lat}&map_center_longitude={lon}&user_latitude={lat}&user_longitude={lon}'.format(
              lat=latitude, lon=longitude)
      

    except (AssertionError,FileNotFoundError):
      
      token, cookie = self.reauthenticate()      
      limeurl = 'https://web-production.lime.bike/api/rider/v1/views/main?' \
            'map_center_latitude={lat}&map_center_longitude={lon}&user_latitude={lat}&user_longitude={lon}'.format(
              lat=latitude, lon=longitude)
    r = requests.get(url=limeurl
                      , headers={'authorization': 'Bearer ' + token}
                      , cookies = {'_limebike-web_session':cookie})
    lime_json = json.loads(r.content.decode('utf-8'))
    nearby_bikes = lime_json['data']['attributes']['nearby_locked_bikes']
    print(r)




#################
# LIME
################
"""
#curl --request GET \
#  --url 'https://web-production.lime.bike/api/rider/v1/login?phone=%2B33612345678'


url = 'https://web-production.lime.bike/api/rider/v1/login?phone=+12537859561'
#headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.get(url)

login_code = 857314


#curl --request POST \
#  --cookie-jar - \
#  --url 'https://web-production.lime.bike/api/rider/v1/login' \
#  --header 'Content-Type: application/json' \
#  --data '{"login_code": "857314", "phone": "+12066507212"}'

r = requests.post('https://web-production.lime.bike/api/rider/v1/login'
                , headers={'content-type': 'application/json'}
                , data = json.dumps({"login_code": login_code, "phone": "2066507212"})
                 )
cookie = r.cookies['_limebike-web_session']
rcookie = r.cookies
token = json.loads(r.content['token'])


#curl --request GET \
#  --url 'https://web-production.lime.bike/api/rider/v1/views/main?map_center_latitude=38.907192&map_center_longitude=-77.036871&user_latitude=38.907192&user_longitude=-77.036871' \
#  --header 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
#  --cookie '_limebike-web_session=[cookie]'


### TESTING PURPOSES #############
openmaps_url = 'https://nominatim.openstreetmap.org/'
address = '98103'

data= {
    'format':'json',
    'addressdetails':1,
    'limit':'1',
    'q':address, 
    'format':'json',
}
h=requests.get(openmaps_url,params=data)
result_loc = json.loads(h.content)[0]
latitude=47.69538
longitude=-122.35554

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3Rva2VuIjoiVTc3VEhCM1JFUzM2QiIsImxvZ2luX2NvdW50Ijo3fQ.sylcnbKdXBGmoR8K7UYtvW3KL1qSTJEaoK4ztWIpRuY"
val = 'eTlVaHpmMUZFQjVaNkQ3a0ZQZWQ5K2svSzdjbDZoSVpvYldERjcyU3lPVU9ubWxneWczaThadUZNOXhJa1piWWd1WWNaUS9lMkFQbDFKSDlJc2dUV3dDNHoySHNoYjZNV3ZhWkNnbXU1ako4V3VCdWVnY1dNMzlYTmZYZXc5TlNpVWVwdEdaenVESEJVVmMyQUw2SUIwaDFEWUVpbFd4aHhmMlRqWGJXOTFGMzZrUnNQRVNGSUNXUkUvRk9taTlzd3JqcEFteHpYeXl0eXM3Q0lrVkxIcy8wVkkzN2QwNFlRdHluM04xYndpeDFha0J2bnRXdGxNd0VibjBpdEgzMGVyUUNnZVRGcHJKUDFESlN6WDE3Mzl5dXdHZGtpbTRuZXVCS0c2VTFDTFV4RTZtTzdyaE9qOEZQRUdGM3dyN2N3Q2QzZ2cxZ2hZOGJkVjVIbzliZjdnPT0tLUU2T05jS2Zvck9BMkRpY3loeE1vQmc9PQ%3D%3D--4eaeb22728a9eb9c1131ea86ebadc81073f18b42'
#################
"""


