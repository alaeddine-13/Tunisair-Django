import bs4 as BeautifulSoup
import requests
import pandas as pd
import datetime as dt 
import re
import random


def get_flights_realtime(x,y,m):
    dics=[]
    m = dt.datetime.today().month
    y = dt.datetime.today().year
    x = dt.datetime.today().day

    registered=0

    url="http://oaca.nat.tn/newapp/hvdynt/resultatsvolsfrcall2.php?change=1&startRow=1&frmmvtCod=D&frmaeropVil=-1&frmnumVol=&frmairport=tunis&frmday={}&frmmonth={}&frmacty={}&frmhour=0".format(x,m,y)
    suburl=url.find("frmmonth",0,len(url))
    #month=url[suburl+9:suburl+11]
    #if (month.isdigit()==False):
        #month=month[0]
    req = requests.get(url)
    soup = BeautifulSoup.BeautifulSoup(req.text) 
    trs = soup.findAll("tr" , attrs={"align": u"center"})
    trs=trs[1:]
    for tr in trs:
        tds=tr.findAll("td")
        company = tds[2].text
        if(company != "TUNISAIR"):
            continue
        dest=tds[0].text
        time=tds[1].text
        hr=int(time[0:time.find(':',0)])
        mi=int(time[time.find(':',0)+1:])
        date=dt.datetime(year=y, month=m, day=x, hour=hr, minute=mi)
        timestampStr = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        comment=tds[4].text
        delay=0
        regex=re.compile("^DECOLLE")
        actualTime = ""
        if (regex.match(comment)):
            
            #time=comment[comment.find(" ",0)+1:]
            hour=int(comment[comment.find(" ",0)+1:comment.find(" ",0)+3])
            minute=int(comment[comment.find(":",0)+1:])
            time=dt.datetime(year=y, month=m, day=x, hour=hour, minute=minute)
            actualTime=time.strftime("%Y-%m-%d %H:%M:%S.%f")
            delay=(time-date).total_seconds()/60
            comment="DECOLLE"
        capacity = 162
        registered = 162
        if(comment=="ENREGISTREMENT"):
            registered = random.randrange(capacity)
        elif (comment=="DECOLLE"):
            registered = capacity
        else :
            registered = 0
        dics.append({"dest":dest,"plannedTime": str(timestampStr),"actualTime": str(actualTime),"company":company,"capacity":capacity,"registered":registered,"flightId":tds[3].text,"status":comment,"delay":delay})
    return dics
