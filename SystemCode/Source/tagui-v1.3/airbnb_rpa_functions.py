# AirBnB RPA Functions
import os
import rpa as r
import shutil

URL = "https://www.airbnb.com.sg"
USERNAME = "rpatestuser001@gmail.com"
PASSWORD = "P@$$w0rd123"


def initialize():
    print('Initializing...')
    r.init()
    r.timeout(15) #set timeout to wait longer
    r.url(URL)
    while r.exist('//*/button[@type="submit"]') == False: 
        r.url(URL)
        print("Wrong page detected, retrying..")
    r.click('//*/button[@type="submit"]')  # Anti RPA by AirBnB
    print('Done.')

def recreate_temp(): #for image download
    print('Clearing Temp Files..')   
    shutil.rmtree('data/',ignore_errors=True)
    os.mkdir('data')
    os.mkdir('data/1')
    os.mkdir('data/2')
    os.mkdir('data/3')
    os.mkdir('data/4')
    os.mkdir('data/5')    
    print('Done.')   

def login():  # GG CAPTCHA (abandoned ship)
    r.click('//header[@role="banner"]/div/div/div[3]/div/div/nav/ul/li[6]')
    r.wait(10)
    if r.present('//div[@aria-label="Log in"]/div[2]/div[4]/button') == True:
        # Anti RPA by AirBnB
        r.click('//div[@aria-label="Log in"]/div[2]/div[4]/button')
    if r.present('//button[@data-testid="social-auth-button-email"]') == True:
        # Anti RPA by AirBnB
        r.click('//button[@data-testid="social-auth-button-email"]')
    r.type('//*[@id="email"]', USERNAME)
    r.type('//*[@id="password"]', PASSWORD)
    r.click('//button[@data-veloute="submit-btn-cypress"]')
    r.click('//*[@id="recaptcha-anchor"]/div[1]')


def logout():  # GG CAPTCHA (abandoned ship)
    r.click('//header[@role="banner"]/div/div/div[3]/div/div/nav/ul/li[6]')
    r.click('//*[@id="headerNavUserMenu"]/li[8]/form/button')


def select_stay():
    print('Selecting "Stays"...')   
    r.click('//*[@id="Koan-via-SearchHeader__input"]')
    r.click('//*[@id="Koan-via-SearchHeader__option-1"]')
    print('Done.')  


def enter_country_city(city):
    print(f'Entering City Information...{city}')
    #r.click('//*[@aria-label="Search"]')  
    r.type('//*[@placeholder="Add city, landmark, or address"]', city) 
    #r.type('//*[@id="Koan-via-SearchHeader__input"]', city)
    #r.click('//*[@id="Koan-via-SearchHeader__option-0"]')

    print('Done.')     

def close_cookie_popup():
    if r.present("//button[@class='optanon-allow-all accept-cookies-button']") == True: r.click("//button[@class='optanon-allow-all accept-cookies-button']")

def monthyearconversion(datestamp):
    monthyear=["",""]
    monthyear = datestamp.split(" ", 1)
    return(monthyear[1])

def monthyearnavigate(monthyear): 
    compare = r.read('//*[@aria-roledescription="datepicker"]/div/div[1]/div[2]/div/div/div')
    while(monthyear != compare):
        r.click('//*[contains(@aria-label,"Next")]')
        compare = r.read(
            '//*[@aria-roledescription="datepicker"]/div/div[1]/div[2]/div/div/div')


def enter_dates(checkin, checkout):
    r.click('//*[@role="search"]/div/div/div[3]/div/button')
    print(f'Entering Check in and Check out Dates..{checkin} to {checkout}')  
    checkinmonthyear = monthyearconversion(checkin)
    # r.click('//*[@id="menuItemButton-date_picker"]/button')
    # r.click('//*[@id="filter-menu-chip-group"]/div[2]/*')
    monthyearnavigate(checkinmonthyear)
    r.click(f'//*[contains(@aria-label,"{checkin}")]')

    monthyearnavigate(monthyearconversion(checkout))
    r.click(f'//*[contains(@aria-label,"{checkout}")]')
    print('Done.')    

def enter_personnel(adult,child,infant):
    r.click('//*[@role="search"]/div/div/div[5]/div/button')    
    print('Entering Personnel Information..')  
    #r.click('//*[@id="filter-menu-chip-group"]/div[3]/*')
    if r.exist('(//*[@aria-label="increase value"])[1]') == True:
        for _i in range (adult):
            r.click('(//*[@aria-label="increase value"])[1]')
        for _i in range (child):
            r.click('(//*[@aria-label="increase value"])[2]')
        for _i in range (infant):
            r.click('(//*[@aria-label="increase value"])[3]')
    else:
        for _i in range (adult):
            r.click('//*[@aria-describedby="subtitle-label-stepper-adults"][2]')
        for _i in range (child):
            r.click('//*[@aria-describedby="subtitle-label-stepper-children"][2]')
        for _i in range (infant):
            r.click('//*[@aria-describedby="subtitle-label-stepper-infants"][2]')        
    #r.click('//*[@id="filter-panel-save-button"]')
    print('Done.')   
    
