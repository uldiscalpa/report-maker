from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from settings import URL_PROTOCOL, URL_DOMAIN, URL_LOGIN_PATH, URL_SEARCH_PATH, USER_LOGIN, PASSWORD
import urllib
import json
import time

class ProApi:
    BASE_URL = URL_PROTOCOL + URL_DOMAIN + "api/"
    
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        url_login = URL_PROTOCOL + URL_DOMAIN + URL_LOGIN_PATH
        self.driver.get(url_login)
        elem_username = self.driver.find_element_by_name("username")
        elem_username.clear()
        elem_username.send_keys(USER_LOGIN)
        elem_password = self.driver.find_element_by_name("password")
        elem_password.clear()
        elem_password.send_keys(PASSWORD)
        elem_password.send_keys(Keys.TAB, Keys.TAB, Keys.ENTER)
        time.sleep(.7)
    
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
    
    def close_web_browser(self):
        self.driver.close()

    def get_pro_route(self, route_id=None):
        """get pro.kurbads.lv response searching by route id example="R9999". Return list"""
        entity = 'routes'
        path = entity + URL_SEARCH_PATH
        params = {
                'search=code=': "'" + route_id + "'",
        }
        url  = self._url_builder(path=path, params=params)
        print(url)
        self.driver.get(url)
        data = self._get_json_from_web_driver()
        route_list = data['_embedded']['routes']
        
        return [route for route in route_list if route['code']==route_id]
        
    def get_pro_route_statistic(self, pro_route_id=None):
        """"return pro routeCars statistic, searching by pro.kurbads id example  12352"""
        entity = 'routeCarStatistic'
        path = entity + URL_SEARCH_PATH
        # linkā tiek pie query parametriem tiek padots vēl katra route atsevišķs links
        params={
            'search=route=': "'" + self.BASE_URL + 'routes/' + pro_route_id + "'",
        }
        url = self._url_builder(path=path, params=params)
        print(url)
        self.driver.get(url)
        data = self._get_json_from_web_driver()
        data = data['_embedded']['routeCarStatistics']
        return data
        
    def get_pro_route_cars(self, pro_route_id=None):
        """get api response which is used in por route monitor"""
        path = 'routeMonitor/' + pro_route_id + '/routeCars'
        params=None
        url = self._url_builder(path=path, params=params)
        self.driver.get(url)
        data = self._get_json_from_web_driver()
        return data['_embedded']['routeCars']

import csv
if __name__ == "__main__":
    # route_list = []
    # with open("test_route_list.csv") as f:
    #     filereader = csv.reader(f)
    #     for row in filereader:
    #         route_list.append({
    #             'route_id': row[0],
    #         })
           
    # proapi_obj = ProApi()
    # response_route_list = []
    # for route in route_list[:2]:
    #     response = proapi_obj.get_pro_route(route_id=route["route_id"])
    #     route["pro_route_id"] = response[0]["_links"]["self"]["href"].split("/")[-1]
    # print(response_route_list)
    # print(len(response_route_list))
    # route_api_response_route_statistic = proapi_obj.get_pro_route_statistic(pro_route_id="12252")
    # print(route_api_response_route_statistic)

    # route_api_response_route_mintor = proapi_obj.get_pro_route_cars(pro_route_id="12252")
    # print(route_api_response_route_mintor)

    # proapi_obj.close_web_browser()

    # for x in route_list:
    #     print(dict(x))
    pass

