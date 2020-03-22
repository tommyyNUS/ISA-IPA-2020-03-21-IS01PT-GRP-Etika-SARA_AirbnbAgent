#Main Routine
import rpa as r
import airbnb_rpa_functions as airbnb

airbnb.initialize()
r.wait()
airbnb.select_stay()
r.wait()
airbnb.enter_country_city("san francisco")
r.wait()
airbnb.enter_dates("21 July 2020","18 December 2020")
r.wait()
r.close()