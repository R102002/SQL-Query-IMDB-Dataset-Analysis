#Project-SQL Query IMDB Dataset Analysis
#Internet Movie Database(IMDB)


#Importing the libraries

#Numpy->To perform the Mathematical operations
import numpy as np

#Pandas->Data Manipulation tool
import pandas as pd

#Matplotlib->Data Visualization tool
import matplotlib.pyplot as plt

#Seaborn->Data Visualization tool
import seaborn as sns

#SQLite->Server-less Database
import sqlite3

#Hints & Tips

# Hints
'''
1. Connect your database (or create a connection) -> sqlite3.connect(database_name)
2. Use the cursor function -> database_variable.cursor()
'''

# Workflow
'''
1. You need to establish a connection to the SQLite database by creating a Connection object
2. Then, you have to create a Cursor object using the cursor() method
3. Then, excute the query -> cursor_object.execute('query')
4. To fetch the data, then use fetchall() method of the cursor object
'''

#1.Establishing the connection to the database
db="movies.sqlite"
conn=sqlite3.connect(db)
cur=conn.cursor()


#2.Get all the data about movies?
#establishing the connection with the Database
cur.execute('select  *  from movies')
#Creating the cursor object
movies=cur.fetchall()
#Displaying the database data
#print(movies)

#Creating a dataframe
movies=pd.DataFrame(movies,columns = ['id', 'original_title', 'budget', 'popularity', 'release_date', 'revenue', 'title', 'vote_average', 'vote_count', 'overview', 'tagline', 'uid', 'director_id'])
#Displaying the dataframe
print(movies)

print(movies.info())

#3.Get all the data about directors?
cur.execute('select * from directors')
directors=cur.fetchall()
#print(directors)

directors=pd.DataFrame(directors,columns=['name', 'id', 'gender', 'uid',
                                  'department'])
print(directors)

print(directors.info())

#4.Check how many movies are present in the IMDB table
cur.execute('select count(Title) from movies')
count=cur.fetchall()
print(f"The number of movies present in IMDB database is {count[0]}")

#5.Find these 3 directors:James Cameron,Luc Besson,John Woo
cur.execute("select * from directors where name in('James Cameron', 'Luc Besson', 'John Woo')")
three_directors=cur.fetchall()
print(three_directors)

#6.Find all the directors with name starting with 'Steven'
cur.execute("SELECT * FROM directors WHERE name LIKE 'Steven%'")
name_like=cur.fetchall()
print(f"The directors whose names are starting with the word 'Steven' are:{name_like}")

#7.Count the Female directors
cur.execute("SELECT COUNT(*) FROM directors WHERE gender=='1'")
females=cur.fetchall()
print(f"The number of female directors is {females[0][0]}")

#8.Find the name of the 10th first women directors
cur.execute('SELECT name FROM directors WHERE gender==1')
tenth=cur.fetchall()
print(f"The tenth first women is {tenth[9][0]}")

#9.What are the 3 most popular movies?
cur.execute('SELECT title FROM movies ORDER BY popularity DESC LIMIT 3')
most_popular=cur.fetchall()
print(f"The 3 mostpopular movies are : {most_popular[0][0]},{most_popular[1][0]},{most_popular[2][0]}")

#10.What are the 3 most bankable movies?
cur.execute('SELECT title FROM movies ORDER BY Budget DESC LIMIT 3')
most_bankable=cur.fetchall()
print(f"The three most bankable movies are : {most_bankable[0][0]},{most_bankable[1][0]},{most_bankable[2][0]}")

#11.What is the most awarded average vote movie since the Jan 1st,2000?
cur.execute("SELECT Original_title FROM movies WHERE Release_date    > '2000-01-01' ORDER BY vote_average DESC LIMIT 1")
most_awarded_avg = cur.fetchall()
print(f"The most awarded average rated movie is {most_awarded_avg[0][0]}")

