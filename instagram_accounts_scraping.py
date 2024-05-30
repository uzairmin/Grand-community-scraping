import time
from typing import List
from selenium.webdriver.common.by import By
import pandas as pd
from helpers import configure_webdriver
import os

def find_posts(driver, scraped_jobs, count):
    try:
        driver.get(f"https://grand-community.com/en/dashboard/$brand/influencers/{ count }")
        time.sleep(2)
        data: dict = {}
        data["username"] = "N/A"
        data["description"] = "N/A"
        data["interests"] = "N/A"
        data["instagram_followers"] = "N/A"
        data["tiktok_followers"] = "N/A"
        data["engagement_rate"] = "N/A"
        data["instagram_following"] = "N/A"
        data["tiktok_following"] = "N/A"
        data["instagram_uploads"] = "N/A"
        data["tiktok_uploads"] = "N/A"
        data["views_count"] = "N/A"
        
        data['username'] = driver.find_element(By.TAG_NAME, "h2").text
        data['description'] = driver.find_element(By.TAG_NAME, "p").text
        data['interests'] = driver.find_elements(By.CLASS_NAME, "direction")[0].text.strip("Intrest\n").replace("\n", ", ")
        social_media = driver.find_elements(By.CLASS_NAME, "v-chip--clickable")
        for media in social_media:
            if 'instagram' in media.text.lower():
                media.click()
                time.sleep(2)
                insta = driver.find_elements(By.TAG_NAME, "strong")
                data['instagram_followers'] = insta[0].text
                data['instagram_following'] = insta[1].text
                data['instagram_uploads'] = insta[2].text
                data['engagement_rate'] = insta[3].text
                try:
                    views = driver.find_elements(By.TAG_NAME, "h3")
                    view_count = []
                    for i, view in enumerate(views):
                        if i == 0 or i % 2 == 0:
                            view_count.append(view.text)
                    result_string = ", ".join(view_count)
                    data["views_count"] = str(result_string)
                except:
                    data["views_count"] = "N/A"

            elif 'tiktok' in media.text.lower():
                media.click()
                time.sleep(2)
                tiktok = driver.find_elements(By.TAG_NAME, "strong")
                data['tiktok_followers'] = tiktok[0].text
                data['tiktok_following'] = tiktok[1].text
                data['tiktok_uploads'] = tiktok[2].text
        
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
            while count < 5000:
                count+=1
                print(count)
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