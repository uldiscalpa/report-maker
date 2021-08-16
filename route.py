import urllib.parse

class MaponRoute:
    """mapon route object""""
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
        self.start_odometer= start_odometer
        self.end_odometer= end_odometer
        self.fuel_level_start= fuel_level_start
        self.fuel_refilling_on_the_way= fuel_refilling_on_the_way
        self.fuel_refilling_end= fuel_refilling_end
        self.fuel_level_end= fuel_level_end
        self.driver_wage= driver_wage
        self.travel_allowance_total= travel_allowance_total
        
        self.pro_route_cars= pro_route_cars
        
        self._pro_id= None

       
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
    def country_codes(self):
        pass

if __name__ == "__main__":
    pass