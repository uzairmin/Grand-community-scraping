import time
from typing import List
from selenium.webdriver.common.by import By
import pandas as pd
from helpers import configure_webdriver
import os

def find_posts(driver, scraped_jobs, count):
    try:
        driver.get(f"https://grand-community.com/en/dashboard/$brand/influencers/{ count }")
        time.sleep(1)
        data: dict = {}
        data["username"] = "N/A"
        data["interests"] = "N/A"
        data["instagram_followers"] = "N/A"
        data["tiktok_followers"] = "N/A"
        data["engagement_rate"] = "N/A"
        
        data['username'] = driver.find_element(By.TAG_NAME, "h2").text
        data['interests'] = driver.find_elements(By.CLASS_NAME, "direction")[0].text.strip("Intrest\n").replace("\n", ", ")
        social_media = driver.find_elements(By.CLASS_NAME, "v-chip--clickable")
        for media in social_media:
            if 'instagram' in media.text.lower():
                media.click()
                time.sleep(1)
                data['instagram_followers'] = driver.find_element(By.TAG_NAME, "strong").text
                data['engagement_rate'] = driver.find_elements(By.TAG_NAME, "strong")[3].text

            elif 'tiktok' in media.text.lower():
                media.click()
                time.sleep(1)
                data['tiktok_followers'] = driver.find_element(By.TAG_NAME, "strong").text
        
        scraped_jobs.append(data.copy())

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
            count = 0
            scraped_jobs:List[dict] = []
            driver.get("https://grand-community.com/en/dashboard/$brand/influencers")
            import pdb
            pdb.set_trace()
            while count < 50000:
                count+=1
                find_posts(driver, scraped_jobs, count)
                if count % 100 == 0:
                    df = pd.DataFrame(data=scraped_jobs)
                    filename = "scraped-data.xlsx"
                    if os.path.exists(filename):
                        existing_df = pd.read_excel(filename, na_filter=False)
                        df = pd.concat([existing_df, df], ignore_index=True)
                    else:
                        df = df
                
                    df.to_excel(filename, index=False)
                    scraped_jobs:List[dict] = []
        except Exception as e:
            print(e)
        finally:
            driver.quit()
    except Exception as e:
        print(e)

instagram()