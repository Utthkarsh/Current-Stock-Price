from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError

def web_content_div(web_content,classPath,value):
    web_content_div = web_content.find_all('div',{'class': classPath})
    try:
        if(value != None):
            fin_streamers = web_content_div[0].find_all(value)
            texts = [streamer.get_text('value') for streamer in fin_streamers]
        else:
            texts = []
    except IndexError:
        texts = []
    return texts
def currentPrice(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch'
    try:
        req = requests.get(url)
        web_content = BeautifulSoup(req.text,'lxml')
        #price and change
        texts = web_content_div(web_content,'D(ib) Mend(20px)','fin-streamer')
        if texts != []:
            price,change = texts[0], texts[1] + '' + texts[2]
        else:
            price,change = [],[]
        #volume
        if ticker[-2:] == '=F':
            texts = web_content_div(web_content,'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)'
                                    ,'fin-streamer')
            
        else:
            texts = web_content_div(web_content,'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)'
                                    ,'fin-streamer')
        if texts != []:
            volume = texts[0]
        else:
            volume = []
    except ConnectionError:
        price,change = [],[]
        print("Connection Error")
    return price,change,volume
def run():
    Stocks = []
    chk = 0
    boo = 1
    cnt = 0
    while(boo == 1):
        s = input("Enter the stock ticker name: ")
        print("\n")
        for i in Stocks:
            if s == i:
                print("Already in list of stocks.\n")
                chk = 1
        if chk == 0:
            Stocks.append(s)
            
        for stk in Stocks:
            a = currentPrice(stk)
            if a[0] != []:
                print("Name: " + stk + "\n" + "Current Price: " + a[0] + "\n" + "Price Change: " + a[1] + "\n" + "Volume: " + a[2] + "\n")
                cnt = 1
            else:
                print("Not a valid stock name.\n")
                Stocks.remove(stk)
                break
        lv = input("Do you want to leave? Answer yes or no. ")
        if lv == 'yes':
            boo = 0
        if lv == 'no':
            if cnt == 1:
                rset = input("Do you want to reset stock data? Answer yes or no. ")
                if rset == "yes":
                    Stocks = []
run()

        




