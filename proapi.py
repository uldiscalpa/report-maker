from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import json
import time

class ProApi:
    BASE_URL = 'https://pro.kurbads.lv/api/'
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://pro.kurbads.lv/#/login")
        elem_username = self.driver.find_element_by_name("username")
        elem_username.clear()
        elem_username.send_keys('uldis.calpa@kurbads.lv')
        elem_password = self.driver.find_element_by_name("password")
        elem_password.clear()
        elem_password.send_keys('Kurbads2019!')
        elem_password.send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)
        time.sleep(.2)
    
    def _get_json_from_web_driver(self):
        """convert chrome web driver response to json. Return python dict object"""
        content = self.driver.page_source
        content = self.driver.find_element_by_tag_name('pre').text
        parsed_json = json.loads(content)
        return parsed_json
    
    def _url_builder(self, path=None, params=None):
        """create url for api request. Return url string"""
        if params:
            params_encoded = urllib.parse.urlencode(params)
            params_encoded = params_encoded.replace('%3D', '=')
        else:
            params_encoded = ''
        full_url =  self.BASE_URL + path + params_encoded
        return full_url
    
    def _close_web_browser(self):
        self.driver.close()

    def get_pro_route(self, route=None):
        """get pro.kurbads.lv response searching by route id. Return list"""
        path = 'routes/search/findAll?'
        params = {
                'search=code=': "'" + route + "'",
        }
        
        url  = self._url_builder(path=path, params=params)
        self.driver.get(url)
        data = self._get_json_from_web_driver()
        route_list = data['_embedded']['routes']
        
        return [route_in_list for route_in_list in route_list if route_in_list['code']==route]
        
    def get_pro_route_statistic(self, pro_route_id=None):
        path = 'routeCarStatistic/search/findAll?'
        params={
            'search=route=': "'" + 'https://pro.kurbads.lv/api/routes/'+ pro_route_id + "'",
        }
        url = self._url_builder(path=path, params=params)
        print(url)
        self.driver.get(url)
        data = self._get_json_from_web_driver()
        data = data['_embedded']['routeCarStatistics']
        return data
        
    def get_pro_route_cars(self, pro_route_id=None):
        path = 'routeMonitor/' + pro_route_id + '/routeCars'
        params=None
        url = self._url_builder(path=path, params=params)
        self.driver.get(url)
        data = self._get_json_from_web_driver()
        return data['_embedded']['routeCars']


if __name__ == "__main__":
    pass