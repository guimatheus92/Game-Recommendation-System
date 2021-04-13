# ml_utils.py

from flask import Blueprint, render_template, request, flash, send_file, send_from_directory
import pandas as pd
import joblib as jb
from scipy.sparse import hstack
from models import gamesunplayed

ml_utils = Blueprint('ml_utils', __name__)

def predict_api():

    df_gamesunplayed = gamesunplayed()

    mdl_rf = jb.load("random_forest_personalized.pkl.z")
    mdl_lgbm = jb.load("lgbm_personalized.pkl.z")
    title_vec = jb.load("title_vectorizer_personalized.pkl.z")

    title = df_gamesunplayed['IMPORTANT_FEATURES']

    features = pd.DataFrame(index=df_gamesunplayed.index)
    features['NR_CRITICSCORE'] = df_gamesunplayed["NR_CRITICSCORE"]
    features['DT_YEAROFRELEASE'] = df_gamesunplayed["DT_YEAROFRELEASE"]

    vectorized_title = title_vec.transform(title)     
    feature_array = hstack([features, vectorized_title])
    
    p_rf = mdl_rf.predict_proba(feature_array)[:, 1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[:, 1]

    p = 0.5*p_rf + 0.5*p_lgbm

    return p