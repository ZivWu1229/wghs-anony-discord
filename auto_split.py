from unicodedata import normalize

split_char=list(',.，。!?;: …⌋⌉)>⁆]›}»⟩⟧⟫⟭⟯')

def split(text)->str:
    output=''
    char_count=0
    for v in text:
        if ord(v)>=33 and ord(v)<=126:
            char_count+=.5
        else:
            char_count+=1
        if v=='\n':
            if len(output)>0 and output[-1]=='\n':
                pass
            else:
                char_count=0
                output+=v
        else:
            output+=v
        if char_count >= 23:
            for char in range(len(output)-1,-1,-1):
                if len(output)-char>=18 or output[char]=='\n':
                    output+='\n'
                    char_count=0
                    break
                elif normalize('NFKC',output[char]) in split_char:
                    output=output[0:char+1]+'\n'+output[char+1:len(output)]
                    char_count=len(output)-char
                    break
    while output[-1] == '\n':
        output=output[:-1]
    return output

def auto_split(text)->list[str]:
    output = ['']
    counter = 0
    line = 0
    page = 0
    for v in text:        
        counter+=1
        if v!='\n':
            if len(output)==0:
                output[page]+=v
            else:
                if output[-1]!='\n':
                    output[page]+=v
        if v == '\n':
            output[page]+=v
            counter = 0
            line += 1
        elif counter >= 18:
            for i in range(len(output[page])-1,-1,-1):
                if len(output[page])-i>=18 or output[page][i]=='\n':
                    output[page]+='\n'
                    counter = 0
                    break
                elif output[page][i] in split_char:
                    output[page]=output[page][0:i+1]+'\n'+output[page][i+1:len(output[page])]
                    counter=len(output[page])-i
                    break
            line += 1
        if line >= 8:
            page += 1
            counter = 0
            line = 0
            output.append('')
    while output[-1][-1] == '\n':
        output[-1]=output[-1][0:-1]
        if output[-1]=='':
            output.pop()
    return output



if __name__ == '__main__':
    #text='Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world Hello world'
    text='''更：我不知道上則編號（還沒發），總之我和朋友推坑某遊她不玩，直到她剛在學校認識新朋友喜歡玩，火速回坑（就是不是對遊戲沒興趣是對我沒興趣啦）而且他們剛認識時她跟我說那人說話像我（我要被取代惹）因為我很喜歡她，不想承認猜想。但我今天看到她貼文和那人今天出去玩，心直接涼掉，成為朋友將近一年她經常說：好想和妳出去，我也積極約她，但每次回應都是父母不允許，口氣也很誠懇和遺憾，因為她身邊朋友大多是一起長大的薇寶，也許她父母不認識我不放心。可今天無法再自欺欺人，真搞不懂；；她是我特別的朋友，我對她很真誠，結果後期一直忽冷忽熱：一邊用誠懇的語氣，一邊做這些事，明明說我是她重要的朋友，明明ig簡介@朋友列我也是前幾。還說訊息blabla，很難發現我發的（數天、數週才回我的人）但妳只是挑人回（親眼看到）我累了，不討厭妳甚至仍喜歡妳，但維持友誼的熱情被消滅殆盡'''
    output=split(text)
    print('----------------------------------------')
    print(output)
    print('----------------------------------------')