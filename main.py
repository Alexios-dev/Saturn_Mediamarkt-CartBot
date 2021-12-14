import datetime
import random
import time

import bs4
import selenium
import requests
import os
import sys
from discordwebhook import Discord
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ForwardedEmail = []
ThreadsTab = []
Tabs = []

while True:
    try:
        with open("CardData.txt",'r') as file:
            a = file.readlines()
            Kartennummer    = str(a[1])
            Ablaufdatum     = str(a[3])
            Kartpruefnummer = str(a[5])
            Karteninhaber   = str(a[7])
        break
    except:
        print('__Pls enter__')
        Kartennummer = input("Card number:")
        Ablaufdatum = input("Expiration date:")
        Kartpruefnummer = input("Card verification number:")
        Karteninhaber = input("Cardholder name:")
        with open("CardData.txt",'w') as file:
            file.write(
                'Card number:\n'
                ''+Kartennummer+'\n'
                'Expiration date\n'
                ''+Ablaufdatum+'\n'
                'Card verification number\n'
                ''+Kartpruefnummer+'\n'
                'Cardholder name:\n'
                ''+Karteninhaber+'\n'
                       )


def SendMessage(DC_Url,Mediamarkt_Url,Cost):
    webhook = Discord(url=DC_Url)
    webhook.post(embeds=[{"title": "Ps5 drop", "description": "Ps5 drop by: "+Mediamarkt_Url+" Cost:"+str(Cost)}],)

