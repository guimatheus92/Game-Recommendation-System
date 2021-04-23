from flask import Blueprint, render_template, request, flash, send_file, send_from_directory
import pandas as pd
from models import gamesunplayed
from flask_login import current_user
from models import gamesplayed
from os.path import join
from statistics import median
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack, vstack
from lightgbm import LGBMClassifier


games = Blueprint('games', __name__)

def save_ml_models():
    
    df_gamesplayed = gamesplayed()
    df_gamesplayed.columns = map(lambda x: str(x).upper(), df_gamesplayed.columns)
    #print(sorted(df_gamesplayed))
    
    # Features
    features = pd.DataFrame(index=df_gamesplayed.index)
    
    # Feature if the user has played the game or not, 1 = yes and 0 = no
    y = df_gamesplayed["IC_PLAYED"].copy()	
    
    # Separates the necessary features of the dataframe for training
    features["NR_CRITICSCORE"] = df_gamesplayed["NR_CRITICSCORE"]
    features["DT_YEAROFRELEASE"] = df_gamesplayed["DT_YEAROFRELEASE"]
    
    mask_train = df_gamesplayed['DT_YEAROFRELEASE'] < median(features["DT_YEAROFRELEASE"])
    mask_val = (df_gamesplayed['DT_YEAROFRELEASE'] >= median(features["DT_YEAROFRELEASE"]))
    
    Xtrain, Xval = features[mask_train], features[mask_val]
    ytrain, yval = y[mask_train], y[mask_val]
    
    title_train = df_gamesplayed[mask_train]['IMPORTANT_FEATURES']
    title_val = df_gamesplayed[mask_val]['IMPORTANT_FEATURES']
        
    title_vec = TfidfVectorizer(min_df=4, ngram_range=(1,3))
    title_bow_train = title_vec.fit_transform(title_train)
    title_bow_val = title_vec.transform(title_val)
    
    from scipy.sparse import hstack, vstack
    
    Xtrain_wtitle = hstack([Xtrain, title_bow_train])
    Xval_wtitle = hstack([Xval, title_bow_val])
        
    mdl_lgbm = LGBMClassifier(random_state=0, class_weight="balanced", n_jobs=6)
    mdl_lgbm.fit(Xtrain_wtitle, ytrain)
    
    from scipy.sparse import hstack, vstack
    
    Xtrain_wtitle = hstack([Xtrain, title_bow_train])
    Xval_wtitle = hstack([Xval, title_bow_val])
    
    # Random Forest	
    mdl_rf = RandomForestClassifier(n_estimators=1000, random_state=0, min_samples_leaf=2, class_weight="balanced", n_jobs=6)
    mdl_rf.fit(Xtrain_wtitle, ytrain)
    
    df_gamesunplayed = gamesunplayed()
    df_gamesunplayed.columns = map(lambda x: str(x).upper(), df_gamesunplayed.columns)
    #print("df_gamesplayed columns:" + str(sorted(df_gamesunplayed)))

    #mdl_rf, mdl_lgbm, title_vec = save_ml_models() # Assign returned tuple

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
