# models.py
import pandas as pd
import sqlite3 as sql
from flask_login import UserMixin, current_user
from . import db

def get_db_connection():
    conn = sql.connect('Games.db')
    conn.row_factory = sql.Row    
    return conn

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    created = db.Column(db.Date)

class USERGAMESPLAYED(db.Model):
    ID_PLAYED = db.Column(db.Integer, primary_key=True)
    ID_USER = db.Column(db.Integer)
    ID_GAME = db.Column(db.Integer)
    NM_GAME = db.Column(db.String(100))
    IC_PLAYED = db.Column(db.String(20))
    DT_PLAYED = db.Column(db.Date)

class V_GAMES(db.Model):
    ID_GAME = db.Column(db.Integer)
    NM_GAME = db.Column(db.String(100), primary_key=True)
    NM_GENRE = db.Column(db.String(100))
    NR_CRITICSCORE = db.Column(db.Integer)
    DT_YEAROFRELEASE = db.Column(db.String(100))

conn = get_db_connection()
qtd_rows = conn.execute('SELECT * FROM V_GAMES').fetchall()

def check_gamesplayed():
    userid = current_user.id    
    params = (str(userid))
    conn = get_db_connection()
    df_checkgamesplayed = pd.read_sql_query('SELECT * FROM USERGAMESPLAYED WHERE ID_USER = ?', conn, params = params)
    conn.close()
    return df_checkgamesplayed

def gamesunplayed():

    #params = ("1", "1")    
    userid = current_user.id    
    params = (str(userid), str(userid))

    conn = get_db_connection()

    # Create dataframe
    df_gamesunplayed = pd.read_sql_query('''SELECT
    x.*,
    NM_GAME || '-' || NM_PUBLISHER || '-' || NM_GENRE AS IMPORTANT_FEATURES
    FROM( 
    SELECT DISTINCT
    IFNULL(f.ID_USER,?) AS ID_USER,
    b.ID_GAME,
    b.NM_GAME,
    MAX(e.NM_PUBLISHER) AS NM_PUBLISHER,
    MAX(c.NM_GENRE) AS NM_GENRE,
    MAX(1) AS QT_GAMES,
    MAX(a.NR_CRITICSCORE) AS NR_CRITICSCORE,
    MAX(a.NR_USERSCORE) AS NR_USERSCORE,
    MIN(d.DT_YEAR) AS DT_YEAROFRELEASE,
    MAX(CASE
    WHEN f.IC_PLAYED = 'NO'  THEN 0
    WHEN f.IC_PLAYED = 'YES' THEN 1
    ELSE 0
    END) IC_PLAYED
    FROM F_GAMESBYPLATFORM a 
    LEFT JOIN D_GAMES b
    ON b.ID_GAME = a.ID_GAME
    LEFT JOIN D_GENRE c
    ON c.ID_GENRE = a.ID_GENRE
    LEFT JOIN D_DATE d
    ON d.ID_DATE = a.ID_DATE
    LEFT JOIN D_PUBLISHER e
    ON e.ID_PUBLISHER = a.ID_PUBLISHER
    LEFT JOIN USERGAMESPLAYED f
    ON f.ID_GAME = a.ID_GAME
    AND f.ID_USER = ?
    WHERE b.LINSOURCE <> 'CARGA MANUAL'
    AND d.DT_YEAR > 0
    GROUP BY b.ID_GAME, b.NM_GAME) x
    WHERE IC_PLAYED = 0''', conn, params = params)

    conn.close()

    return df_gamesunplayed

def gamesplayed():

    #params = ("1", "1")
    userid = current_user.id
    params = (str(userid), str(userid))

    conn = get_db_connection()

    # Create dataframe
    df_gamesplayed = pd.read_sql_query('''SELECT
    x.*,
    NM_GAME || '-' || NM_PUBLISHER || '-' || NM_GENRE AS IMPORTANT_FEATURES
    FROM( 
    SELECT DISTINCT
    IFNULL(f.ID_USER,?) AS ID_USER,
    b.ID_GAME,
    b.NM_GAME,
    MAX(e.NM_PUBLISHER) AS NM_PUBLISHER,
    MAX(c.NM_GENRE) AS NM_GENRE,
    MAX(1) AS QT_GAMES,
    MAX(a.NR_CRITICSCORE) AS NR_CRITICSCORE,
    MAX(a.NR_USERSCORE) AS NR_USERSCORE,
    MIN(d.DT_YEAR) AS DT_YEAROFRELEASE,
    MAX(CASE
    WHEN f.IC_PLAYED = 'NO'  THEN 0
    WHEN f.IC_PLAYED = 'YES' THEN 1
    ELSE 0
    END) IC_PLAYED
    FROM F_GAMESBYPLATFORM a 
    LEFT JOIN D_GAMES b
    ON b.ID_GAME = a.ID_GAME
    LEFT JOIN D_GENRE c
    ON c.ID_GENRE = a.ID_GENRE
    LEFT JOIN D_DATE d
    ON d.ID_DATE = a.ID_DATE
    LEFT JOIN D_PUBLISHER e
    ON e.ID_PUBLISHER = a.ID_PUBLISHER
    LEFT JOIN USERGAMESPLAYED f
    ON f.ID_GAME = a.ID_GAME
    AND f.ID_USER = ?
    WHERE b.LINSOURCE <> 'CARGA MANUAL'
    AND d.DT_YEAR > 0
    GROUP BY b.ID_GAME, b.NM_GAME) x
    WHERE IC_PLAYED IS NOT NUll''', conn, params = params)

    conn.close()

    return df_gamesplayed