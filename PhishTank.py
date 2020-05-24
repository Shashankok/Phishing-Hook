from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from tkinter import *
import requests
from bs4 import BeautifulSoup
WINDOW_SIZE = "1920,1080"



popular_sites_url=['http://google.com','http://geeksforgeeks.org','http://javatpoint.com', 'http://ucnews.in', 'http://youtube.com', 'http://facebook.com', 'http://ucweb.com','http://python.org','http://instagram.com','http://gmail.com', 'http://xnxx.tv', 'http://xvideos3.com', 'http://google.co.in', 'http://xnxx.com', 'http://twitter.com', 'http://xvideos.com', 'http://google.com.br', 'http://wikipedia.org', 'http://covid19india.org', 'http://indiatimes.com', 'http://xvideos2.com', 'http://xhamster2.desi', 'http://whatsapp.com', 'http://amazon.in', 'http://cgtn.com', 'http://zoom.us', 'http://quora.com', 'http://worldometers.info', 'http://9apps.com', 'http://yahoo.com', 'http://linkedin.com', 'http://news18.com', 'http://anybunny.tv', 'http://youtu.be', 'http://flipkart.com', 'http://freepornfull.com', 'http://onlinesbi.com', 'http://netflix.com', 'http://xhamster.com', 'http://pinterest.com', 'http://hotstar.com', 'http://rummycircle.com', 'http://bit.ly', 'http://ndtv.com', 'http://softcore69.com', 'http://freeindianporn.mobi', 'http://office.com', 'http://moneycontrol.com', 'http://tamiltips.ga', 'http://pornhdvideos.net', 'http://timesofindia.com', 'http://primevideo.com', 'http://xnxxfap.com', 'http://livemint.com', 'http://baidu.com', 'http://pornhub.com', 'http://amazon.com', 'http://yandex.ru', 'http://vk.com', 'http://live.com', 'http://yahoo.co.jp', 'http://naver.com', 'http://reddit.com', 'http://mail.ru', 'http://ok.ru', 'http://qq.com', 'http://ebay.com', 'http://microsoft.com', 'http://bing.com', 'http://msn.com', 'http://bilibili.com', 'http://amazon.co.jp', 'http://rakuten.co.jp', 'http://globo.com', 'http://microsoftonline.com', 'http://amazon.de', 'http://paypal.com', 'http://twitch.tv', 'http://google.de', 'http://roblox.com', 'http://uol.com.br', 'http://imdb.com', 'http://google.co.jp']

def google_security():
    global google_lock

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    driver = webdriver.Chrome(executable_path='E:\selenium\chromedriver.exe', chrome_options=chrome_options)

    driver.get("https://transparencyreport.google.com/safe-browsing/search")

    driver.find_element_by_class_name("ng-pristine").send_keys('https://' + url_use)
    driver.find_element_by_class_name("ng-valid").send_keys(Keys.ENTER)

    driver.execute_script("window.scrollTo(0, 600)")
    time.sleep(2)
    google_secure_url = driver.current_url

    driver.get_screenshot_as_file("capture.png")
    google_lock = False
    from PIL import Image
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
    img = Image.open("capture.png")
    text_img = pytesseract.image_to_string(img)
    text_img = text_img.split("\n")
    if "A This site is unsafe" in text_img:
        google_lock = True


def Whois():
    global factor_good
    factor_good = 0
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    from selenium.webdriver.chrome.options import Options
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    driver = webdriver.Chrome(executable_path='E:\selenium\chromedriver.exe', chrome_options=chrome_options)

    driver.get("https://www.iplocation.net/domain-age")
    driver.find_element_by_name("domain").send_keys("gmail.com")
    driver.find_element_by_name("domain").send_keys(Keys.ENTER)

    time.sleep(1)

    k = driver.find_element_by_xpath(
        "/html/body/div[1]/section/div/div/div[1]/div[7]/div/table/tbody/tr[3]/td/strong").text
    domain_age=int(k[0:2])

    if domain_age>=3:
        factor_good = 1

