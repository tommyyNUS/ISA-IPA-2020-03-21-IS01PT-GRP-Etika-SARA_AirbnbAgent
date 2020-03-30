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
    r.url(URL)
    if r.exist('//*/button[@type="submit"]') == True:
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
    r.type('//*[@id="Koan-via-SearchHeader__input"]', city)
    r.click('//*[@id="Koan-via-SearchHeader__option-0"]')
    print('Done.')     

def close_cookie_popup():
    if r.present("//button[@class='optanon-allow-all accept-cookies-button']") == True: r.click("//button[@class='optanon-allow-all accept-cookies-button']")

def monthyearconversion(datestamp):
    #monthyear = datestamp[3:]
    datestamp = datestamp.split(" ")
    return(datestamp[1]+" "+datestamp[2])


def monthyearnavigate(monthyear):
    compare = r.read(
        '//*[@aria-roledescription="datepicker"]/div/div[1]/div[2]/div/div/div')
    while(monthyear != compare):
        r.click('//*[contains(@aria-label,"Next")]')
        compare = r.read(
            '//*[@aria-roledescription="datepicker"]/div/div[1]/div[2]/div/div/div')


def enter_dates(checkin, checkout):
    print(f'Entering Check in and Check out Dates..{checkin} to {checkout}')  
    checkinmonthyear = monthyearconversion(checkin)
    # r.click('//*[@id="menuItemButton-date_picker"]/button')
    r.click('//*[@id="filter-menu-chip-group"]/div[2]/*')
    monthyearnavigate(checkinmonthyear)
    r.click(f'//*[contains(@aria-label,"{checkin}")]')

    monthyearnavigate(monthyearconversion(checkout))
    r.click(f'//*[contains(@aria-label,"{checkout}")]')
    r.click('//*[@id="filter-panel-save-button"]')
    print('Done.')    

def enter_personnel(adult,child,infant):
    print('Entering Personnel Information..')  
    r.click('//*[@id="filter-menu-chip-group"]/div[3]/*')
    for _i in range (adult):
        r.click('//*[@id="filterItem-stepper-adults-0"]/button[2]')
    for _i in range (child):
        r.click('//*[@id="filterItem-stepper-children-0"]/button[2]')
    for _i in range (infant):
        r.click('//*[@id="filterItem-stepper-infants-0"]/button[2]')
    r.click('//*[@id="filter-panel-save-button"]')
    print('Done.')   
    
def snap_map():
    print('Downloading Map..')   
    r.snap('//*[@id="ExploreLayoutController"]/div[2]/div[3]/aside/div',"map.jpg")
    print('Done."')   

def get_stay_url():
    url= [None] * 10 #catching top 10 in case of airbnb plus
    if (r.exist('//*[@id="FMP-target"]/div/div/div/div/div[1]/div/div/div/div[2]/a') == True):
        url[0]=URL+r.read('//*[@id="FMP-target"]/div/div/div/div/div[1]/div/div/div/div[2]/a/@href')
        for i in range(2,11) : url[i-1]=URL+r.read(f'//*[@id="FMP-target"]/div/div/div/div/div[{i}]/div/div/div/div[1]/a/@href')
    else:
        url[0]=URL+r.read('//div[@itemprop="itemList"]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/a/@href')
        for i in range(2,11) : url[i-1]=URL+r.read(f'//div[@itemprop="itemList"]/div[2]/div/div/div/div[2]/div/div/div/div/div[{i}]/div/div/div/div[1]/a/@href')
    #print(url)
    return(url)


