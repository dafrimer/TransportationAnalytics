import unittest
import re, requests, json

import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from Pipeline.TransportationAuth import LimeBike

class limetest(unittest.TestCase):
    def testLimeRequest(self):
        lc = LimeBike()
        login_code = lc.get_login_code()

        self.assertIsNot(re.match('[0-9]{4}', login_code), None)
        
        openmaps_url = 'https://nominatim.openstreetmap.org/'
        address = 'Space Needle, Seattle, WA'

        data= {
            'format':'json',
            'addressdetails':1,
            'limit':'1',
            'q':address, 
            'format':'json',
        }
        h=requests.get(openmaps_url,params=data)  
        result_loc = json.loads(h.content)[0]
        bikes = lc.get_bikes(result_loc['lat'], result_loc['lon'])        

        self.assertGreater(len(bikes), 0)




if __name__ == '__main__':
    unittest.main()