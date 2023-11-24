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

