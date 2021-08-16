import pandas as pd

from proapi import ProApi
from route import Route


dict_mapper = [
            ('route_id', "Reisa ID"),
            ('truck', 'Autovedejs'),
            ('driver_route_id', 'Reisa kartas numurs'),
            ('driver', 'Autovaditajs 1'),
            ('short_desc', 'Reisa Marsruts isais'),
            ('start_date', 'Reisa sakuma datums'),
            ('end_date', 'Reisa beigu datums'),
            ('report_date', 'Datums reisa atskaites'),
            ('start_odometer', 'km reisa sakuma odometrs'),
            ('end_odometer', 'km reisa beigas odometrs'),
            ('fuel_level_start', 'Degviela baka uzsakot reisu'),
            ('fuel_refilling_on_the_way', 'Degviela Reisa laika uzpildita citur'),
            ('fuel_refilling_end', 'Degviela reisa laika uzpildita Baze Kopa'),
            ('fuel_level_end', 'Degviela baka beidzot reisu'),
            ('driver_wage', 'Atalgojums kopa'),
            ('travel_allowance_total', 'Dienas naudas kopa:'),
]

class Reports:
    """Class represent list of bulk of routes"""
    
    def __init__(self,):
        self.route_list = []
        self.api_driver = ProApi()


    def _read_route_excel_pandas(self, file_name=''):        
        df = pd.read_excel(
            file_name,
            parse_dates=[
                "Reisa sakuma datums",
                "Reisa beigu datums",
                "Datums reisa atskaites",
            ],
        )
        return df
    
    def _dict_converter(self, dict_in, _map):
        dict_out = {}
        for _map in _map:
            key_out, key_in = _map
            dict_out[key_out] = dict_in[key_in]
        return dict_out
    
    def import_routes_pandas(self, file_name=''):
        df = self._read_route_excel_pandas(file_name=file_name)
        route_id_list = df["Reisa ID"].unique()
        
        for route_id in route_id_list:
            route_dict = {}
            _dict = df.loc[df['Reisa ID']== route_id].to_dict(orient='records')
            route_dict = self._dict_converter(_dict[0], dict_mapper)
            self.route_list.append(Route(**route_dict))
        print("Imported!")
            
    def get_driver_month_report(self, driver=None, year='2021', month='08'):
        """Return Route object list filtered by params"""
        return list(filter(lambda unit: unit.driver == driver, self.route_list))
    
    def update_route_route_car_list(self, route_id_list=None):
        """Updates routes which are passed in with api request to pro.kurbads.lv"""
        if route_id_list == None or len(route_id_list) == 0:
            route_obj_list = self.route_list
        else:
            route_obj_list = list(filter(lambda unit: unit.route_id in route_id_list, self.route_list)) 
        for route_obj in route_obj_list:
            _ = self.api_driver.get_pro_route(route_obj.route_id)
            route_obj._pro_id = _[0]['_links']['self']['href'].split('/')[-1]
            route_obj.pro_route_cars = self.api_driver.get_pro_route_statistic(pro_route_id=route_obj._pro_id)
            
        
if __name__ == "__main__":
    pass