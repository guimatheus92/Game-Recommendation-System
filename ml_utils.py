# ml_utils.py

from flask import Blueprint, render_template, request, flash, send_file, send_from_directory
import pandas as pd
from scipy.sparse import hstack
from models import gamesunplayed
from games import save_ml_models

ml_utils = Blueprint('ml_utils', __name__)

def predict_api():

    df_gamesunplayed = gamesunplayed()
    df_gamesunplayed.columns = map(lambda x: str(x).upper(), df_gamesunplayed.columns)
    #print("df_gamesplayed columns:" + str(sorted(df_gamesunplayed)))

    mdl_rf, mdl_lgbm, title_vec = save_ml_models() # Assign returned tuple

    title = df_gamesunplayed['IMPORTANT_FEATURES']

    features = pd.DataFrame(index=df_gamesunplayed.index)
    features['NR_CRITICSCORE'] = df_gamesunplayed["NR_CRITICSCORE"]
    features['DT_YEAROFRELEASE'] = df_gamesunplayed["DT_YEAROFRELEASE"]

    vectorized_title = title_vec.transform(title)     
    feature_array = hstack([features, vectorized_title])
    
    try:
        p_rf = mdl_rf.predict_proba(feature_array)[:, 1]
    except:
        p_rf = [0] * feature_array.shape[0]

    try:
        p_lgbm = mdl_lgbm.predict_proba(feature_array)[:, 1]
    except:
        p_lgbm = [0] * feature_array.shape[0]

    try:
        one = 0.5*p_rf
    except:
        one = 0.5
        
    try:
        two = 0.5*p_lgbm
    except:
        two = 0.5
    
    p = one + two

    return p