def download_stay_picinfo(): #Downloads picture locally as jpg img, MIGHT be useful if we are doing local image classification....but I rather gcloud classify with url if needed
    print('Extracting Top 5 Stay Information..')   
    url=[]
    url=get_stay_url()
    print('Downloading Pics uploaded by host..') 
    i=0  
    k=0
    while (i<5):
        r.url(url[i+k])
        r.click('//*[@id="FMP-target"]')
        j=0
        while (1):
            j=j+1
            print(f'Downloading Homestay {i+1} Photo {j}')
            r.wait(0.4) 
            #r.snap('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img',f"data/{i+1}/{j}.jpg") #fastest but not perfect
            if (r.exist('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img/@src') == True): 
                dl_link=r.read('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img/@src')
                r.download(dl_link,f'data/{i+1}/{j}.jpg')
                print(f'Homestay {i+1} Photo {j} downloaded!')
            else:
                i=i-1 #Detects Whales (Airbnb Plus spoils the format alot)
                k=k+1 #Compensating Constant k
                print("WHALE detected, adding one more loop..")

            if (r.exist('/html/body/div[9]/div/div/div/div/div[3]/div/div[2]/button') == False or j >= 15): break #Max 15 photos
            r.click('/html/body/div[9]/div/div/div/div/div[3]/div/div[2]/button')
        i=i+1
    r.click('/html/body/div[9]/div/div/div/section/div/div[1]/div/button')
    print('Done.')      

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
        "url" :  ""
    },
    "1" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "" 
    },
    "2" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "" 
    },
    "3" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "" 
    },
    "4" : {
        "name" : "",
        "description" : "",
        "inventory" : "",
        "price" : "",
        "rating" : "",
        "picurl" : [None] * 10 ,
        "pictext" : [None] * 10,
        "url" :  "" 
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
        if (r.exist('//*[@data-plugin-in-point-id="TITLE_DEFAULT"]/div/div/section/div/div/h1') == True): 
            data[str(i)]["name"]=r.read('//*[@data-plugin-in-point-id="TITLE_DEFAULT"]/div/div/section/div/div/h1')
            data[str(i)]["description"]=r.read('//*[@data-plugin-in-point-id="OVERVIEW_DEFAULT"]/div/div/div/section/div/div/div/div/div')
            data[str(i)]["description"]=data[str(i)]["description"].replace("\xa0"," ")
            data[str(i)]["inventory"]=r.read('//*[@data-plugin-in-point-id="OVERVIEW_DEFAULT"]/div/div/div/section/div/div/div/div/div[2]')    
            data[str(i)]["price"]=r.read('//*[@data-plugin-in-point-id="BOOK_IT_SIDEBAR"]/div/div[2]/div/ul[2]/li/span[2]') #Total Price     
            data[str(i)]["rating"]=r.read('//*[@data-plugin-in-point-id="REVIEWS_DEFAULT"]/div/div/section/div/div/div/h2/span[2]/span')                  
            r.click('//*[@id="FMP-target"]')
            j=0
            while (1):
                j=j+1
                print(f'Extracting Picture Data - Homestay {i+1} Photo {j}')
                r.wait(0.4) 
                #r.snap('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img',f"data/{i+1}/{j}.jpg") #fastest but not perfect
                if (r.exist('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img/@src') == True): 
                    data[str(i)]["picurl"][j-1]=r.read('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div/div/img/@src')
                    if (r.present('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div[2]/div/span/div/span') == True):
                        data[str(i)]["pictext"][j-1]=r.read('//div[@data-testid="photo-viewer-slideshow-desktop"]/div/div/div/div[2]/div/span/div/span')
                    #r.download(dl_link,f'data/{i+1}/{j}.jpg')
                    print(f'Homestay {i+1} Photo {j} extracted!')
                if (r.exist('/html/body/div[9]/div/div/div/div/div[3]/div/div[2]/button') == False or j >= 10): break
                r.click('/html/body/div[9]/div/div/div/div/div[3]/div/div[2]/button')
        else:
            i=i-1 #Detects Whales (Airbnb Plus spoils the format alot)
            k=k+1 #Compensating Constant k
            print("WHALE detected, adding one more loop..")


        i=i+1
    r.click('/html/body/div[9]/div/div/div/section/div/div[1]/div/button')
    print('Done.')

    return data


