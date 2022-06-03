from io import StringIO
import streamlit as st
import pandas as pd
import re
import preprocess,analyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
st.sidebar.title("WhatsApp chat Analyzer")
#single file at a time
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None: 
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocess.do_work(data)
    st.dataframe(df)
    Author_list=df['Author'].unique().tolist()
    Author_list.sort()
    Author_list.insert(0,"OverAll Analysis")
    df=df[df['Message']!="<omitted Media>\n"]
    df=df[df['Message']!="<Media omitted>\n"]
    selected_author=st.sidebar.selectbox("Show analysis with respect to Author",Author_list)
    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media=analyzer.fetch_stats(selected_author,df)
        col1,col2,col3=st.columns(3)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(len(words))
        # with col3:
        #     st.header("Media Files Shared")
        #     st.title(num_media)
        with col3:
            st.header("Sentiment Analysis")
            st.title(analyzer.sentiment_find(df["Message"]))
        if (selected_author=="OverAll Analysis"):    
            st.title("Active Users Analysis")
            x,new_df=analyzer.Fetch_busy_users(df)
            fig,ax=plt.subplots(figsize=(10,10))
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        df_wc=analyzer.create_wordcloud(selected_author,df)
        fig,ax=plt.subplots()
        plt.imshow(df_wc)
        st.header("Wordcloud")
        st.pyplot(fig)