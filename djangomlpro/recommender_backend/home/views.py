from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import pickle
import pandas as pd
# Create your views here.

pwd = os.path.dirname(__file__)


with open(pwd + '/movies_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)

with open(pwd + '/similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movies_dict)

def recommend(movie,cnt):
    l = []
    try:
        movie_index = movies[movies['title'].str.lower() == movie.lower()].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:cnt]
        for i in movies_list:
            l.append(movies.iloc[i[0]].title)
        return l
    except:
        return l

def landingPage(request):
    return HttpResponse("Welcome to django backend")

def getResponseOfRecommendedMovies(request):
    movie_name = request.GET.get('name','Batman Begins')
    cnt = int(request.GET.get('count',5))
    print(movie_name)

    lt = recommend(movie_name,cnt + 1)
    
    if len(lt):
        data = {
            "movie_demanded":movie_name,
            "number_of_movie_needed":cnt,
            "movie_recomended":lt
        }
        return JsonResponse(data)
    data = {
        "movie_demanded":movie_name,
        "number_of_movie_needed":cnt,
        "message":"movie not in our database"
    }
    return JsonResponse(data)
        