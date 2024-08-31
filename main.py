from PIL import Image,ImageDraw,ImageFont
import time,json
from os.path import abspath,isfile

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

purple = (88,117,254)
black = (0,0,0)

config_file='session.json'
template_file='assets/template.json'

#load file
def load_file(file):
    if isfile(file):
        with open(abspath(file)) as file:
            return json.loads(file.read())


#assets init
config = load_file(config_file)
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


#pillow functions
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