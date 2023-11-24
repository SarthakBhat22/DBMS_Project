import mysql.connector
import random

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="DBMS_Project"
)

cursor = db.cursor()

"""
-- Create the User Table
CREATE TABLE UserDB (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Genre Table
CREATE TABLE GenreDB (
    GenreID INT AUTO_INCREMENT PRIMARY KEY,
    GenreName VARCHAR(50) NOT NULL
);

-- Create the Actor Table
CREATE TABLE ActorDB (
    ActorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- Create the Director Table
CREATE TABLE DirectorDB (
    DirectorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

-- Create the Movie Table
CREATE TABLE MovieDB (
    MovieID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    ReleaseYear INT NOT NULL,
    Description TEXT,
    AverageRating DECIMAL(3, 2),
    GenreID INT,
    ActorID INT,
    DirectorID INT,
    FOREIGN KEY (GenreID) REFERENCES Genre(GenreID),
    FOREIGN KEY (ActorID) REFERENCES Actor(ActorID),
    FOREIGN KEY (DirectorID) REFERENCES Director(DirectorID)
);

-- Create the Review Table
CREATE TABLE ReviewDB (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    Rating INT NOT NULL,
    Comments TEXT,
    ReviewDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UserID INT,
    MovieID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID)
);





DELIMITER //
CREATE PROCEDURE Reviews(IN movie_title VARCHAR(255))
BEGIN
SELECT u.Username, r.Rating, r.Comments, r.ReviewDate
FROM ReviewDB r
JOIN UserDB u ON r.UserID = u.UserID
JOIN MovieDB m ON r.MovieID = m.MovieID
WHERE m.Title = movie_title;
END;
//


DELIMITER //
CREATE TRIGGER update_average_rating
AFTER INSERT ON ReviewDB
FOR EACH ROW
BEGIN
UPDATE MovieDB m
SET AverageRating = (
SELECT AVG(Rating)
FROM ReviewDB r
WHERE r.MovieID = NEW.MovieID
)
WHERE m.MovieID = NEW.MovieID;
END;
//
DELIMITER ;

"""

"""

genres_data = [
    (1, 'Thriller'),
    (2, 'Action'),
    (3, 'Drama'),
    (4, 'Crime'),
    (5, 'Sci-Fi'),
    (6, 'Romance'),
    (7, 'Fantasy'),
    (8, 'War'),
]


for genre in genres_data:
    cursor.execute("INSERT INTO GenreDB (GenreID, GenreName) VALUES (%s, %s)", genre)

actor = [
    (114, "Matthew McConaughey"),
    (115, "Jamie Fox"),
    (116, "Michael J Fox"),
    (117, "Arnold Schwarzenegger"),
    (118, "Harrison Ford")
]

for act in actor:
    cursor.execute("INSERT INTO ActorDB (ActorID, Name) VALUES (%s, %s)", act)


director_data = [
    (201, 'Christopher Nolan'),
    (202, 'Robert Zemeckis'),
    (203, 'Frank Darabont'),
    (204, 'Quentin Tarantino'),
    (205, 'Lana Wachowski'),
    (206, 'James Cameron'),
    (207, 'Francis Ford Coppola'),
    (208, 'Steven Spielberg'),
    (209, 'Peter Jackson'),
    (210, 'Jonathan Demme'),
    (211, 'Michel Gondry')
]


for director in director_data:
    cursor.execute("INSERT INTO DirectorDB (DirectorID, Name) VALUES (%s, %s)", director)


    https://www.themoviedb.org/t/p/original/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg
    https://www.themoviedb.org/t/p/original/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg
    https://www.themoviedb.org/t/p/original/8VG8fDNiy50H4FedGwdSVUPoaJe.jpg
     https://www.themoviedb.org/t/p/original/7oWY8VDWW7thTzWh3OKYRkWUlD5.jpg
     https://www.themoviedb.org/t/p/original/ji3ecJphATlVgWNY0B0RVXZizdf.jpg
     https://www.themoviedb.org/t/p/original/hzXSE66v6KthZ8nPoLZmsi2G05j.jpg
     https://www.themoviedb.org/t/p/original/ceG9VzoRAVGwivFU403Wc3AHRys.jpg
"""


movies_data = [
    (str(random.randint(1000, 9999)), 'Interstellar', 2014, 'A space exploration epic', 1, 114, 201),
    (str(random.randint(1000, 9999)), 'Back to the Future', 1985, 'An iconic time-travel adventure', 2, 116, 202),
    (str(random.randint(1000, 9999)), 'The Green Mile', 1999, 'A supernatural drama', 3, 103, 203),
    (str(random.randint(1000, 9999)), 'Django Unchained', 2012, 'A western film by Quentin Tarantino', 4, 115, 204),
    (str(random.randint(1000, 9999)), 'The Revenant', 2015, 'A survival drama film', 2, 101, 212),
    (str(random.randint(1000, 9999)), 'The Terminator', 1984, 'A classic sci-fi film', 5, 117, 206),
    (str(random.randint(1000, 9999)), 'Indiana Jones and the Raiders of the Lost Ark', 1981, 'An adventure film', 8, 118, 208)
]


for movie in movies_data:
    cursor.execute("INSERT INTO MovieDB (MovieID, Title, ReleaseYear, Description, GenreID, ActorID, DirectorID) VALUES (%s, %s, %s, %s, %s, %s, %s)", movie)


db.commit()
