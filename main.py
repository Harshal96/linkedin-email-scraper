from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# my code to load and save cookie from the driver
from cookies_library import load_cookie
import re

import time

"""
1. Launch Chrome
2. Go to https://linkedin.com
3. Load the cookie
    3.1. I have saved the cookie from https://linkedin.com beforehand; saves me the code to write login 
4. Open the post on LinkedIn
    4.1. I can now see all the comments because I am logged in (thanks to step 3)
"""
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://linkedin.com')
load_cookie(driver, 'linkedin_cookie')
driver.get('https://www.linkedin.com/posts/daminimalhotra_linkedin-helpinghands-personaldevelopment-activity'
           '-6673604745808240643-1PWI/')


# commenting while True: because there are a lot of comments
# while True:
for i in range(10):
    try:
        # .comments-comments-list__load-more-comments-button is the button to load more comments
        driver.find_element_by_css_selector(".comments-comments-list__load-more-comments-button").click()
        # give linkedin.com time to load - so slow
        time.sleep(2)
    except Exception:
        # for the case when you are using while True:
        # breaks when there are no more comments i.e. the CSS class mentioned above
        break


# get the div with all the comments
comments_div = driver.find_element_by_css_selector(".comments-comments-list").get_attribute("innerHTML")


# file to store the emails found; delimeter: \n
with open("emails.txt", "w") as file:
    emails_list = []

    # regex to find all the emails from the div
    # set() to only store the unique ones
    for email in set(re.findall(r'[\w.-]+@[\w.-]+\.\w+', comments_div)):

        # code to mask the email ids
        index = str(email).index("@")
        email_list = list(email)
        for i in range(1, int(index / 2)):
            email_list[index - i] = "*"
        emails_list.append("".join(email_list))
    file.write("\n".join(emails_list))
