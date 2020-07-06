# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import chromedriver_binary
import settings

# アカウント情報定義
fbAuthPass = settings.TinderAuth
fbMailXpath = "/html/body/div/div[2]/div[1]/form/div/div[1]/div/input"
fbPassXpath = "/html/body/div/div[2]/div[1]/form/div/div[2]/div/input"
fbLoginXpath = "/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input"
FbMail = settings.FacebookMail
FbPass = settings.FacebookPass

# ブラウザを開く。
driver = webdriver.Chrome()

# facebookアクセストークンを開く。
driver.get(fbAuthPass)

#　メール入力
mailField = driver.find_element_by_xpath(fbMailXpath)
mailField.send_keys(FbMail)

#　パスワード入力
passFirld = driver.find_element_by_xpath(fbPassXpath)
passFirld.send_keys(FbPass)
print("アカウント情報入力完了")

#　ログイン押下s
loginField = driver.find_element_by_xpath(fbLoginXpath)
loginField.click()
print("ログイン成功")

# tinderトップページ遷移
driver.execute_script("window.open()")
new_window = driver.window_handles[1]
driver.switch_to.window(new_window)
driver.get("https://tinder.com/app")
print("トップページ遷移完了")

# モーダル表示待ち
sleep(5)
# アカウントfacebookログイン
fbButton = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[2]/button")
fbButton.click()

driver.implicitly_wait(10)
notificationButtonXpath = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/button[1]")
notificationButtonXpath.click()
print("位置情報on")

driver.implicitly_wait(10)
notificationButtonXpath = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/button[1]")
notificationButtonXpath.click()
print("アラート表記on")

driver.implicitly_wait(10)
cookieAgreeButtonXpath = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[1]/button")
cookieAgreeButtonXpath.click()
print("cookie同意")

#  写真のロードまで待つ
driver.implicitly_wait(10)
targetImage = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div") 
i = 0
while targetImage:
    driver.implicitly_wait(5)
    # 右スワイプ
    try:
        likeButton = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button")
        likeButton.click()
        i += 1
        print(i, "件いいね完了")
        driver.implicitly_wait(5)
        targetImage = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div") 
        continue

    except Exception as e:
        try:
            addHomeButton = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/button[2]")
            addHomeButton.click()
            print("例外モーダルを処理")
            continue

        except Exception as e:
            driver.close()