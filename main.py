# main.py

from flask import Blueprint, render_template, request, flash, send_file, send_from_directory
from flask_login import login_required, current_user
from models import V_GAMES, USERGAMESPLAYED, qtd_rows, User, gamesunplayed, gamesplayed, conn
from __init__ import db
from ml_utils import predict_api
from games import save_ml_models
import datetime
import pandas as pd
import os

main = Blueprint('main', __name__)

def check_gamesplayed():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    df_checkgamesplayed = cursor.execute('SELECT * FROM "USERGAMESPLAYED" WHERE "ID_USER" = %s', [str(current_user.id)])
    print(cursor.execute('SELECT * FROM "USERGAMESPLAYED" WHERE "ID_USER" = %s', [str(current_user.id)]))
    print(df_checkgamesplayed)
    conn.close()
    return df_checkgamesplayed

def get_recommendation():
    df_gamesunplayed = gamesunplayed()
    df_gamesunplayed.columns = map(lambda x: str(x).upper(), df_gamesunplayed.columns)
    p = predict_api()
    output = {"ID_USER": df_gamesunplayed['ID_USER'], "ID_GAME": df_gamesunplayed['ID_GAME'], "NM_GAME": df_gamesunplayed['NM_GAME'], "NM_PUBLISHER": df_gamesunplayed['NM_PUBLISHER'], "NM_GENRE": df_gamesunplayed['NM_GENRE'], "QT_GAMES": df_gamesunplayed['QT_GAMES'], "NR_CRITICSCORE": df_gamesunplayed['NR_CRITICSCORE'], "DT_YEAROFRELEASE": df_gamesunplayed['DT_YEAROFRELEASE'], "IC_PLAYED": df_gamesunplayed['IC_PLAYED'], "Score": p}
    recommendations_df = pd.DataFrame(output)
    recommendations_df = recommendations_df.sort_values('Score',ascending=False)
    recommendations_df = recommendations_df.reset_index(drop=True)
    return recommendations_df

@main.route('/')
def index():
    if current_user.is_authenticated:
        if " " not in current_user.name:
            first_name = current_user.name.rsplit(' ', 1)[0]
            last_name = " "
        else:
            first_name = current_user.name.rsplit(' ', 1)[0]
            last_name = current_user.name.rsplit(' ', 1)[1]
        return render_template('index.html', first_name=first_name, last_name=last_name)
    else:
        return render_template('index.html')

@main.route('/donwloadrecommendation', methods=('GET', 'POST'))
def donwloadrecommendation():
    if request.method =='GET':    
        df_checkgamesplayed = check_gamesplayed()         
        if df_checkgamesplayed is None:
            return None
        else:
            recommendations_df = get_recommendation()
            recommendations_df.to_csv(r'recommendations.csv', index=False)  
            recommendations_file = (r'recommendations.csv')  
            return send_file(recommendations_file, as_attachment=True)

@main.route('/donwloadprofile', methods=('GET', 'POST'))
def donwloadprofile():
    if request.method =='GET':
        df_checkgamesplayed = check_gamesplayed()  
        if df_checkgamesplayed is None:
            return None
        else:            
            profile_table = db.session.query(USERGAMESPLAYED.ID_USER, USERGAMESPLAYED.NM_GAME, V_GAMES.DT_YEAROFRELEASE, V_GAMES.NM_GENRE, V_GAMES.NR_CRITICSCORE).select_from(USERGAMESPLAYED).join(V_GAMES, V_GAMES.ID_GAME == USERGAMESPLAYED.ID_GAME).filter(USERGAMESPLAYED.ID_USER==current_user.id)
            profile_df = pd.DataFrame(profile_table, columns=['ID_USER', 'NM_GAME', 'DT_YEAROFRELEASE', 'NM_GENRE', 'NR_CRITICSCORE'])
            profile_df.to_csv(r'profile.csv', index=False)
            profile = (r'profile.csv')
            return send_file(profile, as_attachment=True)

