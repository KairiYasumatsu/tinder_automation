# coding:utf-8
import emoji
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import process_time, sleep
import chromedriver_binary
import settings

# アカウント情報定義
fbAuthPass = settings.TinderAuth
fbMailXpath = "/html/body/div/div[2]/div[1]/form/div/div[1]/div/input"
fbPassXpath = "/html/body/div/div[2]/div[1]/form/div/div[2]/div/input"
fbLoginXpath = "/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input"
FbMail = settings.FacebookMail
FbPass = settings.FacebookPass

class tinder:
    def __init__(self):
        # ブラウザを開く。
        self.driver = webdriver.Chrome()

    def login(self):
        # facebookアクセストークンを開く。
        self.driver.get(fbAuthPass)

        #　メール入力
        mailField = self.driver.find_element_by_xpath(fbMailXpath)
        mailField.send_keys(FbMail)

        #　パスワード入力
        passFirld = self.driver.find_element_by_xpath(fbPassXpath)
        passFirld.send_keys(FbPass)
        print("アカウント情報入力完了")

        #　ログイン押下s
        loginField = self.driver.find_element_by_xpath(fbLoginXpath)
        loginField.click()
        print("ログイン成功")

        # tinderトップページ遷移
        self.driver.execute_script("window.open()")
        new_window = self.driver.window_handles[1]
        self.driver.switch_to.window(new_window)
        self.driver.get("https://tinder.com/app")
        print("トップページ遷移完了")

        # モーダル表示待ち
        sleep(5)
        # アカウントfacebookログイン
        fbButton = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[2]/button")
        fbButton.click()

        self.driver.implicitly_wait(10)
        notificationButtonXpath = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/button[1]")
        notificationButtonXpath.click()
        print("位置情報on")

        self.driver.implicitly_wait(10)
        notificationButtonXpath = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/button[1]")
        notificationButtonXpath.click()
        print("アラート表記on")

        self.driver.implicitly_wait(10)
        cookieAgreeButtonXpath = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[1]/button")
        cookieAgreeButtonXpath.click()
        print("cookie同意")

    def autoSwipe(self, login):
        login()
        #  写真のロードまで待つ
        self.driver.implicitly_wait(10)
        targetImage = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div") 
        i = 0
        while targetImage:
            self.driver.implicitly_wait(5)
            # 右スワイプ
            try:
                likeButton = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button")
                likeButton.click()
                i += 1
                print(i, "件いいね完了")
                self.driver.implicitly_wait(5)
                targetImage = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div") 
                continue

            except Exception as e:
                try:
                    addHomeButton = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/button[2]")
                    addHomeButton.click()
                    print("例外モーダルを処理")
                    continue

                except Exception as e:
                    self.driver.close()

    def autoMessage(self, login):
        login()
        i = 2

        # 直近のマッチを50件取得
        while i < 50:
            # 2秒まっってみる
            sleep(2)
            # 次のマッチを取得
            matchedXpath = "/html/body/div[1]/div/div[1]/div/aside/nav/div/div/div/div[2]/div[1]/div[1]/div[2]/a"
            self.driver.implicitly_wait(10)
            getMatched = self.driver.find_element_by_xpath(matchedXpath)
            getMatched.click()
            
            # メッセージセット　送信
            self.driver.implicitly_wait(10)
            getTextArea = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/textarea")
            emoji = chr(int(0x1f618))

            # seleniumで絵文字が動かなかったので、Javascriptで対応
            INPUT_EMOJI = """
            arguments[0].value += arguments[1];
            arguments[0].dispatchEvent(new Event('input'));
            """
            text = "お、女神現れた" + emoji
            self.driver.execute_script(INPUT_EMOJI, getTextArea, text)
            # 明示的にスペースを入力して送信ボタンを有効にする
            getTextArea.send_keys(" ")
            print("メッセージセット完了")

            # 送信ボタン押下
            self.driver.implicitly_wait(10)
            getSendButton = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button")
            getSendButton.click()
            print("メッセージ送信完了")

            # ２秒待ってみる 
            sleep(2)
            # 4枚目からメッセージリストに画面遷移してしまうので、ここで毎回明示的にマッチリストに戻る
            self.driver.implicitly_wait(10)
            backMatchedList = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/aside/nav/div/div/div/div[1]/div/div[1]/button")
            backMatchedList.click()

            i += 1