#12.Which movie(s) were directed by Brenda Chapman?
cur.execute("SELECT original_title FROM movies JOIN directors ON directors.id = movies.director_id WHERE directors.name = 'Brenda Chapman'")
directed_by = cur.fetchall()
print(f"The movie(s) directed by Brenda Chapman is {directed_by[0][0]}")

#13.Name the director who has made the most movies?
cur.execute("SELECT name FROM directors JOIN movies ON directors.id = movies.director_id GROUP BY director_id ORDER BY count(name)DESC LIMIT 1 ")
director_movie=cur.fetchall()
print(f"The director who made the most movies is {director_movie[0][0]}")

#14.Name of the director who is most bankable
cur.execute("SELECT name FROM directors JOIN movies on directors.id=movies.director_id GROUP BY director_id ORDER BY SUM(budget) DESC LIMIT 1")
most_bankable = cur.fetchall()
print(f'The most bankable director is {most_bankable[0][0]}')

#BUDGET ANALYSIS
#1.Tell the Top 10 highest budget making movie

cur.execute('Select * FROM movies ORDER BY budget DESC LIMIT 10')
top_10 = cur.fetchall()
most_popular = pd.DataFrame(top_10, columns=['id', 'original_title', 'budget', 'popularity', 'release_date',
       'revenue', 'title', 'vote_average', 'vote_count', 'overview', 'tagline',
       'uid', 'director_id'])
print(most_popular)

#Revenue Analysis
#1.Find Top 10 Revenue making movies

cur.execute("SELECT * FROM movies ORDER BY revenue DESC LIMIT 10")
top10_movies = cur.fetchall()
most_revenue = pd.DataFrame(top10_movies,  columns= ['id','original_title','budget','popularity','release_date',
                                    'revenue', 'title','vote_average','vote_count','overview',
                                    'tagline','uid','director_id'])
print(most_revenue)

#Voting Analysis

#1.Find the most popular movies with highest vote_average
cur.execute(("SELECT * FROM movies ORDER BY vote_average DESC LIMIT 10"))
most_pop = cur.fetchall() 
most_popular_movie = pd.DataFrame(most_pop,columns =['id', 'original_title', 'budget', 'popularity', 'release_date',
       'revenue', 'title', 'vote_average', 'vote_count', 'overview', 'tagline',
       'uid', 'director_id'])
print(most_popular_movie)

#Director Analysis

'''
1.Name all the directors with the number of movies and revenue where Revenue should be taken into account for doing the analysis. The director who has the highest revenue should comes at the top and so on and so forth.
'''

cur.execute("SELECT name,COUNT(*) AS 'Total Movies',SUM(revenue) AS 'Total Revenue' FROM  directors JOIN movies WHERE directors.id==movies.director_id GROUP BY director_id ORDER BY SUM(revenue) DESC")
director_revenue=cur.fetchall()
director_most_revenue=pd.DataFrame(director_revenue,columns=['Director_Name','Total Movies','Total Revenue'])
print(director_most_revenue.head(10))


'''
2.Name all the directors with the number of movies and revenue where number of movies should be taken into account for doing the analysis. The director who has the highest number of movies should comes at the top and so on and so forth.
'''
cur.execute("SELECT name, COUNT(title), SUM(revenue) FROM directors JOIN movies ON movies.director_id = directors.id GROUP by director_id ORDER BY  COUNT(title) DESC LIMIT 10")
director_movies = cur.fetchall()
director_most_movies = pd.DataFrame(director_movies,columns=['name','no_of_title','revenue'])
print(director_most_movies)

'''
3.Give the Title of the movie, realease_date, budget, revenue, popularity and vote_average made by Steven Spielberg
'''
cur.execute("SELECT title, release_date,budget,revenue,popularity,vote_average FROM directors JOIN movies ON directors.id==movies.director_id WHERE directors.name=='Steven Spielberg'")
movies_list=cur.fetchall()
movies_list_Steven_Spielberg=pd.DataFrame(movies_list,columns=['Movie_Name','Release_Date','Total Budget','Total_Revenue','Popularity','Vote_Average'])
print(movies_list_Steven_Spielberg)