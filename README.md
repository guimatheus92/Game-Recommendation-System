# Game recommendation System using Machine Learning and Flask

This is a game recommendation system project that I developed to put into practice some Machine Learning techniques, so the goal is for the user to add the games that have already been played by him and add it to his profile, and later receive the recommendation of new games.

## Project structure
    .
    └── Game-Recommendation-System
        ├── __init__.py                  # setup our app
        ├── auth.py                      # the auth routes for our app
        ├── Games.db                     # our database
        ├── main.py                      # the non-auth routes for our app
        ├── models.py                    # our user personalized ML model
        ├──	games.py	             # our ML personalized models
        ├──	ml_utils.py	             # our uploader ML models
        └── templates
            ├── base.html                # contains common layout and links
            ├── index.html               # show the home page
            ├── login.html               # show the login form
            ├── profile.html             # show the profile page
            └── signup.html              # show the signup form
            └── games.html    	     # show the games page
            └── profile.html             # show the profile page
            └── 404.html                 # show the 404 error page
        └── static
            ├── img
                ├── EA-Access.png        # image for index.html
                ├── EA-Access@2x.png     # image for index.html
                ├── GitHub-Contact.png   # image for index.html
                ├── GitHub-Logo.jpg      # image for index.html
                ├── Medium-Logo.jpg      # image for index.html
            ├── css
                ├── 404.css              # contais js script for 404.html
                ├── base.css             # contais js script for base.html
                ├── index.css            # contais js script for index.html
                ├── games.css            # contais js script for games.html
                ├── profile.css          # contais js script for profile.html
            ├── js
                ├── games.js             # contais js script for games.js
                ├── index.js             # contais js script for index.js
                ├── profile.js           # contais js script for profile.js
            ├── csv       		     # contains common csv files
    
    

## Tutorial

The tutorial to use this project after deploy, can be found on [GitHub Wiki](https://github.com/guimatheus92/Game-Recommendation-System/wiki/Tutorial-on-how-to-get-a-recommendation "GitHub Wiki") page.

## Changelog

This tutorial was last updated on April 15th, 2020:

- 16/04/2021: 
	- Created subfolders `js` and `css` inside `static` folder
	- I entered the user's full name in the dropdown-menu
- 15/04/2021: Published the full project.

## Requirements

The requirements can be found in requirements.txt file also.
This project utilizes the following requirements:

    Flask==1.1.2
    Flask-Login==0.5.0
    Flask-SQLAlchemy==2.5.1
    gunicorn==20.1.0
    Jinja2==2.11.2
    joblib==1.0.1
    lightgbm==3.2.0
    numpy==1.20.2
    pandas==1.2.3
    psycopg2==2.8.6
    pylint-flask==0.6
    requests==2.25.1
    scikit-learn==0.24.1
    scikit-optimize==0.8.1
    scipy==1.6.2
    SQLAlchemy==1.4.7
    Werkzeug==1.0.1

## Conclusion

1.  Want my code? [Grab it here](http://https://github.com/guimatheus92/Game-Recommendation-System "Grab it here").
2. Want the tutorial? [Go to here](https://github.com/guimatheus92/Game-Recommendation-System/wiki/Tutorial-on-how-to-get-a-recommendation "Go to here").
3. View my app on Heroku. Cheers! ☺
4. New ideas for this app? Help me to improve it ♥
5. Want something else added to this tutorial? Add an issue to the repo.

