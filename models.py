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

try:
    qtd_rows = pd.read_sql_query('SELECT * FROM "V_GAMES"', conn)
except:
    qtd_rows = 0

def check_gamesplayed():  
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    df_checkgamesplayed = pd.read_sql_query('SELECT * FROM "USERGAMESPLAYED"', conn)
    df_checkgamesplayed.columns = map(lambda x: str(x).upper(), df_checkgamesplayed.columns)
    df_checkgamesplayed.loc[df_checkgamesplayed['ID_USER'] == current_user.id]
    conn.close()
    return df_checkgamesplayed

def gamesunplayed():
	
    userid = current_user.id    
    params = (str(userid), str(userid), str(userid))

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Create dataframe
    df_gamesunplayed = pd.read_sql_query('''select
	x.*,
	nm_game || '-' || nm_publisher || '-' || nm_genre as IMPORTANT_FEATURES
	from( 
	select distinct
	coalesce(f."ID_USER",%s) as id_user,
	b.id_game AS ID_GAME,
	b.nm_game AS NM_GAME,
	max(e.nm_publisher) as NM_PUBLISHER,
	max(c.nm_genre) as NM_GENRE,
	max(1) as qt_games,
	max(a.nr_criticscore) as NR_CRITICSCORE,
	max(a.nr_userscore) as NR_USERSCORE,
	min(d.dt_year) as DT_YEAROFRELEASE,
	max(case
	when f."IC_PLAYED" = 'NO'  then 0
	when f."IC_PLAYED" = 'YES' then 1
	else 0
	end) IC_PLAYED
	from f_gamesbyplatform a 
	left join d_games b
	on b.id_game = a.id_game
	left join d_genre c
	on c.id_genre = a.id_genre
	left join d_date d
	on d.id_date = a.id_date
	left join d_publisher e
	on e.id_publisher = a.id_publisher
	left join "USERGAMESPLAYED" AS f
	on f."ID_GAME" = a.id_game
	and f."ID_USER" = %s
	where b.linsource <> 'CARGA MANUAL'
	and d.dt_year > 0
	group by b.id_game, b.nm_game, coalesce(f."ID_USER",%s)) x
	where ic_played = 0''', conn, params = params)

    print("df_gamesunplayed: " + df_gamesunplayed)

    conn.close()

    return df_gamesunplayed

def gamesplayed():

    userid = current_user.id
    params = (str(userid), str(userid), str(userid))

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Create dataframe
    df_gamesplayed = pd.read_sql_query('''select
	x.*,
	nm_game || '-' || nm_publisher || '-' || nm_genre as IMPORTANT_FEATURES
	from( 
	select distinct
	coalesce(f."ID_USER",%s) as id_user,
	b.id_game AS ID_GAME,
	b.nm_game AS NM_GAME,
	max(e.nm_publisher) as NM_PUBLISHER,
	max(c.nm_genre) as NM_GENRE,
	max(1) as qt_games,
	max(a.nr_criticscore) as NR_CRITICSCORE,
	max(a.nr_userscore) as NR_USERSCORE,
	min(d.dt_year) as DT_YEAROFRELEASE,
	max(case
	when f."IC_PLAYED" = 'NO'  then 0
	when f."IC_PLAYED" = 'YES' then 1
	else 0
	end) IC_PLAYED
	from f_gamesbyplatform a 
	left join d_games b
	on b.id_game = a.id_game
	left join d_genre c
	on c.id_genre = a.id_genre
	left join d_date d
	on d.id_date = a.id_date
	left join d_publisher e
	on e.id_publisher = a.id_publisher
	left join "USERGAMESPLAYED" AS f
	on f."ID_GAME" = a.id_game
	and f."ID_USER" = %s
	where b.linsource <> 'CARGA MANUAL'
	and d.dt_year > 0
	group by b.id_game, b.nm_game, coalesce(f."ID_USER",%s)) x
    WHERE ic_played IS NOT NUll''', conn, params = params)

    print("df_gamesplayed: " + df_gamesplayed)
    conn.close()

    return df_gamesplayed
