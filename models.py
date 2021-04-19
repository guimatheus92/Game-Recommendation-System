# models.py
import pandas as pd
import sqlite3 as sql
import os
import psycopg2
from flask_login import UserMixin, current_user
from __init__ import db
from sqlalchemy import create_engine

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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

qtd_rows = pd.read_sql_query('SELECT * FROM "v_games"', conn)

def check_gamesplayed():
    userid = current_user.id
    params = (str(userid))
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    df_checkgamesplayed = pd.read_sql_query('SELECT * FROM "usergamesplayed" WHERE "id_user" = %s', conn, params=params)
    #df_checkgamesplayed = conn.execute("SELECT * FROM USERGAMESPLAYED WHERE ID_USER=:id",{"id": params}).fetchall()
    conn.close()
    return df_checkgamesplayed

def gamesunplayed():

    #params = ("1", "1")    
    userid = current_user.id    
    params = (str(userid), str(userid))

    # Create dataframe
    df_gamesunplayed = pd.read_sql_query('''select
	x.*,
	nm_game || '-' || nm_publisher || '-' || nm_genre as important_features
	from( 
	select distinct
	ifnull(f."id_user",%s) as id_user,
	b.id_game,
	b.nm_game,
	max(e.nm_publisher) as nm_publisher,
	max(c.nm_genre) as nm_genre,
	max(1) as qt_games,
	max(a.nr_criticscore) as nr_criticscore,
	max(a.nr_userscore) as nr_userscore,
	min(d.dt_year) as dt_yearofrelease,
	max(case
	when f."ic_played" = 'no'  then 0
	when f."ic_played" = 'yes' then 1
	else 0
	end) ic_played
	from f_gamesbyplatform a 
	left join d_games b
	on b.id_game = a.id_game
	left join d_genre c
	on c.id_genre = a.id_genre
	left join d_date d
	on d.id_date = a.id_date
	left join d_publisher e
	on e.id_publisher = a.id_publisher
	left join "usergamesplayed" f
	on f."id_game" = a.id_game
	and f."id_user" = %s
	where b.linsource <> 'carga manual'
	and d.dt_year > 0
	group by b.id_game, b.nm_game) x
	where ic_played = 0''', conn, params = params)

    conn.close()

    return df_gamesunplayed

def gamesplayed():

    #params = ("1", "1")
    userid = current_user.id
    params = (str(userid), str(userid))

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
