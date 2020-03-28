#Main Routine
import rpa as r
import airbnb_rpa_functions as airbnb
import time

start = time.time()

airbnb.initialize()
r.wait()
airbnb.select_stay()
r.wait()
airbnb.enter_country_city("milan")
airbnb.close_cookie_popup()
r.wait()
airbnb.enter_dates("25 December 2020","30 December 2020")
r.wait()
airbnb.enter_personnel(1,2,3)
#airbnb.recreate_temp()
airbnb.snap_map()
airbnb.extract_stay_info_as_data()
r.close()

end = time.time()

elapsed = end - start
print(f'Time Elapsed: {elapsed} seconds')

