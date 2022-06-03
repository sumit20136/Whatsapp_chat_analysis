
from pyexpat.errors import messages
import re
import regex
import pandas as pd
import numpy as np
import emoji
import datetime
def startsWithDateAndTimeAndroid(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -' 
    result = re.match(pattern, s)
    if result:
        return True
    return False

def FindAuthor(s):
    s=s.split(":")
    if len(s)==2:
        return True
    else:
        return False
def getDataPointAndroid(line):   
    splitLine = line.split(' - ') 
    dateTime = splitLine[0]
    date, time = dateTime.split(', ') 
    message = ' '.join(splitLine[1:])
    if FindAuthor(message): 
        splitMessage = message.split(':') 
        author = splitMessage[0] 
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message

def dateconv(date):
    year=''
    if '-' in date:
      year = date.split('-')[2]
      if len(year) == 4:
        return datetime.datetime.strptime(date, "[%d-%m-%Y").strftime("%Y-%m-%d")
      elif len(year) ==2:
        return datetime.datetime.strptime(date, "[%d-%m-%y").strftime("%Y-%m-%d")
    elif '/' in date:
      year = date.split('/')[2]
      if len(year) == 4:
        return datetime.datetime.strptime(date, "[%d/%m/%Y").strftime("%Y-%m-%d")
      if len(year) ==2:
        return datetime.datetime.strptime(date, "[%d/%m/%y").strftime("%Y-%m-%d")
def split_count(text):

    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list
parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
# conversationPath = 'WhatsApp Chat with Hostel Peeps.txt' 
# f=open(conversationPath,'r', encoding="utf-8")
# data=f.read()
def do_work(data):
    data=data.split('\n')
    messageBuffer = [] 
    date, time, author = None, None, None
    for line in data:
        line = line.strip() #to remove whitespaces at beginning and end of string
        if startsWithDateAndTimeAndroid(line): #indicates beginning of new message
          if len(messageBuffer) > 0:
            parsedData.append([date, time, author, ' '.join(messageBuffer)])
          messageBuffer.clear()
          date, time, author, message = getDataPointAndroid(line)
          messageBuffer.append(message)
        else:
          messageBuffer.append(line)

    df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.dropna()  #dropping all null valued rows
    df["emoji"] = df["Message"].apply(split_count)
    df=df.reset_index(drop=True)
    df['year']=df['Date'].dt.year
    df['month']=df['Date'].dt.month_name()
    df['date']=df['Date'].dt.day
    df=df.drop(columns="Date")
    df.to_csv("processed_chat.csv")
    return df