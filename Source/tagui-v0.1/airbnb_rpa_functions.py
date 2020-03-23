#AirBnB RPA Functions
import rpa as r

URL = "https://www.airbnb.com.sg"
USERNAME = "rpatestuser001@gmail.com"
PASSWORD = "P@$$w0rd123"

def initialize():
    r.init(); r.url(URL)
    if r.exist('//*/button[@type="submit"]') == True: r.click('//*/button[@type="submit"]') #Anti RPA by AirBnB

def login(): #GG CAPTCHA
    r.click('//header[@role="banner"]/div/div/div[3]/div/div/nav/ul/li[6]')
    r.wait(10)
    if r.present('//div[@aria-label="Log in"]/div[2]/div[4]/button') == True: r.click('//div[@aria-label="Log in"]/div[2]/div[4]/button') #Anti RPA by AirBnB
    if r.present('//button[@data-testid="social-auth-button-email"]') == True: r.click('//button[@data-testid="social-auth-button-email"]') #Anti RPA by AirBnB
    r.type('//*[@id="email"]',USERNAME)
    r.type('//*[@id="password"]',PASSWORD)
    r.click('//button[@data-veloute="submit-btn-cypress"]')
    r.click('//*[@id="recaptcha-anchor"]/div[1]')

def logout():
    r.click('//header[@role="banner"]/div/div/div[3]/div/div/nav/ul/li[6]')
    r.click('//*[@id="headerNavUserMenu"]/li[8]/form/button')       

def select_stay():
    r.click('//*[@id="Koan-via-SearchHeader__input"]')
    r.click('//*[@id="Koan-via-SearchHeader__option-1"]')

def enter_country_city(city):
    r.type('//*[@id="Koan-via-SearchHeader__input"]',city)
    r.click('//*[@id="Koan-via-SearchHeader__option-0"]')


def monthyearconversion(datestamp):
    monthyear=datestamp[3:]
    return(monthyear)

def monthyearnavigate(monthyear):
    compare = r.read('//*[@aria-roledescription="datepicker"]/div/div[1]/div[2]/div/div/div')
    while(monthyear != compare): 
        r.click('//*[contains(@aria-label,"Next")]')
        compare = r.read('//*[@aria-roledescription="datepicker"]/div/div[1]/div[2]/div/div/div')


def enter_dates(checkin,checkout):
    checkinmonthyear=monthyearconversion(checkin)
    #r.click('//*[@id="menuItemButton-date_picker"]/button')
    r.click('//*[@id="filter-menu-chip-group"]/div[2]/*')
    monthyearnavigate(checkinmonthyear)
    r.click(f'//*[contains(@aria-label,"{checkin}")]')

    monthyearnavigate(monthyearconversion(checkout))
    r.click(f'//*[contains(@aria-label,"{checkout}")]')
    r.click('//*[@id="filter-panel-save-button"]')



