from PIL import Image,ImageDraw,ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json
from os.path import abspath,isdir,isfile
from os import system,listdir,remove,mkdir
from selenium.webdriver.chrome.options import Options

#load file
def load_file(file):
    if isfile(file):
        with open(abspath(file)) as file:
            return json.loads(file.read())

#draw post
def draw_post(number,word,page,total_page):
        if total_page==1:
            image = Image.open(abspath("assets/"+template['background']['both']))
        elif page == 0:
            image = Image.open(abspath("assets/"+template['background']['first']))
        elif page == total_page-1:
            image = Image.open(abspath("assets/"+template['background']['last']))
        else:
            image = Image.open(abspath("assets/"+template['background']['middle']))
        draw = ImageDraw.Draw(image)
        #Date
        localTime = time.localtime(time.time())
        date = f'{str(localTime.tm_year)}/{str(localTime.tm_mon)}/{str(localTime.tm_mday)}'
        
        if page == 0:
            draw.text(template['position']['title'],"#匿名薇閣"+str(number),black,font=title_font,anchor='mm')
        if page == total_page-1:
            draw.text(template['position']['date'],date,black,font=date_font)
        #body
        if total_page==1:
            draw.multiline_text(template['position']['content']['middle'],word,black,font=word_font,anchor='mm',align='center',spacing=20)
        elif page ==0 :
            draw.multiline_text(template['position']['content']['first'],word,black,font=word_font,anchor='mm',align='center',spacing=30)
        elif page == total_page-1:
            draw.multiline_text(template['position']['content']['last'],word,black,font=word_font,anchor='mm',align='center',spacing=30)
        else:
            draw.multiline_text(template['position']['content']['middle'],word,black,font=word_font,anchor='mm',align='center',spacing=30)
        #save
        image.save(abspath("output/"+str(number)+'-'+str(page+1)+".png"))

def split_page(text):
    output=['']
    line_counter=0
    page=0
    for v in text:
        output[page]+=v
        if v == '\n':
            line_counter+=1
        if line_counter >= 9:
            page += 1
            line_counter = 0
            output.append('')
    
    #delete empty page
    if output[-1]=='':
        output=output[:-1]
    #delete unnecessary \n
    for page,text in enumerate(output):
        if text[len(text)-1]=='\n':
            output[page]=output[page][:-1]
    return output

#inti drawing
purple = (88,117,254)
black = (0,0,0)

template_file='assets/template.json'
template = load_file(template_file)

try:
    title_font = ImageFont.truetype(abspath(f"assets/{template['font']['title']}"),size=template['size']['title'])
    date_font = ImageFont.truetype(abspath(f"assets/{template['font']['date']}"),size=template['size']['date'])
    word_font = ImageFont.truetype(abspath(f"assets/{template['font']['content']}"),size=template['size']['content'])
    Image.open(abspath("assets/"+template['background']['first']))
    Image.open(abspath("assets/"+template['background']['middle']))
    Image.open(abspath("assets/"+template['background']['last']))
    Image.open(abspath("assets/"+template['background']['both']))

except:
    print('Assets missing, contact developer for further information.')
    input('Press enter to exit:')
    exit()

class Post():
    post_index = 0
    def login(self,config):
        self.driver_startup()
        for i in range(3):
            try:
                self.Login(config,self.driver)
                self.get_post()
            except IndexError:
                return 1
            except Exception as exception:
                print('error:'+str(exception))
                return 1
            else:
                return " ".join(self.driver.find_elements(By.CLASS_NAME,"mr-3")[0].text.split(" ")[2:])
        #input('登入失敗，點擊enter重啟...')
        #system(f'py {abspath("main.py")}')
        #quit()
    def driver_startup(self):
        #print('網頁驅動器啟動中...')
        options = Options()
        self.driver=webdriver.Edge()
        self.driver.minimize_window()
    def approve(self):
        text=self.text
        while True:
            
            self.driver.find_elements(By.XPATH,"//button")[5+5*self.post_index].click()
            self.driver.implicitly_wait(10)
            self.get_post()
            if self.text != text:
                break
    def ban(self):
        self.driver.find_elements(By.XPATH,"//button")[6+5*self.post_index].click()
        self.get_post()
    def get_post(self,refresh=True):
        if refresh:
            self.driver.get('https://wghs-anony.forteens.cc/admin/articles?type=waiting')
        self.driver.implicitly_wait(10)
        self.text=self.driver.find_elements(By.CLASS_NAME,"break-words")[self.post_index].text
        return self.text
    def skip(self):
        self.post_index+=1
        self.get_post(refresh=False)
    def logout(self):
        self.driver.quit()
        del self
    def submit(self):
        #setup file
        if not isdir(abspath('output')):
            mkdir('output')
        [remove(abspath('output/'+i)) for i in listdir(abspath('output'))]
        
        #draw
        word = self.text
        pages=split_page(word)
        for page,word in enumerate(pages):
            draw_post(self.number,word,page,len(pages))
    class Login():
        def __init__(self,config,driver) -> None:
            #print('嘗試登入中...')
            self.driver=driver
            self.manual_login(config['email'],config['password'])
            #config['session']=self.driver.get_cookie('_session')['value']
            #save_config()
        def manual_login(self,email=None,password=None):
            self.driver.get('https://wghs-anony.forteens.cc/admin/dashboard')
            self.driver.find_element(By.ID,'email').send_keys(email)
            self.driver.find_element(By.ID,'password').send_keys(password)
            self.driver.find_element(By.XPATH,'//button').click()
            #os.system('cls')
        def auto_login(self,config):
            self.manual_login(config['email'],config['password'])
