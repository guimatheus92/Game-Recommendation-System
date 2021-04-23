from flask_login import current_user
from flask import Blueprint
from models import gamesplayed
from os.path import join
from statistics import median
import pandas as pd
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
	print(sorted(df_gamesplayed))
	
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
	
	try:
		p_lgbm = mdl_lgbm.predict_proba(Xval_wtitle)[:, 1]
	except:
		p_lgbm = [0] * Xval_wtitle.shape[0]
	
	from scipy.sparse import hstack, vstack
	
	Xtrain_wtitle = hstack([Xtrain, title_bow_train])
	Xval_wtitle = hstack([Xval, title_bow_val])
	
	# Random Forest
	
	mdl_rf = RandomForestClassifier(n_estimators=1000, random_state=0, min_samples_leaf=2, class_weight="balanced", n_jobs=6)
	mdl_rf.fit(Xtrain_wtitle, ytrain)

	try:
		p_rf = mdl_rf.predict_proba(Xval_wtitle)[:, 1]
	except:
		p_rf = [0] * Xval_wtitle.shape[0]

	return mdl_rf, mdl_lgbm, title_vec
