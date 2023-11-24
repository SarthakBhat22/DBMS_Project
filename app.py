import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
import json

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="DBMS_Project"
)
cursor = db.cursor()

# Function to check login credentials
def check_login(username, password):
    cursor.execute("SELECT * FROM UserDB WHERE Username = %s AND Password = %s", (username, password))
    user = cursor.fetchone()
    return user


if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Main Section (Only visible after successful login)
def get_user_id(username):
    cursor.execute("SELECT UserID FROM UserDB WHERE Username = %s", (username,))
    user_id = cursor.fetchone()
    return user_id[0] if user_id else None


# Function to get movie reviews using the stored procedure
def get_movie_reviews(movie_title):
    cursor.callproc("Reviews", [movie_title])
    reviews = []
    for result in cursor.stored_results():
        reviews = result.fetchall()
    return reviews

# Streamlit UI
st.title('Movie Review System')

# Check if the user is logged in
if st.session_state.get('logged_in', False):
    st.subheader('Welcome to the Movie Review System')

    # Get the movie titles for the dropdown
    cursor.execute("SELECT Title FROM MovieDB")
    movie_titles = [title[0] for title in cursor.fetchall()]
    selected_movie_title = st.selectbox("Select a movie to review:", movie_titles)

    cursor.execute("SELECT m.Title, m.GenreID, m.Description, m.AverageRating, d.Name AS Director, a.Name AS Actor, g.GenreName AS Genre "
                   "FROM MovieDB m "
                   "JOIN DirectorDB d ON m.DirectorID = d.DirectorID "
                   "JOIN ActorDB a ON m.ActorID = a.ActorID "
                   "JOIN GenreDB g ON m.GenreID = g.GenreID "
                   "WHERE m.Title = %s",
                   (selected_movie_title,))
    movie_details = cursor.fetchone()
    with open('conf.json', 'r') as config_file:
        config_data = json.load(config_file)
    if movie_details:
        col1, col2, col3 = st.columns([1, 2, 1])
        if selected_movie_title in config_data:
            with col2:
                poster_width = 250
                st.image(config_data[selected_movie_title]["poster_url"], width=poster_width, use_column_width=False)
        st.subheader("Movie Details for {}".format(selected_movie_title))
        movie_details_data = {
            "Title": movie_details[0],
            "Genre": movie_details[6],
            "Description": movie_details[2],
            "Average Rating": st.session_state.average_rating if hasattr(st.session_state, 'average_rating') else movie_details[3],
            "Director": movie_details[4],
            "Lead Actor": movie_details[5]
        }
        st.table(pd.DataFrame([movie_details_data]))
    else:
        st.warning("No details available for {}".format(selected_movie_title))

    # Get review information from the user
    rating = st.slider("Rating (1-5)", 1, 5, 3)
    comments = st.text_area("Comments")

    review_date = datetime.now().strftime("%Y-%m-%d")

    # Insert the review into the ReviewDB table
    if st.button("Submit Review"):
        # Fetch MovieID based on the selected title
        cursor.execute("SELECT MovieID FROM MovieDB WHERE Title = %s", (selected_movie_title,))
        movie_id = cursor.fetchone()[0]

        # Insert review
        cursor.execute("INSERT INTO ReviewDB (Rating, Comments, ReviewDate, UserID, MovieID) "
                       "VALUES (%s, %s, %s, %s, %s)",
                       (rating, comments, review_date, st.session_state.user_id, movie_id))
        db.commit()
        st.success("Review submitted successfully!")


    if st.session_state.get('logged_in', False) and st.session_state.get('is_admin', False):
        st.subheader('Admin Section')

        # Get the movie titles for the dropdown
        cursor.execute("SELECT Title FROM MovieDB")
        movie_titles = [title[0] for title in cursor.fetchall()]
        selected_movie_title = st.selectbox("Select a movie to delete reviews:", movie_titles)

        if st.button("Delete Reviews"):
            # Delete reviews for the selected movie
            cursor.execute("DELETE FROM ReviewDB WHERE MovieID = (SELECT MovieID FROM MovieDB WHERE Title = %s)", (selected_movie_title,))
            db.commit()
            st.success("Reviews for {} deleted successfully!".format(selected_movie_title))
            

    movie_reviews = get_movie_reviews(selected_movie_title)

    if movie_reviews:
        st.subheader("Reviews for {}".format(selected_movie_title))
        review_df = pd.DataFrame(movie_reviews, columns=["Username", "Rating", "Comments", "ReviewDate"])
        st.dataframe(review_df)
    else:
        st.info("No reviews available for {}".format(selected_movie_title))

    # Display the highest-rated movie
    cursor.execute("SELECT m.Title, m.AverageRating, d.Name AS Director, a.Name AS Actor, g.GenreName AS Genre "
                   "FROM MovieDB m "
                   "JOIN DirectorDB d ON m.DirectorID = d.DirectorID "
                   "JOIN ActorDB a ON m.ActorID = a.ActorID "
                   "JOIN GenreDB g ON m.GenreID = g.GenreID "
                   "ORDER BY m.AverageRating DESC "
                   "LIMIT 1")
    highest_rated_movie = cursor.fetchone()

    st.subheader('Movies by Actor')
    
    cursor.execute("SELECT Name FROM ActorDB")
    actor_names = [name[0] for name in cursor.fetchall()]
    selected_actor_name = st.selectbox("Select an actor to view movies:", actor_names)

    # Fetch movies and review counts for the selected actor
    cursor.execute("SELECT m.Title, m.Description, m.AverageRating, d.Name AS Director, a.Name AS Actor, g.GenreName AS Genre, COUNT(r.MovieID) AS ReviewCount "
                "FROM MovieDB m "
                "JOIN DirectorDB d ON m.DirectorID = d.DirectorID "
                "JOIN ActorDB a ON m.ActorID = a.ActorID "
                "JOIN GenreDB g ON m.GenreID = g.GenreID "
                "LEFT JOIN ReviewDB r ON m.MovieID = r.MovieID "
                "WHERE a.Name = %s "
                "GROUP BY m.MovieID",
                (selected_actor_name,))
    actor_movies = cursor.fetchall()

    if actor_movies:
        st.subheader(f"Movies featuring {selected_actor_name}")
        actor_movies_df = pd.DataFrame(actor_movies, columns=["Title", "Description", "Average Rating", "Director", "Actor", "Genre", "Review Count"])
        st.dataframe(actor_movies_df)
        
        average_actor_rating = actor_movies_df["Average Rating"].mean()
        st.subheader(f"Average Rating for {selected_actor_name}: {average_actor_rating:.2f}")

    else:
        st.info(f"No movies available for {selected_actor_name}")

    st.subheader("Highest Rated Movie")

    highest_rated_movie_data = {
        "Movie Title": highest_rated_movie[0],
        "Average Rating": highest_rated_movie[1],
        "Director": highest_rated_movie[2],
        "Lead Actor": highest_rated_movie[3],
        "Genre": highest_rated_movie[4]
    }
    st.table(pd.DataFrame([highest_rated_movie_data]))


    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.is_admin = False

