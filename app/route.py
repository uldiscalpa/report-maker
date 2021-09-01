import matplotlib.pyplot as plt

from datetime import datetime
import urllib.parse



class MaponRoute:
    """mapon route object"""
    BASE_URL = "https://mapon.com/pro/"

    def __init__(
            self,
            mapon_truck_id,
            start_date_time,
            end_date_time,
    ):
        self.mapon_truck_id = mapon_truck_id
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time

    def get_mapon_web_route_link(self):
        """date format string yyyy-mm-dd hh:mm:ss"""
        links_strings = [
            "online#openCar=",
            self.mapon_truck_id,
            "&activeDetail=1&range=",
            self.start_date_time,
            ',',
            self.end_date_time,
        ]
        return  urllib.parse.quote("".join(links_strings), safe="=/#&")


class Route:

    amortization_rate = 0.064
    salary_bruto_koef = 1.77
    
    def __init__(
        self,
        route_id= None,
        truck= None,
        driver_route_id= None,
        driver= None,
        short_desc= None,
        start_date= None,
        end_date= None,
        report_date= None,
        start_odometer= None,
        end_odometer= None,
        fuel_level_start= None,
        fuel_refilling_on_the_way= None,
        fuel_refilling_end= None,
        fuel_level_end= None,
        driver_wage= None,
        other_expenses= None,
        travel_allowance_total= None,
        pro_route_cars= None,

        *args,
        **kwargs,
    ):
        self.route_id= route_id
        self.truck= truck
        self.driver_route_id= driver_route_id
        self.driver= driver
        self.short_desc= short_desc
        self.start_date= start_date
        self.end_date= end_date
        self.report_date= report_date
        self.start_odometer= start_odometer # if start_odometer!= None else
        self.end_odometer= end_odometer
        self.fuel_level_start= fuel_level_start if fuel_level_start != None else 0
        self.fuel_refilling_on_the_way= fuel_refilling_on_the_way if fuel_refilling_on_the_way != None else 0
        self.fuel_refilling_end= fuel_refilling_end if fuel_refilling_end != None else 0
        self.fuel_level_end= fuel_level_end if fuel_refilling_end != None else 0
        self.driver_wage= driver_wage
        self.other_expenses= other_expenses if fuel_refilling_end != None else 0
        self.travel_allowance_total= travel_allowance_total
        
        self.pro_route_cars= pro_route_cars

       
    @property
    def revenue(self):
        return sum( route_car['revenue'] for route_car in self.pro_route_cars)
    
    @property
    def expenses(self):
        return sum( route_car['expenses'] for route_car in self.pro_route_cars)
    
    @property
    def km(self):
        return self.end_odometer - self.start_odometer
        
    @property
    def scissors(self):
        pass
    
    @property
    def profitability(self):
        return (self.revenue - self.expenses) / self.km

    @property
    def fuel_spent(self):
        return self.fuel_level_start + self.fuel_refilling_on_the_way + self.fuel_refilling_on_the_way - self.fuel_level_end

    @property
    def amortization(self):
        return self.km * self.amortization_rate

    @property
    def salary_bruto(self):
        return self.driver_wage * self.salary_bruto_koef

    @property
    def driver_expenses(self):
        return self.salary_bruto + self.travel_allowance_total

    @property
    def profit_raw(self):
        return self.revenue - self.fuel_spent - self.driver_expenses - self.other_expenses - self.expenses - self.amortization


    def route_cars_export_format(self):
        data = []
        for route_car in self.pro_route_cars:
            data.append({
                "Autovedējs": self.truck,
                "Šoferis": self.driver,
                "Uzkraušana": route_car["pickupLocation_location"],
                "RV uzkraušana": route_car["pickupLocation_sequence"],
                "Nokraušana": route_car["dropLocation_location"],
                "Klients": route_car["order_customer"],
                "PA sākumpunkts": route_car["groupStartLocation"],
                "PA galapunkts": route_car["groupEndLocation"],
                "Modelis": route_car["orderCar_carModel"],
                "VIN": route_car["orderCar_vin"],
                "CMR": route_car["orderCar_cmr_cmrId"],
                "Rēķina summa": route_car["transportationPrice"],
                "Ienākumi": route_car["revenue"],
            }
            )
        return sorted(data, key=lambda key: key["RV uzkraušana"])

    def get_route_load_plot(self):
        fig, gnt = plt.subplots()
        
        i = 1
        start_point_date = self._date_parser(self.pro_route_cars[0]['pickupLocation_date'])
        for car in sorted(self.pro_route_cars, key=lambda key: key["pickupLocation_sequence"], reverse=True):

            car_start_mark = self._date_parser(car['pickupLocation_date']) - start_point_date
            start_point = car_start_mark.days * 24 + car_start_mark.seconds // 3600

            car_pick_up_date = self._date_parser(car['pickupLocation_date'])
            car_unload_date = self._date_parser(car['dropLocation_date'])
            car_on_truck_days = car_unload_date - car_pick_up_date

            car_on_truck_hours = car_on_truck_days.days * 24 + car_on_truck_days.seconds // 3600

            gnt.grid(True)
            gnt.broken_barh([(start_point, car_on_truck_hours)], (i, 0.8), facecolors =('tab:orange'))

            i += 1

        gnt.set_xlabel('')
        gnt.set_ylabel('')
        gnt.set_yticks([])
        gnt.set_yticklabels([])
        gnt.set_xticklabels([])
        print(self.route_id)
        plt.show()


    def _date_parser(self, date_string):
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f" )


# Tika veidots lai request ir no route objekta kas būtu loģiski
# bet par cik pieprasījumam nepieciešams web drivers, tas tiek pārnests uz report sadaļu, kur visam reportam ir viens

    # def update_pro_route_id(self):
    #     """updates self. pro route id"""
    #     _ = self.api_driver.get_pro_route(self.route_id)
    #     self._pro_id = _[0]['_links']['self']['href'].split('/')[-1]


    # def update_route_route_car_list(self):
    #     """Updates routes which are passed in with api request to pro.kurbads.lv"""
    #     if self._pro_id == None:
    #         self.update_pro_route_id()
    #     self.pro_route_cars = self.api_driver.get_pro_route_statistic(pro_route_id=self._pro_id)

import pickle

if __name__ == "__main__":
    with open("route_ojb.pkl", "rb") as f:
        route_obj = pickle.load(f)

    route_obj.get_route_load_plot()