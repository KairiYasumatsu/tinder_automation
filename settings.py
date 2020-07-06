# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

FacebookMail= os.environ.get("FACEBOOK_MAIL") # 環境変数の値をFacebookMailに代入
FacebookPass= os.environ.get("FACEBOOK_PASS")
TinderAuth= os.environ.get("TINDER_AUTH")