from flask import Flask, jsonify, request
from demographic_filtering import output
import pandas as pd


movies_df = pd.read_csv('final.csv')
app = Flask(__name__)
all_movies = movies_df[['original_title','poster_link','release_date','runtime','weighted_rating']]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        'original_title': all_movies.iloc[0,0],
        'poster_link': all_movies.iloc[0,1],
        'realese_date': all_movies.iloc[0,2]or'N/A',
        'runtime': all_movies.iloc[0,3],
        'weighted_rating': all_movies.iloc[0,4]/2
    }
    return m_data

@app.route('/movies')
def get_movies():
    movie_data = assign_val()
    return jsonify({
        'data': movie_data,
        'status': 'success'
    })
    
@app.route('/like')
def liked_movie():
    global all_movies
    movie_data = assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0],inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        'status': 'success'
    })
    
   
@app.route('/dislike')
def unliked_movie():
    global all_movies
    movie_data = assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0],inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        'status': 'success'
    })
    
   
@app.route('/didwatch')
def did_watch_movie():
    global all_movies
    movie_data = assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0],inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        'status': 'success'
    })
    
@app.route('/pop_movies')
def popular_movies():
    popular_data =[]
    for index, row in output.interrows():
        _p = {
            'original_title': row['original_title'],
            'post_link':row['post_link'],
            'release_date': row['release_date']or 'N/A',
            'duration':row['runtime'],
            'rating':row['weighted_rating']/2
        }
        popular_data.append(_p)
    return jsonify({
        'data':popular_data,
        'status':'success',
    })
    
@app.route('/recommended_movies')
def recommended_movies():
    global liked_movies
    col_names = ['original_title','poster_link','release_date','runtime','weighted_rating']
    all_recommended = pd.DataFrame(columns=col_names)
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie['original_title'])
        all_recommended = all_recommended.append(output)
    all_recommended.drop_duplicates(subset=['original_title'],inplace=True)
    recommended_movie_data = []
    for index, row in all_recommended.interrows():
        _p = {
            'original_title': row['original_title'],
            'post_link':row['post_link'],
            'release_date': row['release_date']or 'N/A',
            'duration':row['runtime'],
            'rating':row['weighted_rating']/2
        }
        recommended_movies.append()
    return jsonify({'data':recommended_movie_data,'status':'success'})

    
if __name__ == '__main__':
    app.run()