else:
    # Login/Sign Up Section
    st.subheader('Login or Sign Up')
    st.subheader('Select Action')
    login_or_signup = st.radio("Choose an option:", ("Login", "Sign Up"))

    # Sign Up Section
    if login_or_signup == "Sign Up":
        st.subheader('Sign Up')
        new_username = st.text_input('Username')
        new_email = st.text_input('Email')
        new_password = st.text_input('Password', type='password')
        
        if st.button('Sign Up'):
            if new_username and new_email and new_password:
                # Check if the username is already taken
                cursor.execute("SELECT * FROM UserDB WHERE Username = %s", (new_username,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    st.error('Username already taken. Please choose a different one.')
                else:
                    # Insert new user into UserDB
                    cursor.execute("INSERT INTO UserDB (Username, Email, Password, RegistrationDate) "
                                "VALUES (%s, %s, %s, CURDATE())",
                                (new_username, new_email, new_password))
                    db.commit()
                    st.success('Sign Up successful! You can now log in.')
            else:
                st.error('Please fill in all the fields for Sign Up.')
    
    # Login Section
    if login_or_signup == "Login":
        st.subheader('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            if username and password:
                user = check_login(username, password)
                if user:
                    st.success('Login successful!')
                    st.session_state.logged_in = True
                    st.session_state.user_id = get_user_id(username)  # Fetch user_id based on the username
                    st.session_state.is_admin = username == 'admin'
                else:
                    st.error('Invalid username or password')

# Close the database connection
db.close()
