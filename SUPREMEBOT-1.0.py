from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import requests
import os

# main class
class supremeBot:
    
    def __init__(self):

        # gets the account details for the bot
        with open("checkoutdetails.txt", "r") as f:
            usersettings = f.readlines()
            self.usersettings = usersettings
            usersettings = [setting.split("= ")[1].replace("\n", "") for setting in usersettings]
            
        self.name = str(usersettings[0])
        self.email = str(usersettings[1])
        self.telephone = str(usersettings[2])
        self.address = str(usersettings[3])
        self.city = str(usersettings[4])
        self.postcode = str(usersettings[5])
        self.country = str(usersettings[6])
        self.type = str(usersettings[7])[:2]
        self.cardnum = str(usersettings[8])
        self.month = str(usersettings[9])
        self.year = str(usersettings[10])
        self.cvv = str(usersettings[11])


    # logs in using the credentials from pastebin
    def login(self):
        
        status = True
        while status:
            InputUsername = input("Please input your username: ")
            InputPassword = str(input("Please input your password: "))
            
            passwordPaste = "https://pastebin.com/raw/V44yEAfT"
            # gets the text from the raw page of pastebin
            r = requests.get(passwordPaste)
            lines = r.text
            lines = lines.split("\n")
            for line in lines:
                line = line.split(", ")
                username = line[0].replace("\r", "")
                password = line[1].replace("\r", "")
                # if both are correct start the browser
                if username == InputUsername and password == InputPassword:
                    print("Welcome\n")
                    profile = webdriver.FirefoxProfile()
                    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    profile.set_preference("general.useragent.override", user_agent)
                    self.driver = webdriver.Firefox(profile)
                    status = False
            # otherwise keep asking
            if status == True:
                print("Incorrect or Invalid username or password")
                print("Retry\n")

    # waits until the start of a new minute
    def wait(self, minute):
        notTime = True
        oldSecond = 0
        while notTime:

            currentTime = time.localtime()
            currentMinute = int(time.strftime("%M", currentTime))
            currentSecond = int(time.strftime("%S", currentTime))
            if currentMinute == minute:
                notTime = False
            # print ever new second
            if currentSecond != oldSecond:
                print(currentMinute, currentSecond)
                oldSecond = currentSecond

    # finds each item and adds to cart
    def findItem(self):

        bought = 0
        for i in range(len(self.items)):
            item = self.items[i]
            self.category = str(item[0]).lower()
            self.itemname = str(item[1])
            self.colour = str(item[2]).title()
            self.colour2 = str(item[3]).title()
            self.size = str(item[4]).title().replace("Xl", "XL")
            self.size2 = str(item[5]).title().replace("Xl", "XL")
            self.type = str(item[6]).title()

            if self.type == "False" or (bought == 0 and i == len(items)-1):

                # opens the correct store page with the right category
                self.driver.get("https://www.supremenewyork.com/shop/all/" + self.category)
                self.driver.implicitly_wait(5)
                

                # clicks on the item if it can find it
                try:
                    self.driver.find_element_by_partial_link_text(self.itemname).click()
                    self.driver.implicitly_wait(5)
                except:
                    print("Item name", self.itemname, "not found")
                    continue
                
                # clicks on the correct colour
                colourFound = False
                try:
                    colour = self.driver.find_element_by_xpath("//a[@data-style-name='" + self.colour + "']")
                    #if sold out atribute is false that means its not sold out so pick that one
                    if colour.get_attribute("data-sold-out") == "false":
                        colour.click()
                        self.driver.implicitly_wait(5)
                        colourFound = True
                except:
                    pass
                # otherwise try colour two
                try:
                    if colourFound == False:
                        colour = self.driver.find_element_by_xpath("//a[@data-style-name='" + self.colour2 + "']")
                        if colour.get_attribute("data-sold-out") == "false":
                            colour.click()
                            self.driver.implicitly_wait(5)
                        else:
                            print(self.itemname, "doesnt have your colours")
                            continue
                except:
                    pass

                # select size
                if self.size != "Na":
                    # get all avaliable sizes
                    sizes = self.driver.find_elements_by_xpath("//select[@id='size']//*")
                    sizes = [size.text for size in sizes]
                    if self.size in sizes:
                        # click on drop down then select correct size
                        self.driver.find_element_by_xpath("//select[@id='size']").click()
                        self.driver.find_element_by_xpath("//select[@id='size']//option[contains(text(), '" + self.size + "')]").click()
                        # add to basket
                        self.driver.find_element_by_xpath("//input[@value='add to basket']").click()
                        bought += 1
                    elif self.size2 in sizes:
                        self.driver.find_element_by_xpath("//select[@id='size']").click()
                        self.driver.find_element_by_xpath("//select[@id='size']//option[contains(text(), '" + self.size2 + "')]").click()
                        # add to basket
                        self.driver.find_element_by_xpath("//input[@value='add to basket']").click()
                        bought += 1    
                    else:
                        print(self.itemname, "doesnt have your size")

                if i == len(self.items)-1 or (i == len(self.items)-2 and str(self.items[len(self.items)-1][6]).title() == "True"):
                    # if last item checkout
                    self.driver.find_element_by_xpath("//a[@class='button checkout']").click()
                    self.driver.implicitly_wait(5)

    # checks out and enters details
    def checkout(self):
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='full name']")
        element.send_keys(self.name)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='email']")
        element.send_keys(self.email)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='tel']")   
        element.send_keys(self.telephone)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='address']")
        element.send_keys(self.address)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='city']")
        element.send_keys(self.city)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='postcode']")
        element.send_keys(self.postcode)
        
        #element = self.driver.find_element_by_xpath("//select[@id='order_billing_country']")
        #element.send_keys(self.country)
        
        element = self.driver.find_element_by_xpath("//select[@id='credit_card_type']")
        element.send_keys(self.type)
        element.send_keys(Keys.RETURN)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='number']")
        element.send_keys(self.cardnum)
        
        element = self.driver.find_element_by_xpath("//select[@id='credit_card_month']")
        element.send_keys(self.month)
        
        element = self.driver.find_element_by_xpath("//select[@id='credit_card_year']")
        element.send_keys(self.year)
        
        element = self.driver.find_element_by_xpath("//input[@placeholder='CVV']")
        element.send_keys(self.cvv)

        self.driver.find_element_by_xpath("//*[contains(text(), 'I have read and agree to the ')]").click()

        self.driver.find_element_by_xpath("//input[@value='process payment']").click()

    # updater function with google drive and pastebin
    def update(self):
        # gets the most recent versions download link and version
        r = requests.get("https://pastebin.com/raw/uAD25kVX")
        lines = r.text.split("\n")
        url = lines[0]
        version = lines[1]
        # gets current version from program name
        filenames = os.listdir()
        filename = [filename for filename in filenames if "SUPREME" in filename][0]
        currentVersion = filename.split("-")[1].replace(".exe", "").replace(".py", "")
        if version != currentVersion:
            print("Wrong version, updating")
            r = requests.get(url, allow_redirects=True)
            newName = "SUPREMEBOT-" + version + ".exe"
            # gets data from download page and writes to exe file
            with open(newName, "wb") as f:
                f.write(r.content)
            print("Updated, run new program and delete this one")
            time.sleep(10)
            quit()
        else:
            print("Version", version, "is all up to date")

    # gets the details of all the wanted items
    def getItemDetails(self):

        with open("itemdetails.txt", "r") as f:
            settings = f.readlines()
            self.items = []
            newItem = False
            item = []
            for line in settings:
                if newItem == True and "***" not in line:
                    item.append(line.split("= ")[1].replace("\n", ""))
                if "***" in line and newItem == False:
                    newItem = True
                elif "***" in line and newItem == True:
                    self.items.append(item)
                    item = []
                    
bot = supremeBot()
bot.update()
bot.getItemDetails()
bot.login()
mins = int(input("Time you want it to buy items at, the mins: "))
bot.wait(mins)
startTime = time.time()
bot.findItem()
bot.checkout()
endTime = time.time()
print("That took", endTime-startTime, "second")
