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
            ('other_expenses', 'Izdevumi kopa'),
            ('travel_allowance_total', 'Dienas naudas kopa:'),
]

class Report:
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
            
    def get_driver_month_report_routes(self, driver=None, year='2021', month='08'):
        """Return Route object list filtered by params"""
        data  = list(filter(lambda unit: unit.driver == driver, self.route_list))
        sorted_data = sorted(data, key= lambda route: route.route_id, reverse=True)
        return sorted_data

    def get_summary(self, route_obj_list= None):
        data= []
        for route_obj in route_obj_list:
             data.append({
                 "Reiss ID": route_obj.route_id,
                 "Reisa kārtas nr": route_obj.driver_route_id,
                 "Autovadītājs": route_obj.driver,
                 "Maršruts": route_obj.short_desc,
                 "Reisa sākuma d.": route_obj.start_date,
                 "Reisa beigu d.": route_obj.end_date,
                 "Nobraukti km": route_obj.km,
                 "Ienākumi": route_obj.revenue,
                 "Degviela iztērēta": route_obj.fuel_spent,
                 "Amorti. izm.": route_obj.amortization,
                 "Bruto alga": route_obj.driver_expenses,
                 "Pārējie izdevumi": route_obj.other_expenses,
                 "Prāmja izmaksas": route_obj.expenses,
                 "Rentabilitāte": route_obj.profitability,
                 "Peļņa": route_obj.profit_raw,
             })
        return data


    def get_all_drivers(self):
        return list(set(route.driver for route in self.route_list ))


# Tika veidots lai request ir no route objekta kas būtu loģiski bet par cik pieprasījumam nepieciešams web drivers, tas tiek pārnests uz report sadaļu, kur visam reportam ir viens
    
    def update_route_route_car_list(self, route_id_list=None):
        """Updates routes which are passed in with api request to pro.kurbads.lv"""
        if route_id_list == None or len(route_id_list) == 0:
            route_obj_list = self.route_list
        else:
            route_obj_list = list(filter(lambda unit: unit.route_id in route_id_list, self.route_list)) 
        for route_obj in route_obj_list:
            try:
                _ = self.api_driver.get_pro_route(route_obj.route_id)
                route_obj._pro_id = _[0]['_links']['self']['href'].split('/')[-1]
                route_obj.pro_route_cars = self.api_driver.get_pro_route_statistic(pro_route_id=route_obj._pro_id)
            except:
                pass
            
        
if __name__ == "__main__":
    pass