# def Alexa():
#     rank_str = BeautifulSoup(urllib.request.urlopen("https://www.alexa.com/minisiteinfo/" + Whois.calc().url_use),
#                              'html.parser', headers={'User-Agent': 'Mozilla/5.0'}).table.a.get_text()
#     global rank_int
#     rank_int = int(rank_str.replace(',', ''))

def do():

    check = "Unknown"
    global url_use
    url_use = url.get()
    # Checking the url in popular sites
    if "http://"+url_use in popular_sites_url:
        check="It Is Not A Phishing Site"
        show_Label.config(text=check, bg='yellow')

    # Checking the url in phishtank database
    elif requests.get('https://www.phishtank.com/').status_code == 200:
        google_security()
        Whois()
        # Alexa()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

        driver = webdriver.Chrome(executable_path='E:\selenium\chromedriver.exe', chrome_options=chrome_options)

        driver.get("https://www.phishtank.com/")
        time.sleep(1)

        driver.find_element_by_name("isaphishurl").send_keys(url_use)
        time.sleep(1)

        driver.find_element_by_class_name("submitbutton").send_keys(Keys.ENTER)
        time.sleep(1)

        current_url_link = driver.current_url
        time.sleep(1)


        if current_url_link != 'https://www.phishtank.com/':

            result = requests.get(current_url_link)
            src = result.content

            soup = BeautifulSoup(src, 'lxml')

            for link in soup.find_all("b"):
                if "Is a phish" in link:
                    check="It Is A Phishing Site"
                    show_Label.config(text=check,bg='yellow')

                elif "Is NOT a phish" in link:
                    check="It Is Not A Phishing Site"
                    show_Label.config(text=check,bg='yellow')


                else:
                    if google_lock:
                        check = "It Is A Phishing Site"
                        show_Label.config(text=check, bg='yellow')

                    # elif rank_int <= 150000:
                    #     check = "It Is Not A Phishing Site"
                    #     show_Label.config(text=check, bg='yellow')

                    elif factor_good == 1:
                        check = "It Does Not Looks A Phishing Site"
                        show_Label.config(text=check, bg='yellow')

                    else:
                        check = "It Can Be A Phishing Site"
                        show_Label.config(text=check, bg='yellow')

        elif google_lock:
            check = "It Is A Phishing Site"
            show_Label.config(text=check, bg='yellow')

        # elif rank_int<=150000:
        #     check = "It Is Not A Phishing Site"
        #     show_Label.config(text=check,bg='yellow')

        elif factor_good==1:
            check = "It Does'nt Looks Like A Phishing Site"
            show_Label.config(text=check, bg='yellow')

        else:
            check = "It Can Be A Phishing Site"
            show_Label.config(text=check, bg='yellow')

    elif google_lock:
        check = "It Is A Phishing Site"
        show_Label.config(text=check, bg='yellow')

    # elif rank_int <= 150000:
    #     check = "It Is Not A Phishing Site"
    #     show_Label.config(text=check, bg='yellow')

    elif factor_good == 1:
        check = "It Does'nt Looks Like A Phishing Site"
        show_Label.config(text=check, bg='yellow')

    else:
        check = "It Does'nt Looks Like A Phishing Site"
        show_Label.config(text=check, bg='yellow')


root=Tk()
root.geometry("300x300")
root.maxsize(300,300)
root.minsize(300,300)

url = StringVar()
root.title("Phishing Hook")

Label(root,text="Phishing Hook",font=("Trajan","26"),fg="purple").pack()
Label(root,text="").pack()

url_Label=Label(root,text="Enter URL: ").pack()
url_Entry=Entry(root,textvariable=url).pack()

Label(root,text="").pack()
enter_btn=Button(root,text="Capture The Phish",fg="red",bg="aquamarine",command=do).pack()
Label(root,text="").pack()
Label(root,text="").pack()

show_Label=Label(root)
show_Label.pack()


root.mainloop()