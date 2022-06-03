from wordcloud import WordCloud
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def fetch_stats(selected_author,df):
    if selected_author!="OverAll Analysis":
        df=df[df['Author']==selected_author]
    num_messages=df.shape[0]
    words=[]
    for word in df['Message']:
        words.extend(word.split(" "))
    # df=df[df['Message']!="<omitted Media>"]
    # df=df[df['Message']!="<Media omitted>"]
    
    num_media=df[df['Message']=='<Media omitted>'].shape[0]
    return num_messages,words,num_media

def Fetch_busy_users(df):
    x=df['Author'].value_counts().head()
    new_df=round((df["Author"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':"Name","Author":"Percentage"})
    return x,new_df
def create_wordcloud(selected_author,df):
    if selected_author!='OverAll Analysis':
        df=df[df['Author']==selected_author]
    wc=WordCloud(width=500,height=500,min_font_size=10)
    df_wc=wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc

def sentiment_find(message_list):
    sentiments=SentimentIntensityAnalyzer();
    positive=[]
    negative=[]
    neutral=[]
    positive.append([sentiments.polarity_scores(i)["pos"] for i in message_list])
    negative.append([sentiments.polarity_scores(i)["neg"] for i in message_list])
    neutral.append([sentiments.polarity_scores(i)["neu"] for i in message_list])
    positive_ans=sum(positive[0])
    negative_ans=sum(negative[0])
    neutral_ans=sum(neutral[0])
    if( (positive_ans>negative_ans) and (positive_ans>neutral_ans)):
        return "positive"
    elif((neutral_ans>positive_ans) and (neutral_ans>negative_ans)):
        return "neutral"
    else:
        return "negative"