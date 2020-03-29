#Main Routine
import rpa as r
import airbnb_rpa_functions as airbnb
import time

def process(country, numOfAdults, numOfInfants, numOfChildren, fromDate, toDate):
    start = time.time()

    airbnb.initialize()
    r.wait()
    airbnb.select_stay()
    r.wait()
    airbnb.enter_country_city(country)
    airbnb.close_cookie_popup()
    r.wait()
    airbnb.enter_dates(fromDate,toDate)
    r.wait()
    #adult, infant, child
    #airbnb.enter_personnel(1,2,3)
    airbnb.enter_personnel(numOfAdults,numOfInfants,numOfChildren)

    #airbnb.recreate_temp()
    airbnb.snap_map()
    data = airbnb.extract_stay_info_as_data()
    print(data)
    r.close()

    end = time.time()

    elapsed = end - start
    print(f'Time Elapsed: {elapsed} seconds')  

    response =  """
            Country : {0}
            Num: {1}
            From: {2}
            To: {3}
        """.format(country, numOfPeople, fromDate, toDate)
    
    return response