class Tab():
    def __init__(self,email,password, vorname, nachname, plz, stadt, straße, hausnummer,telefonnummer, carting,productUrl,productId,webHook,geburtsdatum,payments):
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
        self.Telefonnummer = telefonnummer
        self.ProductId = productId
        self.Geburtsdatum = geburtsdatum
        self.Payments = payments
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

        while True:
            self.OpenTab()

            a = self.Carting()
            if a == 'OOS':
                return 'OOS'
            elif a == True:
                return 'INC'
            elif a == 'RE':
                pass
            self.driver.close()
            time.sleep(2)

    def OpenTab(self):
        from selenium import webdriver
        from fake_useragent import UserAgent
        ua = UserAgent()
        self.useragent = ua['Firefox']
        options = webdriver.FirefoxOptions()
        options.headless = False
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("general.useragent.override", self.useragent+"")
        self.profile.set_preference('useAutomationExtension', False)
        self.profile.update_preferences()
        while True:
            try:
                self.driver = webdriver.Firefox(executable_path='geckodriver.exe', options=options,firefox_profile=self.profile)
                self.driver.get('https://www.mediamarkt.de')
                self.profile.set_preference('useAutomationExtension', False)
                self.profile.update_preferences()
                while True:
                    time.sleep(0.5)
                    try:
                        if 'Media' in self.driver.page_source:
                            break
                        if 'Alle zulassen' in self.driver.page_source:
                            self.driver.find_element('xpath', '//*[@id="privacy-layer-accept-all-button"]').click()
                    except:
                        pass
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
        javaScriptbuy =r'''
            fetch("https://www.mediamarkt.de/api/v1/graphql", {
    "credentials": "include",
    "headers": {
        "User-Agent": "'''+self.useragent+'''",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "content-type": "application/json",
        "apollographql-client-name": "pwa-client",
        "apollographql-client-version": "1.58.0",
        "x-operation": "AddProduct",
        "x-flow-id": "c879e121-92f4-42cf-8620-a13a2ff79d02",
        "x-cacheable": "false",
        "x-mms-language": "de",
        "x-mms-country": "DE",
        "x-mms-salesline": "Media",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "'''+self.ProductUrl+'''",
    "body": "{\\"operationName\\":\\"AddProduct\\",\\"variables\\":{\\"items\\":[{\\"productId\\":\\"'''+self.ProductId+'''\\",\\"outletId\\":null,\\"quantity\\":1,\\"serviceId\\":null,\\"warrantyId\\":null}]},\\"extensions\\":{\\"persistedQuery\\":{\\"version\\":1,\\"sha256Hash\\":\\"404e7401c3363865cc3d92d5c5454ef7d382128c014c75f5fc39ed7ce549e2b9\\"},\\"pwa\\":{\\"salesLine\\":\\"Media\\",\\"country\\":\\"DE\\",\\"language\\":\\"de\\"}}}",
    "method": "POST",
    "mode": "cors"
});
        '''
        javaScriptClear = '''
            fetch("https://www.mediamarkt.de/api/v1/graphql", {
    "credentials": "include",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "content-type": "application/json",
        "apollographql-client-name": "pwa-client",
        "apollographql-client-version": "1.58.0",
        "x-operation": "CancelLineItem",
        "x-flow-id": "c9fa69dd-2eb6-4a63-9c7e-800da85037a9",
        "x-cacheable": "false",
        "x-mms-language": "de",
        "x-mms-country": "DE",
        "x-mms-salesline": "Media",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "https://www.mediamarkt.de/checkout",
    "body": "{\\"operationName\\":\\"CancelLineItem\\",\\"variables\\":{\\"itemId\\":\\"'''+self.ProductId+'''\\",\\"productType\\":\\"MMS\\"},\"extensions\\":{\\"persistedQuery\\":{\\"version\\":1,\\"sha256Hash\\":\\"dff62c500eb428450c259dcd855d3c9ba82adbfa3e4571ff2e39b631c6154283\\"},\\"pwa\\":{\\"salesLine\\":\\"Media\",\\"country\\":\\"DE\\",\\"language\\":\\"de\\"}}}",
    "method": "POST",
    "mode": "cors"
});
        '''

        javaScriptcheckout = '''
            fetch("https://www.mediamarkt.de/api/v1/graphql", {
    "credentials": "include",
    "headers": {
        "User-Agent": "'''+self.useragent+'''",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "content-type": "application/json",
        "apollographql-client-name": "pwa-client",
        "apollographql-client-version": "1.58.0",
        "x-operation": "SetAddress",
        "x-flow-id": "8dc3fc1c-5f72-4aa3-828a-688772872177",
        "x-cacheable": "false",
        "x-mms-language": "de",
        "x-mms-country": "DE",
        "x-mms-salesline": "Media",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "https://www.mediamarkt.de/checkout/address",
    "body": "{\\"operationName\\":\\"SetAddress\\",\\"variables\\":{\\"billing\\":{\\"salutation\\":\\"MR\\",\\"firstname\\":\\"'''+self.Vorname+'''\\",\\"lastname\\":\\"'''+self.Nachname+'''\\",\\"zipcode\\":\\"'''+self.PLZ+'''\\",\\"city\\":\\"'''+self.Stadt+'''\\",\\"street\\":\\"'''+self.Straße+'''\\",\\"houseNumber\\":\\"'''+self.Hausnummer+'''\\",\\"country\\":\\"DE\\"},\\"customer\\":{\\"birthdate\\":null,\\"companyName\\":null,\\"companyTaxId\\":null,\\"customerTaxId\\":null,\\"businessRelationship\\":\\"B2C\\",\\"email\\":\\"'''+self.Email+'''\\",\\"phoneNumber\\":null},\\"shipping\\":{\\"salutation\\":\\"MR\\",\\"country\\":\\"DE\\",\\"zipcode\\":\\"'''+self.PLZ+'''\\",\\"firstname\\":\\"'''+self.Vorname+'''\\",\\"lastname\\":\\"'''+self.Nachname+'''\\",\\"city\\":\\"'''+self.Stadt+'''\\",\\"street\\":\\"'''+self.Straße+'''\\",\\"houseNumber\\":\\"'''+self.Hausnummer+'''\\"}},\\"extensions\\":{\\"persistedQuery\\":{\\"version\\":1,\\"sha256Hash\\":\\"ee8cfe3d90ec50c8cf41f33e4f080a353a9db21a074595c4695c72e120d5ae38\\"},\\"pwa\\":{\\"salesLine\\":\\"Media\\",\\"country\\":\\"DE\\",\\"language\\":\\"de\\"}}}",
    "method": "POST",
    "mode": "cors"
});
        '''
        JavascriptcheckoutRechnung1 = '''
            fetch("https://www.mediamarkt.de/api/v1/graphql?operationName=GetBasket&variables=%7B%22isThankYouPage%22%3Afalse%2C%22isSummaryPage%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22ce1899b08d79c91b699b033faf3da2d3fa1e065f0689ad55252c9e885f6fc0c8%22%7D%2C%22pwa%22%3A%7B%22salesLine%22%3A%22Media%22%2C%22country%22%3A%22DE%22%2C%22language%22%3A%22de%22%7D%7D", {
    "credentials": "include",
    "headers": {
        "User-Agent": "'''+self.useragent+'''",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "content-type": "application/json",
        "apollographql-client-name": "pwa-client",
        "apollographql-client-version": "1.58.0",
        "x-operation": "GetBasket",
        "x-flow-id": "10e8950c-5a50-4ff0-ab51-44bf65d7e0d9",
        "x-cacheable": "false",
        "x-mms-language": "de",
        "x-mms-country": "DE",
        "x-mms-salesline": "Media",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "https://www.mediamarkt.de/checkout/summary",
    "method": "GET",
    "mode": "cors"
});
        '''
        JavascriptcheckoutRechnung2 = '''
            await fetch("https://www.mediamarkt.de/api/v1/graphql", {
    "credentials": "include",
    "headers": {
        "User-Agent": "'''+self.useragent+'''",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "content-type": "application/json",
        "apollographql-client-name": "pwa-client",
        "apollographql-client-version": "1.58.0",
        "x-operation": "UpdateSelectedPayment",
        "x-flow-id": "7422bb89-e3c6-45c4-b8d8-ef8a9bf77bab",
        "x-cacheable": "false",
        "x-mms-language": "de",
        "x-mms-country": "DE",
        "x-mms-salesline": "Media",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "referrer": "https://www.mediamarkt.de/checkout/summary",
    "body": "{\"operationName\":\"UpdateSelectedPayment\",\"variables\":{},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"4e3282c96e98cfc5e04d7b367bc43220f179be82a578e6a36dd47448013492a2\"},\"pwa\":{\"salesLine\":\"Media\",\"country\":\"DE\",\"language\":\"de\"}}}",
    "method": "POST",
    "mode": "cors"
});
        '''
        if 'Alle zulassen' in self.driver.page_source:
            self.driver.find_element('xpath','//*[@id="privacy-layer-accept-all-button"]').click()
        self.driver.get('https://www.mediamarkt.de/checkout')
        time.sleep(0.5)
        waitfor = 5
        d = 0
        while True:
            d = d+1
            while True:
                time.sleep(0.3)
                try:
                    if 'Media' in self.driver.page_source:
                        break
                except:
                    pass
            a = self.driver.execute_script(javaScriptbuy)
            time.sleep(0.5)
            self.driver.get('https://www.mediamarkt.de/checkout')
            while True:
                time.sleep(0.3)
                try:
                    if 'Media' in self.driver.page_source:
                        break
                except:
                    pass
            if self.ProductId in self.driver.page_source:
                print("Product in Cart")
                break
            elif waitfor == d:
                #return 'OOS'
                try:
                    self.driver.find_element('xpath',
                                             '/html/body/div[1]/div[3]/div[3]/div[1]/div/div/div/div/button').click
                    return 'RE'
                except:
                    pass



        self.profile.set_preference('useAutomationExtension', False)
        self.profile.update_preferences()
        time.sleep(1)
        if 'Alle zulassen' in self.driver.page_source:
            self.driver.find_element('xpath','//*[@id="privacy-layer-accept-all-button"]').click()
        self.driver.refresh()
        f = 0
        while True:
            a = self.driver.execute_script(javaScriptcheckout)
            time.sleep(0.5)
            self.driver.get('https://www.mediamarkt.de/checkout/address')
            while True:
                time.sleep(0.3)
                if 'Lieferung' in self.driver.page_source:
                    f = 1
                    break
            if f == 1:
                break
        a = self.driver.execute_script(JavascriptcheckoutRechnung1)
        time.sleep(0.5)
        self.driver.get('https://www.mediamarkt.de/checkout/summary')
        time.sleep(0.5)
        self.driver.refresh()
        while True:
            time.sleep(0.5)
            try:
                if 'Media' in self.driver.page_source:
                    break
            except:
                pass
        s = 0
        time.sleep(0.3)
        while True:
            time.sleep(0.3)
            try:
                self.driver.find_element('xpath', "//*[contains(text(), 'Kreditkarte')]")

                break
            except:
                pass

        if 'Alle zulassen' in self.driver.page_source:
            self.driver.find_element('xpath','//*[@id="privacy-layer-accept-all-button"]').click()
        time.sleep(0.3)

        if 'payment-selection-PAYONINVOICE' in self.driver.page_source and self.Payments == 1:
            s = 1
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[5]/div/div[1]/div[6]/div/div/div/div/div[1]/div/span').click()
            time.sleep(0.3)
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        elif 'payment-selection-PAYONINVOICE' in self.driver.page_source and self.Payments == 1:
            s = 3
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[5]/div/div[1]/div[1]/div/div/div/div/div[1]').click()
            time.sleep(0.3)
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        elif 'StyledCard' in self.driver.page_source and self.Payments == 1:
            s = 2
            self.driver.find_element('xpath',
                                     "//*[contains(text(), 'Kreditkarte')]").click()
            time.sleep(0.3)
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        if 'StyledCard' in self.driver.page_source and self.Payments == 2:
            s = 2
            if 'Zusammenfassung' in self.driver.page_source:
                try:
                    self.driver.find_element('xpath','/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button')
                except:
                    pass
            self.driver.find_element('xpath',
                                     "//*[contains(text(), 'Kreditkarte')]").click()
            time.sleep(0.3)
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        elif 'payment-selection-PAYONINVOICE' in self.driver.page_source and self.Payments == 2:
            s = 3
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[5]/div/div[1]/div[1]/div/div/div/div/div[1]').click()
            time.sleep(0.3)
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        elif 'payment-selection-PAYONINVOICE' in self.driver.page_source and self.Payments == 2:
            s = 1
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[5]/div/div[1]/div[6]/div/div/div/div/div[1]/div/span').click()
            time.sleep(0.3)
            self.driver.find_element('xpath',
                                     '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        try:
            self.driver.find_element('xpath', '/html/body/div[1]/div[3]/div[3]/div[1]/div/div/div/div/button').click
            return 'RE'
        except:
            pass
        while True:
            time.sleep(0.3)
            try:
                if 'Zusammenfassung' in self.driver.page_source:
                    break
            except:
                pass

        time.sleep(0.5)
        while True:
            time.sleep(0.3)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button')
                break
            except:
                pass
        self.driver.find_element('xpath',
                                 '/html/body/div[1]/div[3]/div[3]/div[1]/div/div[2]/div/div[8]/div/div/div/div/div[4]/div/button').click()
        time.sleep(0.5)
        try:
            self.driver.find_element('xpath', '/html/body/div[1]/div[3]/div[3]/div[1]/div/div/div/div/button').click
            return 'RE'
        except:
            pass
        if s == 1:
            while True:
                try:
                    self.driver.find_element('xpath','//*[@id="mat-input-0"]')
                    break
                except:
                    pass
            self.driver.find_element('xpath', '//*[@id="mat-input-0"]').send_keys(self.Geburtsdatum)
            self.driver.find_element('xpath','//*[@id="mat-input-1"]').send_keys(self.Telefonnummer)
            self.driver.find_element('xpath','/html/body/checkout-root/checkout-pages-show-wrapper/checkout-main-wrapper/checkout-main-layout/pe-layout-app/div/div/div/div[3]/pe-layout-content/div/div/div/div[2]/div/div/mat-accordion[1]/mat-expansion-panel[1]/div/div/div/div/checkout-main-selector-show/div/checkout-main-choose-payment-method/div/section-choose-payment-method/section-choose-payment/div/div[1]/div/div/div/div[3]/div/lazy-payments-step-first-santander-invoice-de/div/santander-invoice-de-inquiry-container/santander-invoice-de-shared-form/form/div[2]/pe-form-fieldset/div/div/div[2]/div').click()
        if s == 2:
            while True:
                try:
                    self.driver.find_element('xpath','//*[@id="MMSKKNr"]')
                    break
                except:
                    pass
            self.driver.find_element('xpath','//*[@id="MMSKKNr"]').send_keys(Kartennummer)
            self.driver.find_element('xpath','//*[@id="MMSExpiry"]').send_keys(Ablaufdatum)
            self.driver.find_element('xpath','//*[@id="MMSCCCVC"]').send_keys(Kartpruefnummer)
            self.driver.find_element('xpath','//*[@id="MMScreditCardHolder"]').send_keys(Karteninhaber)
            while True:
                time.sleep(0.3)
                try:
                    self.driver.find_element('xpath','//*[@id="submitButton"]')
                    break
                except:
                    pass
            input("s")
            time.sleep(0.7)
            self.driver.find_element('xpath', '//*[@id="submitButton"]').click()
            test = 0
            while True:
                time.sleep(0.7)
                try:
                    if 'authorize this payment' in self.driver.page_source:
                        break
                except:
                    pass
            start = self.driver.current_url
            while True:
                if test == 0:
                    print("Carted wait for payment: "+self.ProductUrl)
                    start = self.driver.current_url
                    webhook = Discord(
                        url='https://discord.com/api/webhooks/912806361719525438/UeTYA14MG1CDec648mW6s1Kx_q6Emyl4fjFTecNuq1Xi7jBWwVNAqPuPKPvwWa869l1S')#authorize this payment
                    webhook.post(embeds=[
                        {
                            "author": {
                                "name": "" + str('Mediamarkt/Saturn') + "",
                                "description": str(self.driver.current_url) + "",
                                "url": self.driver.current_url,
                            },
                            "description": self.ProductUrl+"\n**[carted wait for payment. Price " + self.driver.find_element('xpath','/html/body/div/div[4]/div/div[2]/span[2]').text + "](" + self.driver.current_url + ")**",
                            "footer": {
                                "text": "Custom Monitor | XaliCooks | " + str(datetime.datetime.now().hour) + ":" + str(
                                    datetime.datetime.now().minute) + ":" + str(
                                    datetime.datetime.now().second) + " | *Affiliate Links",
                                "icon_url": "https://cdn.discordapp.com/attachments/652270149591760957/920071972640153651/LOGO.png"
                            },
                            "color": 559624,
                        }
                    ], )
                    test = 1
                if 'The payment has timed out' in self.driver and test == 1:
                    time.sleep(0.3)
                    print("Carted wait for payment: " + self.ProductUrl)
                    webhook = Discord(
                        url='https://discord.com/api/webhooks/912806361719525438/UeTYA14MG1CDec648mW6s1Kx_q6Emyl4fjFTecNuq1Xi7jBWwVNAqPuPKPvwWa869l1S')  # authorize this payment
                    webhook.post(embeds=[
                        {
                            "author": {
                                "name": "" + str('Mediamarkt/Saturn') + "",
                                "description": str(self.driver.current_url) + "",
                                "url": self.driver.current_url,
                            },
                            "description": self.ProductUrl + "\n**[Payment declined. Price " + self.driver.find_element(
                                'xpath',
                                '/html/body/div/div[4]/div/div[2]/span[2]').text + "](" + self.driver.current_url + ")**",
                            "footer": {
                                "text": "Custom Monitor | XaliCooks | " + str(datetime.datetime.now().hour) + ":" + str(
                                    datetime.datetime.now().minute) + ":" + str(
                                    datetime.datetime.now().second) + " | *Affiliate Links",
                                "icon_url": "https://cdn.discordapp.com/attachments/652270149591760957/920071972640153651/LOGO.png"
                            },
                            "color": 559624,
                        }
                    ], )
                    return 'CF'#Card Failed
                if self.driver.current_url != start and not 'The payment has timed out' in self.driver.page_source and test == 1:
                    webhook = Discord(
                        url='https://discord.com/api/webhooks/912806361719525438/UeTYA14MG1CDec648mW6s1Kx_q6Emyl4fjFTecNuq1Xi7jBWwVNAqPuPKPvwWa869l1S')  # authorize this payment
                    webhook.post(embeds=[
                        {
                            "author": {
                                "name": "" + str('Mediamarkt/Saturn') + "",
                                "description": str(self.driver.current_url) + "",
                                "url": self.driver.current_url,
                            },
                            "description": self.ProductUrl + "\n**[Carted.](" + self.driver.current_url + ")**",
                            "footer": {
                                "text": "Custom Monitor | XaliCooks | " + str(datetime.datetime.now().hour) + ":" + str(
                                    datetime.datetime.now().minute) + ":" + str(
                                    datetime.datetime.now().second) + " | *Affiliate Links",
                                "icon_url": "https://cdn.discordapp.com/attachments/652270149591760957/920071972640153651/LOGO.png"
                            },
                            "color": 559624,
                        }
                    ], )
                    exit()

            pass
        input("Wait")
        return True


#               email,password, vorname, nachname, plz, stadt, straße, hausnummer,telefonnummer, carting,productUrl,productId,webHook,geburtsdatum,payments
a = Tab("Alexander.genenger@hotmail.de","test","Alexander","Genenger","41065","Mönchengladbach","Bungtstraße","52",'017641794896',1,'https://www.mediamarkt.de/de/product/_microsoft-xbox-series-s-512-gb-2677359.html','2677359',"https://discord.com/api/webhooks/895695395718561862/ObjJ4zv4nuBTOx-N65GchrAnu3Rryw8THgUXlklr6FUfOS-l7XjpV7NDfeDxehybJBZ3",'03.03.2003',2)
print(a.main())
def main():
    s = 0
    try:
        URL = sys.argv[1]
        s = 1
    except:
        print("Not Enough Arguments")
    if s == 1:
        URL = sys.argv[1]
        Tabs.append(Tab("Alexander.genenger@hotmail.de","test","Alexander","Genenger","41065","Mönchengladbach","Bungtstraße","52",'017641794896',10,URL,"https://discord.com/api/webhooks/897429754439942185/0Al9O5kR1GTrXpckcBQr0vF9e-ngGNBnE6X5hKCxV88yeC_pdqsWzYvs1Q5jiMc1KPPU"))
        Tabs[0].main()
if __name__ == '__main__':
    main()
