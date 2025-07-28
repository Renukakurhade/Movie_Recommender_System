import time

import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=b4b32e8e6b07aed5728b3143bf8f88bd&language=en-US'
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/150?text=No+Poster"
    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/150?text=Error"


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        time.sleep(1)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

st.header('Movie Recommender System')
movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie=st.selectbox('Type or select a movie from the dropdown',movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i]:
            st.markdown(f"<p style='white-space: nowrap; overflow: hidden; text-overflow: ellipsis'>{names[i]}</p>",
            unsafe_allow_html=True
            )
            st.image(posters[i], use_container_width=True)