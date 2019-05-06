#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options


class TwitterLogin(object):
    """docstring for TwitterLogin"""
    def __init__(self, arg):
        super(TwitterLogin, self).__init__()
        chrome_options = Options()
        chrome_options.add_argument("disable-infobars")

        # options.addArguments("disable-infobars");
        # WebDriver driver = new ChromeDriver(options);


        self.browser = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'), chrome_options=chrome_options)

        self.username = arg[0]
        self.password = arg[1]
        self.hastag = arg[2]

        self.login_url = "https://twitter.com/login/"
        self.search_url = "https://twitter.com/search?src=typd&q={0}".format(arg[2])

    def user_auth(self):
        self.browser.get(self.login_url)

        username = self.browser.find_element_by_css_selector('.js-username-field')
        password = self.browser.find_element_by_css_selector('.js-password-field')
        

        username.send_keys(self.username)
        password.send_keys(self.password)

        try:
            self.browser.find_element_by_css_selector("button.submit").click()
            sleep(3)
            print("Login into twiiter as user {0}".format(self.username))
            self.follow_hastag_user()
        except Exception as e:

            print("""
                    ########################################################
                    Please pass as correct arguments username and password.
                    #######################################################
                """)
            self.browser.quit()


    def follow_hastag_user(self):
        query = self.browser.find_element_by_css_selector('input.search-input')
        query.send_keys(self.hastag)
        query.submit()

        sleep(5)

        hastag_tweet = self.browser.find_elements_by_css_selector('li.stream-item div.stream-item-header a.js-action-profile')
        
        for index in range(len(hastag_tweet)):
            
            if index == 20: print("""
                Congrat's you are following {0} twitter user of using #{1}
                """.format(self.hastag, index+1 )); self.browser.back(); break;
            hastag_tweet[index].click()
            sleep(5)
        
            print("Twitter User Profile page..", self.browser.current_url)            
            
            try:
                self.browser.find_element_by_css_selector('ul.ProfileNav-list \
                    li.ProfileNav-item--userActions button.button-text.follow-text').click()
                print("New twitter user following  :: -->", self.browser.current_url)
            except Exception as e:
                print("Already following this user :: -->", self.browser.current_url)
                pass

            sleep(4)
            self.browser.back()
            sleep(4)
            hastag_tweet = self.browser.find_elements_by_css_selector('li.stream-item div.stream-item-header a.js-action-profile')

        print(""""
                #################################################
                    
                ######    Script successfully finished   ########
                
                #################################################
            """)



if __name__ == "__main__":
    if len(sys.argv[1:]) == 3:
        print("Script started....")
        t_loign = TwitterLogin(sys.argv[1:])
        t_loign.user_auth()
    else:
        print("""Username ,password and hashtag must required, example: 
                python twitter.py username password hashtag""")

