from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import mysql.connector
from tkinter import *
import requests
from bs4 import BeautifulSoup
WINDOW_SIZE = "1920,1080"


mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='toor',
    database='internship'
)

mycursor=mydb.cursor()

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
    driver.find_element_by_name("domain").send_keys(url_use)
    driver.find_element_by_name("domain").send_keys(Keys.ENTER)

    time.sleep(1)

    k = driver.find_element_by_xpath(
        "/html/body/div[1]/section/div/div/div[1]/div[7]/div/table/tbody/tr[3]/td/strong").text

    if k == "Domain age unknown.":
        return factor_good
    domain_age=int(k[0:2])

    if domain_age>=3:
        factor_good = 1
    return factor_good


# def Alexa():
#     rank_str = BeautifulSoup(urllib.request.urlopen("https://www.alexa.com/minisiteinfo/" + Whois.calc().url_use),
#                              'html.parser', headers={'User-Agent': 'Mozilla/5.0'}).table.a.get_text()
#     global rank_int
#     rank_int = int(rank_str.replace(',', ''))

def do():
    url_p = url_b = "not in database"
    # check = "Unknown"
    global url_use
    url_use = url.get()

    url_for_database = "http://" + url_use
    https_url = "https://" + url_use

    # code to remove / from the end of domain
    if url_use[-1:] == "/":
        url_use = url_use[:-1]


    # Checking the url in DataBase
    mycursor.execute('select http from popular_sites where http=%s', (url_for_database,))
    for i in mycursor:
        url_p = i[0]

    mycursor.execute('select http from blocked_urls where http=%s', (url_for_database,))
    for i in mycursor:
        url_b = i[0]

    if url_p != "not in database" or url_b != "not in database":
        if url_for_database == url_p:
            check="It Is Not A Phishing Site"
            show_Label.config(text=check, bg='yellow')

        else:
            check = "It Is A Phishing Site"
            show_Label.config(text=check, bg='yellow')


    # Checking the url in phishtank database
    elif requests.get('https://www.phishtank.com/').status_code == 200:
        # google_security()
        # Whois()
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

        if current_url_link == 'https://www.phishtank.com/':
            driver.find_element_by_name("isaphishurl").send_keys((Keys.BACKSPACE) * 7)
            time.sleep(1)

            driver.find_element_by_name("isaphishurl").send_keys('https://' + url_use)
            time.sleep(1)

            driver.find_element_by_class_name("submitbutton").send_keys(Keys.ENTER)
            time.sleep(1)

            current_url_link = driver.current_url
            time.sleep(1)
            if current_url_link != 'https://www.phishtank.com/':

                result = requests.get(current_url_link)
                src = result.content

                soup = BeautifulSoup(src, 'lxml')

                link = soup.find_all("b")
                if "Is a phish" in link:
                    check = "It Is A Phishing Site"
                    show_Label.config(text=check, bg='yellow')
                    mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)",(url_for_database,https_url,))
                    mydb.commit()

                elif "Is NOT a phish" in link:
                    check = "It Is Not A Phishing Site"
                    show_Label.config(text=check, bg='yellow')
                    mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
                                         (url_for_database, https_url,))
                    mydb.commit()

                else:
                    google_security()
                    if google_lock:
                        check = "It Is A Phishing Site"
                        show_Label.config(text=check, bg='yellow')
                        mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)",
                                             (url_for_database, https_url,))
                        mydb.commit()


                    # elif rank_int <= 150000:
                    #     check = "It Is Not A Phishing Site"
                    #     show_Label.config(text=check, bg='yellow')
                    #     mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
                    #                                          (url_for_database, https_url,))
                    #     mydb.commit()
                    #

                    elif Whois():
                            check = "It Does Not Looks A Phishing Site"
                            show_Label.config(text=check, bg='yellow')

                    else:
                        check = "It Can Be A Phishing Site"
                        show_Label.config(text=check, bg='yellow')

            else:
                if google_lock:
                    check = "It Is A Phishing Site"
                    show_Label.config(text=check, bg='yellow')
                    mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)",
                                     (url_for_database, https_url,))
                    mydb.commit()

                # elif rank_int <= 150000:
                #     check = "It Is Not A Phishing Site"
                #     show_Label.config(text=check, bg='yellow')
                #     mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
                #                                          (url_for_database, https_url,))
                #     mydb.commit()

                elif factor_good == 1:
                    check = "It Does Not Looks A Phishing Site"
                    show_Label.config(text=check, bg='yellow')

                else:
                    check = "It Can Be A Phishing Site"
                    show_Label.config(text=check, bg='yellow')

        elif current_url_link != 'https://www.phishtank.com/':

            result = requests.get(current_url_link)
            src = result.content

            soup = BeautifulSoup(src, 'lxml')

            link=soup.find_all("b")
            if "Is a phish" in link:
                check="It Is A Phishing Site"
                show_Label.config(text=check,bg='yellow')
                mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)",
                                     (url_for_database, https_url,))
                mydb.commit()

            elif "Is NOT a phish" in link:
                check="It Is Not A Phishing Site"
                show_Label.config(text=check,bg='yellow')
                mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
                                     (url_for_database, https_url,))
                mydb.commit()


            else :
                google_security()
                if google_lock:
                    check = "It Is A Phishing Site"
                    show_Label.config(text=check, bg='yellow')
                    mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)",
                                         (url_for_database, https_url,))
                    mydb.commit()

                # elif rank_int <= 150000:
                #     check = "It Is Not A Phishing Site"
                #     show_Label.config(text=check, bg='yellow')
                #     mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
                #                                          (url_for_database, https_url,))
                #     mydb.commit()

                elif Whois():
                    check = "It Does Not Looks A Phishing Site"
                    show_Label.config(text=check, bg='yellow')

                else:
                    check = "It Can Be A Phishing Site"
                    show_Label.config(text=check, bg='yellow')

        elif google_lock:
            google_security()
            check = "It Is A Phishing Site"
            show_Label.config(text=check, bg='yellow')
            mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)", (url_for_database, https_url,))
            mydb.commit()

        # elif rank_int<=150000:
        #     check = "It Is Not A Phishing Site"
        #     show_Label.config(text=check,bg='yellow')
        #     mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
        #                                          (url_for_database, https_url,))
        #     mydb.commit()

        elif Whois():
            check = "It Does'nt Looks Like A Phishing Site"
            show_Label.config(text=check, bg='yellow')

        else:
            check = "It Can Be A Phishing Site"
            show_Label.config(text=check, bg='yellow')

    elif google_lock:
        google_security()
        check = "It Is A Phishing Site"
        show_Label.config(text=check, bg='yellow')
        mycursor.execute("Insert into blocked_urls (http,https) values (%s, %s)", (url_for_database, https_url,))
        mydb.commit()

    # elif rank_int <= 150000:
    #     check = "It Is Not A Phishing Site"
    #     show_Label.config(text=check, bg='yellow')
    #     mycursor.execute("Insert into popular_sites (http,https) values (%s, %s)",
    #                                          (url_for_database, https_url,))
    #     mydb.commit()

    elif Whois():
        check = "It Does'nt Looks Like A Phishing Site"
        show_Label.config(text=check, bg='yellow')

    else:
        check = "It Can Be a Phishing site"
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