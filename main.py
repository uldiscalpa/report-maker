from report import Report
from excel_export import ExcelCreator

import pickle




def main():
    
    # #  Datu ielasīšana pick filā
    

    # ilonas_file_name = "ilonas_reisi.xlsx"
    # report = Report()
    # report.import_routes_pandas(file_name=ilonas_file_name)
            
    # route_list = [route.route_id for route in report.route_list]
    # report.update_route_route_car_list(route_list)

    # report.api_driver.close_web_browser()

    # # ################
    # #  report obj ierakstīšana pickle
    # ##################


    # with open("report_ojb.pkl", "wb")as f:
    #     pickle.dump(report.route_list, f)



    with open("report_ojb.pkl", "rb") as f:
        route_list = pickle.load(f)
    
    report = Report()
    report.route_list = route_list

    driver = "Jeremy Sayer"
    year = "2021"
    month = "08"
    for driver in report.get_all_drivers():
        driver_month_routes = report.get_driver_month_report_routes(driver=driver, year= year, month= month)

        export_obj = ExcelCreator(file_name=year + " " + month + " " + driver + ".xlsx")
        for route in driver_month_routes:
            data_list = route.route_cars_export_format()
            work_sheet_name = route.route_id
            export_obj.write_report(work_sheet_name=work_sheet_name, data_list= data_list)
            
        # print(report.get_summary(route_obj_list=driver_month_routes))
        export_obj.write_report(work_sheet_name="Kopsavlikums", data_list= report.get_summary(route_obj_list=driver_month_routes))

    report.route_list[0].get_route_load_plot()

    # with open("route_ojb.pkl", "wb")as f:
    #     pickle.dump(report.route_list[0], f)

    # export_obj = ExcelCreator(file_name=year + month + driver + ".xlsx")
    # for route in driver_month_routes:
    #     data_list = [
    #         {
    #             "Reiss": route.route_id,
    #             "Autovedējs": route.truck,
    #         }
    #     ]
    #     export_obj.write_report(work_sheet_name=route.route_id, data_list= data_list)



    # print([route.pro_route_cars for route in report.route_list])


if __name__ == "__main__":
    main()
