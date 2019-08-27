from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(4)

        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(4)

        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)

        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        time.sleep(2)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(3)

    # u cann't like most 300 photos per hour
    def like_photos(self, hashtag):

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/"+ hashtag +"/")
        time.sleep(4)

        # gahering photos
        pic_hrefs = []
        for i in range(1, 6):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)

                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')

                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]

                # building list of unique photos
                # store photos in pics_hrefs just one time
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(15,30))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
            except Exception:
                time.sleep(2)
            # Counting missing photos
            unique_photos -= 1
            print("Quantidade restante:" + str(unique_photos))

    # u cann't follow or unfollow most 60 ppl's per hour
    def follow_users(self, hashtags):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtags + "/")
        time.sleep(5)

        # gahering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)

                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')

                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]

                # building list of unique photos
                # store photos in pics_hrefs just one time
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # follow users by hashtag
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2.5)
            try:
                time.sleep(60)
                follow_button = lambda: driver.find_element_by_xpath("//button[@type='button']").click()
                follow_button().click()
            except Exception:
                time.sleep(2)
            unique_photos -= 1
            print("Missing Follows: " + str(unique_photos))

    # unfollow all users who do not follow your profile
    def unfollow_users(self, username):
        driver = self.driver
        time.sleep(3)
        driver.get("https://www.instagram.com/")

        # click on profile
        try:
            time.sleep(3)
            driver.find_element_by_xpath("//a[@href='/"+username+"/']").click()
        except Exception:
            print("Exception: Cann't click profile")
            time.sleep(5)

        #click on ours followers
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//a[@href='/"+username+"/followers/']").click()

            time.sleep(3)
            #FIND A WAY TO SCROLL DOWN
	    # SEE THE NEW CHANGES
	    # SEE THE NEW CHANGES 2
            #followers_on_view = driver.find_element_by_css_selector("div[role=\'dialog\'] ul")


            # get profile names
            profiles = []
            # finding profiles by tag
            profiles_in_view = driver.find_elements_by_tag_name('a')

            # getting all my followers profiles names
            profiles_in_view = [profile.get_attribute('title') for profile in profiles_in_view]

            # append name just one time
            [profiles.append(prof) for prof in profiles_in_view if prof not in profiles]

            time.sleep(3)
            print(profiles)
            # close window
            try:
                time.sleep(2)
                close_button = lambda: driver.find_element_by_xpath("//span[@aria-label='Close']").click()
                close_button().click()
            except Exception:
                print("Cann't close window!")
                time.sleep(2)

        except Exception:
            print("Exception: Cann't take profile names!")
            time.sleep(15)

        try:
            # click on following names
            time.sleep(3)
            driver.find_element_by_xpath("//a[@href='/" + username + "/following/']").click()

            time.sleep(2)
            #FIND A WAY TO SCROLL DOWN


            time.sleep(3)
            names = []
            # get name of people i follow
            follow_names = driver.find_elements_by_tag_name('a')

            # getting all names in store in vector
            follow_names = [name.get_attribute('title') for name in follow_names]

            # append name just one time
            [names.append(name) for name in follow_names if name not in names]
            print(names)
        except Exception:
            print("Cannot take following names!")
            time.sleep(15)


if __name__ == "__main__":

    username = "your login"
    password = "your password"

    ig = InstagramBot(username, password)
    ig.login()

    hashtags = ['greek', 'achilles', 'troy', 'atenas', 'medieval', 'warrior', 'history']

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            hashtags.remove(tag)
            ig.like_photos(tag)
            #ig.follow_users(tag)
            #ig.unfollow_users(username)
        except Exception:
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()
