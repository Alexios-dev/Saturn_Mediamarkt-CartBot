import datetime
import random
import time
import selenium
import requests
import os
import sys
try:
    import undetected_chromedriver.v2 as uc
except:
    pass
from discordwebhook import Discord
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ForwardedEmail = []
ThreadsTab = []

def SendMessage(DC_Url,Mediamarkt_Url,Cost):
    webhook = Discord(url=DC_Url)
    webhook.post(embeds=[{"title": "Ps5 drop", "description": "Ps5 drop by: "+Mediamarkt_Url+" Cost:"+str(Cost)}],)

class Tab():
    def __init__(self,email,password, vorname, nachname, plz, stadt, straße, hausnummer, carting,productUrl,webHook):
        self.user = [vorname, nachname, plz, stadt, straße, hausnummer, email, password]
        self.Vorname = vorname
        self.Nachname = nachname
        self.PLZ = plz
        self.Stadt = stadt
        self.Straße = straße
        self.Hausnummer = hausnummer
        self.Email = email
        self.Password = password
        self.Cartingnumber = carting
        self.ProductUrl = productUrl
        self.WebHook = webHook
        # Cart Address
        self.Xpath_addtocart = '//*[@id="pdp-add-to-cart-button"]'
        self.Xpath_addtocart_Cookies = '/html/body/div[3]/div/form/div/div/div[2]/div/div/button[4]'
        self.Xpath_addtocart_Cart = '//*[@id="root"]/div[2]/div[3]/div[1]/div[1]/div/div[2]/div/p'

        # Checkout Address Url
        self.Url_checkoutAddress = 'https://www.mediamarkt.de/checkout/address'

        # Checkout Address Xpath
        self.Xpath_Address_Firstname = '//*[@id="shipping_firstname"]'
        self.Xpath_Address_Lastname = '//*[@id="shipping_lastname"]'
        self.Xpath_Address_Zipcode = '//*[@id="shipping_zipcode"]'
        self.Xpath_Address_City = '//*[@id="shipping_city"]'
        self.Xpath_Address_Street = '//*[@id="street"]'
        self.Xpath_Address_Number = '//*[@id="shipping_houseNumber"]'
        self.Xpath_Address_Email = '//*[@id="customer_email"]'

        self.Xpath_Address = [self.Xpath_Address_Firstname, self.Xpath_Address_Lastname, self.Xpath_Address_Zipcode,
                              self.Xpath_Address_City, self.Xpath_Address_Street
            , self.Xpath_Address_Number, self.Xpath_Address_Email]

        self.Xpath_Address_next = '//*[@id="root"]/div[2]/div[3]/div[1]/div/div[2]/form/div/div[11]/div/button'
        # Checkout Payment Url
        self.Url_Payment = 'https://www.mediamarkt.de/checkout/payment'

        # Checkout Payment Xpath
        self.Xpath_Payment_method = '//*[@id="root"]/div[2]/div[3]/div[1]/div/div[2]/div/div[5]/div/div[1]/div[1]/div/div[1]'
        self.Xpath_Payment_next = '//*[@id="root"]/div[2]/div[3]/div[1]/div/div[2]/div/div[11]/div/button'

        # Checkout finally Url
        self.Url_Finally = 'https://www.mediamarkt.de/checkout/summary'

        # Checkout finnaly Xpath
        self.Xpath_finally_proofText = '//*[@id="root"]/div[2]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[1]/h3'
        self.Xpath_finally_next = '//*[@id="root"]/div[2]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button'

        # Payment Login Email Xpath
        self.Xpath_Payment_Email = '//*[@id="email"]'

    def main(self):
        for i in range(1,int(self.Cartingnumber)+1):
            self.OpenTab()
            while True:
                if self.Carting():
                    break
            while True:
                if self.CheckoutAddress():
                    break
                elif not self.CheckoutAddress():
                    if self.Carting():
                        break
            while True:
                if self.CheckoutPayment():
                    break
            while True:
                if self.CheckoutFinally():
                    break
            while True:
                if self.SendMail():
                    break
            self.driver.close()
    def OpenTab(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument("--diable-backgrounding-occluded-windows")
        self.options.headless = True
        while True:
            try:
                self.driver = uc.Chrome(version_main=93, options=self.options)
                return True
            except:
                pass

    def PushText(self, xpath, text):
        textbutton = self.driver.find_element_by_xpath(xpath)
        textbutton.send_keys(text)

    def PushButton(self, xapth):
        button = self.driver.find_element_by_xpath(xapth)
        button.click()

    def Carting(self):
        self.driver.get(self.ProductUrl)
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.Xpath_addtocart_Cookies))
            )
            while True:
                try:
                    self.PushButton(self.Xpath_addtocart_Cookies)
                except:
                    break

        except TimeoutException:
            pass
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.Xpath_addtocart))
            )


        except TimeoutException:
            return False
        time.sleep(3)

        try:
            self.PushButton(self.Xpath_addtocart)
            time.sleep(1)
            self.PushButton(self.Xpath_addtocart)
        except:
            pass
        return True

    def CheckoutAddress(self):
        while True:
            self.driver.get(self.Url_checkoutAddress)
            if self.driver.current_url == self.Url_checkoutAddress:
                break
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, self.Xpath_Address_City))
            )
        except TimeoutException:
            return False
        for i in range(0,7):
            self.PushText(self.Xpath_Address[i], str(self.user[i]))
        self.PushButton(self.Xpath_Address_next)
        return True

    def CheckoutPayment(self):
        while True:
            if self.driver.current_url == self.Url_Payment:
                break
        time.sleep(2)
        self.PushButton(self.Xpath_Payment_next)
        input("s")
        return True

    def CheckoutFinally(self):
        while True:
            self.OldUrl = self.driver.current_url
            if self.driver.current_url == self.Url_Finally:
                self.PushButton(self.Xpath_finally_next)
                break

        return True

    def SendMail(self):
        while True:
            if self.OldUrl != self.driver.current_url:
                break
        SendMessage(self.WebHook,self.ProductUrl,"0")
        return True

def main():
    if len(sys.argv) == 2:
        URL = sys.argv[1]
        print("Url ausgelesen: "+sys.argv[1])
        a = Tab.__init__("Alexander.genenger@hotmail.de","test","Alexander","Genenger","41065","Mönchengladbach","Bungtstraße","52",10,URL,"https://discord.com/api/webhooks/897429754439942185/0Al9O5kR1GTrXpckcBQr0vF9e-ngGNBnE6X5hKCxV88yeC_pdqsWzYvs1Q5jiMc1KPPU")
        a.main()
