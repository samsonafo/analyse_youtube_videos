import streamlit as st
import pandas as pd
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk

# Download stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load the pre-trained model
model = joblib.load('youtube_view_predictor.pkl')

# Function to preprocess text (remove special characters, tokenize, remove stopwords)
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = re.sub(r'\W', ' ', text.lower())
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# Streamlit app
st.title('YouTube View Predictor')

#.main {background-color: #f0f2f6;}

st.markdown("""
<style>
    
    .stButton>button {background-color: #4CAF50;color: white;}
</style>
""", unsafe_allow_html=True)

st.header('Enter video details')

title = st.text_input('Video Title')
description = st.text_area('Video Description')
tags = st.text_input('Tags (separated by spaces)')
category_name = st.selectbox('Category', ['Entertainment', 'Education', 'Music', 'Sports', 'Gaming', 'News', 'Travel', 'Lifestyle'])
duration_seconds = st.number_input('Duration (seconds)', min_value=1)
channel_video_count = st.number_input('Number of videos on the channel', min_value=1)
days_since_channel_creation = st.number_input('Days since channel creation', min_value=1)
is_for_kids = st.selectbox('Is this video for kids? (0 = No, 1 = Yes)', [0, 1])
subscriber_count = st.number_input('Subscriber count', min_value=0)

if st.button('Predict Views'):
    # Create a DataFrame for the new video
    new_video = pd.DataFrame({
        'title': [title],
        'description': [description],
        'tags': [tags],
        'category_name': [category_name],
        'duration_seconds': [duration_seconds],
        'channel_video_count': [channel_video_count],
        'days_since_channel_creation': [days_since_channel_creation],
        'is_for_kids': [is_for_kids],
        'subscriber_count': [subscriber_count]
    })

    # Preprocess the new video data
    new_video['title'] = new_video['title'].apply(preprocess)
    new_video['description'] = new_video['description'].apply(preprocess)
    new_video['tags'] = new_video['tags'].apply(preprocess)

    # Predict views
    predicted_views = model.predict(new_video)
    st.write(f'We Predict Your Video will get {predicted_views[0]:,.0f} Views')


    #color: white;