def click_search():
    r.click('//button[@type="submit"]') 

def snap_map():
    print('Downloading Map..')   
    r.snap('//*[@id="ExploreLayoutController"]/div/div[3]/aside/div',"map.jpg")
    print('Done."')   

def get_stay_url():
    url= [None] * 10 #catching top 10 in case of airbnb plus
    if (r.exist('//*[@id="FMP-target"]/div/div/div/div/div[1]/div/div/div/div[1]/a') == True):
        url[0]=URL+r.read('//*[@id="FMP-target"]/div/div/div/div/div[1]/div/div/div/div[1]/a/@href')
        for i in range(2,11) : url[i-1]=URL+r.read(f'//*[@id="FMP-target"]/div/div/div/div/div[{i}]/div/div/div/div[1]/a/@href')
    else:
        url[0]=URL+r.read('//*[@itemprop="itemList"]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/a/@href')
        for i in range(2,11) : url[i-1]=URL+r.read(f'//*[@itemprop="itemList"]/div/div/div/div[2]/div/div/div/div/div[{i}]/div/div/div/div/a/@href')      
    #print(url)
    return(url)    

def extract_stay_info_as_data(): #Generates URL/text in dict instead, shorten time for upload/download, more unified

    data = {
    "0" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "",
        "coordinates" : ""
    },
    "1" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "", 
        "coordinates" : ""
    },
    "2" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "", 
        "coordinates" : ""
    },
    "3" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "",
        "coordinates" : ""
    },
    "4" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "", 
        "coordinates" : ""
    }
    }

    print('Extracting Top 5 Stay Picture Information (10 Image Max)..')   
    url=[]
    url=get_stay_url()
    i=0  
    k=0
    while (i<5):
        data[str(i)]["url"]=url[i+k]
        r.url(url[i+k])
        print(f'Extracting Text Data - Homestay {i+1}')
        if (r.exist('//*[@itemprop="name"]/span/h1/span') == True):
            data[str(i)]["coordinates"]=r.read('//*[@data-veloute="map/GoogleMap"]/div/div/div/div[2]/a/@href').split("=", 1)[1].split("&",1)[0]

            data[str(i)]["name"]=r.read('//*[@itemprop="name"]/span/h1/span')

            data[str(i)]["description"]=r.read('//*[@href="#neighborhood"]/div')
            #data[str(i)]["description"]=data[str(i)]["description"].replace("\xa0"," ")

            data[str(i)]["inventory"]= r.read('//*[@id="room"]/div[2]/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div') + " " + r.read('//*[@id="room"]/div[2]/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div[2]/div') + " " + r.read('//*[@id="room"]/div[2]/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div[3]/div') + " " + r.read('//*[@id="room"]/div[2]/div/div[2]/div/div/div[3]/div/div/div[1]/div/div/div[4]/div') 

            if (r.present('//*[@id="book_it_form"]/div[4]/div[2]') == True): data[str(i)]["price"]=r.read('//*[@id="book_it_form"]/div[4]/div[2]').split("Total",1)[1]
            else: data[str(i)]["price"]=r.read('//*[@id="book_it_form"]/div[2]').split("Total",1)[1] #Total Price  

            if r.present('//*[@data-heading-focus="review header"]/div'): data[str(i)]["rating"]=r.read('//*[@data-heading-focus="review header"]/div/div/@aria-label')+" ("+r.read('//*[@data-heading-focus="review header"]/div/span')+")"
            else: data[str(i)]["rating"]="No Reviews Yet"     

            r.click('//*[@data-veloute="hero-view-photos-button"]')
            j=0
            while (1):
                j=j+1
                print(f'Extracting Picture Data - Homestay {i+1} Photo {j}')
                r.wait(0.4) 
                #r.snap('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img',f"data/{i+1}/{j}.jpg") #fastest but not perfect
                if (r.exist('//img[@data-veloute="slideshow-image"]/@src') == True): 
                    data[str(i)]["picurl"][j-1]=r.read('//img[@data-veloute="slideshow-image"]/@src')
                    if (r.present('//*[@data-veloute="slideshow-modal"]/div/div/div[2]/div[2]/div[2]/div[2]/div') == True): 
                        data[str(i)]["pictext"][j-1]=r.read('//*[@data-veloute="slideshow-modal"]/div/div/div[2]/div[2]/div[2]/div[2]/div')
                    #r.download(dl_link,f'data/{i+1}/{j}.jpg')
                    print(f'Homestay {i+1} Photo {j} extracted!')

                if (r.exist('//button[@aria-label="Next"]') == False or j >= 7): break
                r.click('//button[@aria-label="Next"]')
        else:
            i=i-1 #Detects Whales (Airbnb Plus spoils the format alot)
            k=k+1 #Compensating Constant k
            print("WHALE detected, adding one more loop..")
        i=i+1
    #r.click('/html/body/div[9]/div/div/div/section/div/div[1]/div/button')
    print('Done.')

    return data