@main.route('/profile/<int:page_num>', methods=('GET', 'POST'))
@login_required
def profile(page_num):    
    profile = db.session.query(USERGAMESPLAYED.ID_USER, USERGAMESPLAYED.NM_GAME, V_GAMES.DT_YEAROFRELEASE, V_GAMES.NM_GENRE, V_GAMES.NR_CRITICSCORE).select_from(USERGAMESPLAYED).join(V_GAMES, V_GAMES.ID_GAME == USERGAMESPLAYED.ID_GAME).filter(USERGAMESPLAYED.ID_USER==current_user.id).paginate(per_page=len(qtd_rows), page=page_num, error_out=True)    

    if " " not in current_user.name:
        first_name = current_user.name.rsplit(' ', 1)[0]
        last_name = " "
    else:
        first_name = current_user.name.rsplit(' ', 1)[0]
        last_name = current_user.name.rsplit(' ', 1)[1]  
    
    df_checkgamesplayed = check_gamesplayed()
    print(df_checkgamesplayed)

    if df_checkgamesplayed is None:
        recommendations_df = pd.DataFrame()
        recommendations_df[["ID_USER", "ID_GAME", "NM_GAME", "NM_PUBLISHER", "NM_GENRE", "QT_GAMES", "NR_CRITICSCORE", "DT_YEAROFRELEASE", "IC_PLAYED", "Score"]] = ""
        disable = True
    else:
        disable = False
        recommendations_df = get_recommendation()

    if request.method =='POST':
        if request.form.getlist('delete_checkbox'):            
            for id in request.form.getlist('delete_checkbox'):
                # Delete the games that were checked and commit in the database
                #USERGAMESPLAYED.query.filter_by(NM_GAME=id, ID_USER=current_user.id).delete(synchronize_session='fetch')                                    
                cursor = conn.cursor()
                cursor.execute('DELETE FROM "USERGAMESPLAYED" WHERE "NM_GAME" = %s AND "ID_USER" = %s', (id, current_user.id))
                conn.commit()
                #db.session.commit()
            recommendations_df = get_recommendation()
            profile = db.session.query(USERGAMESPLAYED.ID_USER, USERGAMESPLAYED.NM_GAME, V_GAMES.DT_YEAROFRELEASE, V_GAMES.NM_GENRE, V_GAMES.NR_CRITICSCORE).select_from(USERGAMESPLAYED).join(V_GAMES, V_GAMES.ID_GAME == USERGAMESPLAYED.ID_GAME).filter(USERGAMESPLAYED.ID_USER==current_user.id).paginate(per_page=len(qtd_rows), page=page_num, error_out=True)
            return render_template('profile.html', name=current_user.name, profile=profile, first_name=first_name, last_name=last_name, len = len(recommendations_df), recommendations_profile=recommendations_df, disable=disable)
            flash('Games have been successfully deleted from your profile.')

        if not request.form.getlist('delete_checkbox'):            
            flash('You have to check at least one game to delete from your profile!')
            return render_template('profile.html', name=current_user.name, profile=profile, first_name=first_name, last_name=last_name, len = len(recommendations_df), recommendations_profile=recommendations_df, disable=disable)
    
    return render_template('profile.html', name=current_user.name, profile=profile, first_name=first_name, last_name=last_name, len = len(recommendations_df), recommendations_profile=recommendations_df, disable=disable)

# Depois de logado, o usuário poderá adicionar os jogos que desejar
@main.route('/games/<int:page_num>', methods=('GET', 'POST'))
def games(page_num):
    if current_user.is_authenticated:        
        subquery = db.session.query(USERGAMESPLAYED.NM_GAME).filter(USERGAMESPLAYED.ID_USER==current_user.id).subquery()
        games = db.session.query(V_GAMES).filter(V_GAMES.NM_GAME.notin_(subquery)).paginate(per_page=len(qtd_rows), page=page_num, error_out=True)        
        
        if " " not in current_user.name:
            first_name = current_user.name.rsplit(' ', 1)[0]
            last_name = " "
        else:
            first_name = current_user.name.rsplit(' ', 1)[0]
            last_name = current_user.name.rsplit(' ', 1)[1]

        if request.method =='POST':
            if request.form.getlist('one_checkbox'):
                    for id in request.form.getlist('one_checkbox'):
                        game = V_GAMES.query.filter_by(NM_GAME=id).first()
                        ID_USER = current_user.id
                        ID_GAME = game.ID_GAME
                        NM_GAME = id
                        IC_PLAYED = "YES"
                        SYSDATE = datetime.datetime.now()
                        # add games to the profile
                        addprofile = USERGAMESPLAYED(ID_USER=ID_USER, ID_GAME=ID_GAME, NM_GAME=NM_GAME, IC_PLAYED=IC_PLAYED, DT_PLAYED=SYSDATE)                        
                        db.session.add(addprofile)
                        db.session.commit()

                    subquery = db.session.query(USERGAMESPLAYED.NM_GAME).filter(USERGAMESPLAYED.ID_USER==current_user.id).subquery()
                    games = db.session.query(V_GAMES).filter(V_GAMES.NM_GAME.notin_(subquery)).paginate(per_page=len(qtd_rows), page=page_num, error_out=True)                                        
                    flash('Games have been successfully added to your profile.')                    
                    return render_template('games.html', games=games, first_name=first_name, last_name=last_name)

            if not request.form.getlist('one_checkbox'):            
                flash('You have to check at least one game to add to your profile!')
                return render_template('games.html', games=games, first_name=first_name, last_name=last_name)
        
        return render_template('games.html', games=games, first_name=first_name, last_name=last_name)
    
    else:
        if request.method =='POST':
            flash('You have to sign in to submit games to your profile!')  
        games = db.session.query(V_GAMES).paginate(per_page=len(qtd_rows), page=page_num, error_out=True)
        return render_template('games.html', games=games)    

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
