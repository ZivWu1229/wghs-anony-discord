from PIL import Image,ImageDraw,ImageFont
import time,pyperclip
import tkinter,Get_Post
from tkinter import font,messagebox
from os.path import abspath,isdir,isfile
from os import listdir ,remove, mkdir
from auto_split import split as auto_split
import json

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

post=Get_Post.Post()

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

#tkinter functions
def prepare(text): #reset the input box
    post_content.delete(1.0,'end')
    post_content.insert('0.0',auto_split(text))

def submit(approve=True,draw=True): #approve the post, generate the picture, prepare for the next post
    #title
    try:
        number_input = int(title.get())
    except:
        messagebox.showerror("匿名薇閣","編號輸入錯誤")
        title.set(0)
        return
        
    if approve:
        post.approve()
        prepare(post.text)
        title.set(number_input+1)
    if draw:
        #setup file
        if not isdir(abspath('output')):
            mkdir('output')
        [remove(abspath('output/'+i)) for i in listdir(abspath('output'))]
        
        #draw
        word = post_content.get(1.0,'end')
        pages=split_page(word)
        for page,word in enumerate(pages):
            draw_post(number_input,word,page,len(pages))

        #prepare
        pyperclip.copy("#匿名薇閣\n#匿名薇閣"+str(number_input)+"\n#台灣匿名聯合")
    messagebox.showinfo("匿名薇閣","成功")

def ban(): #ban the post
    post.ban()
    prepare(post.text)
    messagebox.showinfo("匿名薇閣","成功")

def preview_text(): #auto split
    prepare(post_content.get(1.0,'end'))

def refresh():
    post.get_post()
    prepare(post.text)

def skip():
    post.skip()
    prepare(post.text)

def quit_handler():
    config=load_file(config_file)
    with open(config_file,'w') as file:
        config['title']=int(title.get())
        file.write(json.dumps(config))
    post_win.destroy()
    quit()

#tkinter initialization
#post window
post_win=tkinter.Tk()
post_win.title("發文審核")
post_win.resizable(0,0)
post_win.columnconfigure(0,weight=1)
post_win.columnconfigure(1,weight=1)
post_win.columnconfigure(2,weight=3)
post_win.configure(bg='#eae164')

title = tkinter.IntVar()
title.set(config['title'] if config.get('title') else 0)

button_font=font.Font(family="微軟正黑體",size=20,weight="bold")

tkinter.Entry(post_win,textvariable=title,width=40,font=font.Font(family=abspath("assets/HuiFont29.ttf"), size=20),bg='#fffefe').grid(row=0,column=0,columnspan=3,sticky='ew',padx=5,pady=5)
tkinter.Button(post_win,text='核准並送出',command=submit,font=button_font,bg='#5271ff',fg='#ffffff').grid(row=2,column=0,columnspan=2,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='送出',command=lambda: submit(approve=False),font=button_font,bg='#5271ff',fg='#ffffff').grid(row=3,column=1,rowspan=2,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='核准',command=lambda: submit(draw=False),font=button_font,bg='#5271ff',fg='#ffffff').grid(row=3,column=0,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='駁回',command=ban,font=button_font,bg='#5271ff',fg='#ffffff').grid(row=4,column=0,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='自動換行',command=preview_text,font=button_font,bg='#5271ff',fg='#ffffff').grid(row=2,column=2,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='刷新',command=refresh,font=button_font,bg='#5271ff',fg='#ffffff').grid(row=3,column=2,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='略過',command=skip,font=button_font,bg='#5271ff',fg='#ffffff').grid(row=4,column=2,sticky='nsew',padx=5,pady=5)
tkinter.Button(post_win,text='退出',command=quit_handler,font=button_font,bg='#5271ff',fg='#ffffff').grid(row=5,column=0,columnspan=3,sticky='nsew',padx=5,pady=5)

post_content = tkinter.Text(post_win,height=8,width=40,font=font.Font(family=abspath("assets/WordFont.TTC"),size=20),relief="solid",bg='#fffefe')
post_content.grid(row=1,column=0,columnspan=3,sticky='ew',padx=5,pady=5)
prepare(post.text)

post_win.protocol("WM_DELETE_WINDOW", lambda: quit_handler())

post_win.mainloop()