import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import pandas as pd

from helpers import configure_webdriver

def find_posts(driver):
    try:
        actions = ActionChains(driver)
        scraped_jobs:List[dict] = []
        posts = driver.find_elements(By.CLASS_NAME, "card-contain")
        for post in posts:
            try:
                data: dict = {}
                data['username'] = post.text.split('\n')[1]
                time.sleep(1)
                social_media = post.find_elements(By.TAG_NAME, "a")
                for media in social_media:
                    if 'instagram' in media.get_attribute('href'):
                        actions.move_to_element(media).perform()
                        social_media = post.find_elements(By.TAG_NAME, "a")
                        for s_media in social_media:
                            if 'instagram' in s_media.get_attribute('href'):
                                data['followers'] = s_media.text
                                break
                if not "K" in data["followers"] and float(data['followers'].split("K")[0]) >= 10 and float(data['followers'].split("K")[0]) <= 200:
                    data: dict = {}
                    continue
                data['engagement_rate'] = post.find_element(By.CLASS_NAME, "font-bold").text
                scraped_jobs.append(data.copy())
            except Exception as e:
                print(e)
            break
        df = pd.DataFrame(scraped_jobs)
        df.to_excel("instagram_accounts_info.xlsx", index=False)
    except Exception as e:
        print(e)

def load_posts(driver, count):
    try:
        time.sleep(3)
        posts = driver.find_elements(By.CLASS_NAME, "card-contain")
        posts_count = len(posts)
        if posts_count != count and posts_count >= count:
            for post in posts:
                post.location_once_scrolled_into_view
            return True
        else:
            return False
    except:
        pass


def instagram():
    print("Instagram")
    try:
        driver = configure_webdriver(True)
        driver.maximize_window()
        try:
            flag = True
            count = 0
            driver.get("https://grand-community.com/en/dashboard/$brand/influencers")
            import pdb
            pdb.set_trace()
            while flag:
                load_posts(driver, count)
            find_posts(driver)
        except Exception as e:
            print(e)
        finally:
            driver.quit()
    except Exception as e:
        print(e)

instagram()