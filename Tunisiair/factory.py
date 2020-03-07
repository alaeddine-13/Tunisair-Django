import requests
import os, sys
import datetime
from ml_models.predictive_maintenance import train_model as predictive_maintenance_train_model
import threading


from joblib import load
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import pandas as pd
import  sqlalchemy as db



DB= os.getenv("DB")
engine = db.create_engine(DB, use_batch_mode=True)



predictive_maintenance_model = load('ml_models/predictive_maintenance.joblib')

