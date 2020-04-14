#Main Routine
import rpa as r
import airbnb_rpa_functions as airbnb
import time

def process(country, numOfAdults, numOfInfants, numOfChildren, fromDate, toDate):
    start = time.time()

    airbnb.initialize()
    r.wait()
	#airbnb.select_stay()
	#r.wait()
    airbnb.close_cookie_popup()
    airbnb.enter_country_city(country)
    airbnb.enter_dates(fromDate,toDate)
	#airbnb.enter_personnel(2,2,1)
    airbnb.enter_personnel(numOfAdults,numOfChildren,numOfInfants)
    airbnb.click_search()
    r.wait()
	#airbnb.recreate_temp()
    #airbnb.snap_map()
    data = airbnb.extract_stay_info_as_data()
    print("Sending Date back to controller")
    print(data)
    r.close()

    end = time.time()

    elapsed = end - start
    print(f'Time Elapsed: {elapsed} seconds')
	
    response =  data
    
    return response

