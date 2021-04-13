from flask_login import current_user
from flask import Blueprint
from .models import gamesplayed
from os.path import join
from statistics import median
import pandas as pd
import numpy as np
import os
import sqlite3 as sql
import joblib as jb
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack, vstack
from lightgbm import LGBMClassifier

games = Blueprint('games', __name__)

def save_ml_models():
	
	df_gamesplayed = gamesplayed()
	df_gamesplayed = df_gamesplayed[~df_gamesplayed['IC_PLAYED'].isnull()]

	#df_gamesplayed.to_csv('E:\\OneDrive\\Documentos\\Cursos\\Mario Filho\\Games\\Web\\flask_auth_app\\project\\static\\csv\\df_gamesplayed.csv', index=False)

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
	
	# LightGBM after optimization	
	params = [0.059718899146636396, 2, 3, 0.5850311564924788, 0.8012679059209196, 688, 1, 3]
	lr = params[0]
	max_depth = params[1]
	min_child_samples = params[2]
	subsample = params[3]
	colsample_bytree = params[4]
	n_estimators = params[5]
	
	min_df = params[6]
	ngram_range = (1, params[7])
	
	title_vec = TfidfVectorizer(min_df=min_df, ngram_range=ngram_range)
	title_bow_train = title_vec.fit_transform(title_train)
	title_bow_val = title_vec.transform(title_val)
	
	from scipy.sparse import hstack, vstack

	Xtrain_wtitle = hstack([Xtrain, title_bow_train])
	Xval_wtitle = hstack([Xval, title_bow_val])
	
	mdl_lgbm = LGBMClassifier(learning_rate=lr, num_leaves=2 ** max_depth, max_depth=max_depth, min_child_samples=min_child_samples, subsample=subsample, colsample_bytree=colsample_bytree, bagging_freq=1,n_estimators=n_estimators, random_state=0, class_weight="balanced", n_jobs=6)
	mdl_lgbm.fit(Xtrain_wtitle, ytrain)
	
	p_lgbm = mdl_lgbm.predict_proba(Xval_wtitle)[:, 1]
	
	from scipy.sparse import hstack, vstack
	
	Xtrain_wtitle = hstack([Xtrain, title_bow_train])
	Xval_wtitle = hstack([Xval, title_bow_val])
	
	# Random Forest
	
	mdl_rf = RandomForestClassifier(n_estimators=1000, random_state=0, min_samples_leaf=2, class_weight="balanced", n_jobs=6)
	mdl_rf.fit(Xtrain_wtitle, ytrain)
	p_rf = mdl_rf.predict_proba(Xval_wtitle)[:, 1]
	
	# Save machine learning models
	
	# v1 = 08/03/2021
	
	jb.dump(mdl_rf, "random_forest_personalized.pkl.z")
	jb.dump(mdl_lgbm, "lgbm_personalized.pkl.z")
	jb.dump(title_vec, "title_vectorizer_personalized.pkl.z")

	return True