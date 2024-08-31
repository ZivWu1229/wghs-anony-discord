from selenium import webdriver
from selenium.webdriver.common.by import By
import os.path,json
from tkinter import messagebox
from os import remove,system
from selenium.webdriver.chrome.options import Options


config_file=os.path.abspath('session.json')
config={}

#load config
if os.path.isfile(config_file):
    with open(config_file) as file:
        config=json.loads(file.read())
        
def save_config():
    with open(config_file,('w' if os.path.isfile(config_file) else 'x')) as file:
        file.write(json.dumps(config))

class Post():
    post_index = 0
    def __init__(self):
        global config
        self.driver_startup()
        for i in range(3):
            try:
                Login()
                self.get_post()
            except IndexError:
                if os.path.isfile(config_file):
                    remove(config_file)
                config={}
                print('登入失敗!')
                continue
            except Exception as exception:
                if os.path.isfile(config_file):
                    remove(config_file)
                config={}
                print('error:'+str(exception))
                continue
            else:
                print('登入成功，請開始審核!')
                return
        input('登入失敗，點擊enter重啟...')
        system(f'py {os.path.abspath("main.py")}')
        quit()
    def driver_startup(self):
        global driver
        print('網頁驅動器啟動中...')
        options = Options()
        #driver=webdriver.Chrome(options=options)
        driver=webdriver.Edge()
        driver.minimize_window()
    def approve(self):
        text=self.text
        while True:
            
            driver.find_elements(By.XPATH,"//button")[5+5*self.post_index].click()
            driver.implicitly_wait(10)
            self.get_post()
            if self.text != text:
                break
    def ban(self):
        driver.find_elements(By.XPATH,"//button")[6+5*self.post_index].click()
        self.get_post()
    def get_post(self,refresh=True):
        if refresh:
            driver.get('https://wghs-anony.forteens.cc/admin/articles?type=waiting')
        driver.implicitly_wait(10)
        self.text=driver.find_elements(By.CLASS_NAME,"break-words")[self.post_index].text
    def skip(self):
        self.post_index+=1
        self.get_post(refresh=False)

class Login():
    def __init__(self) -> None:
        print('嘗試登入中...')
        driver.get('https://wghs-anony.forteens.cc/admin/dashboard')
        if config == {}:
            self.manual_login()
        else:
            self.auto_login()
        config['session']=driver.get_cookie('_session')['value']
        save_config()
    def manual_login(self,email=None,password=None):
        if not (email and password):
            print('請輸入帳號密碼...')
            email = input('email:')
            password = input('password:')
            config['email']=email
            config['password']=password
            system('cls')
        driver.get('https://wghs-anony.forteens.cc/admin/dashboard')
        driver.find_element(By.ID,'email').send_keys(email)
        driver.find_element(By.ID,'password').send_keys(password)
        driver.find_element(By.XPATH,'//button').click()
        #os.system('cls')
    def auto_login(self):
        driver.add_cookie({'name':'_session','value':config['session']})
        try:
            driver.get('https://wghs-anony.forteens.cc/admin/articles?type=waiting')
            driver.implicitly_wait(10)
            driver.find_element(By.CLASS_NAME,"break-words")
        except:
            print('憑證失效，嘗試輸入帳密...')
            self.manual_login(config['email'],config['password'])

if __name__ == "__main__":
    #driver=webdriver.Chrome(options=Options(),executable_path=os.path.abspath('driver\\chromedriver.exe'))
    driver=webdriver.Edge()
    driver.maximize_window()
    Login()