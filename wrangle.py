# from __future__ import division
import itertools
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import math
from sklearn import metrics
from random import randint
from matplotlib import style
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler


def acquire_and_wrangle():
    # Read the csv file
    userlog = pd.read_csv('user_logs.csv')
    # Set datetime object as the index
    userlog = userlog.set_index(userlog.datetime)
    # Drop the original datetime column
    userlog.drop(columns='datetime',inplace=True)
    # Set 'datetime' as a datetime index.
    userlog.index = pd.to_datetime(userlog.index)
    # Convert all datetime values into datetime datatype
    userlog.end_date = pd.to_datetime(userlog.end_date)
    userlog.start_date = pd.to_datetime(userlog.start_date)
    userlog.created_at = pd.to_datetime(userlog.created_at)
    userlog.updated_at = pd.to_datetime(userlog.updated_at)
    # Drop 'deleted_at' column
    userlog.drop(columns='deleted_at', inplace=True)
    # Drop nan values(there is only one)
    userlog.dropna(inplace=True)
    userlog['program'] = userlog.program_id.map(
        {
            1.0: 'Full-Stack PHP',
            2.0: 'Full-Stack Java',
            3.0: 'Data Science',
            4.0: 'Front-End'
        })
    userlog['ds_student'] = userlog.program_id == 3
    return userlog

def get_weekly_student_activity(df):
    # Save list for Data Science students.
    datascience = list(df[df.ds_student == True].path.unique())
    # Save list for Web Development students.
    webdev = list(df[df.ds_student == False].path.unique())
    # Convert lists into sets.
    set_datascience = set(datascience)
    set_webdev = set(webdev)
    # Create a set that contains the paths that both Web Development students and Data Science students
    # are accessing.
    set1 = set_webdev.intersection(set_datascience)
    # Create a for loop that will compare the amount of visits to a certain path. 
    ds_path = []
    webdev_path = []
    for webpath in set1:
        if (df[df.ds_student == True].path == webpath).sum() > (df[df.ds_student == False].path == webpath).sum():
            ds_path.append(webpath)
        else:
            webdev_path.append(webpath)
    # Convert newly created list into a set.
    ds_path = set(ds_path)
    # Convert newly created list into a set.
    webdev_path = set(webdev_path)
    # Create a new set for Data Science paths only.
    datascience_paths = set_datascience.difference(webdev_path)
    # Create a new set for Web Development paths only.
    webdev_paths = set_webdev.difference(ds_path)
    data_science_hits = df[df.path.isin(datascience_paths)]
    webdev_hits = df[df.path.isin(webdev_paths)]
    # Create a dataframe of all Data Science curriculum hits that are from Web Development students.
    webdev_ds_hits = data_science_hits[data_science_hits.ds_student == False]
    # Create a dataframe of all Web Development curriculum hits that are from Web Development students.
    webdev_webdev_hits = webdev_hits[webdev_hits.ds_student == False]
    ## Resample by week and plot the data from above.
    #webdev_webdev_hits.resample('7d').path.count().plot(label='Webdev Curriculum')
    #webdev_ds_hits.resample('7d').path.count().plot(label='DS Curriculum')
    #plt.title('Weekly Web Development Codeup Activity')
    #plt.ylabel('Number of Page Visits')
    #plt.legend()
    # Create a dataframe of all Data Science curriculum hits that are from Data Science students.
    ds_ds_hits = data_science_hits[data_science_hits.ds_student == True]
    # Create a dataframe of all Web Development curriculum hits that are from Data Science students.
    ds_webdev_hits = webdev_hits[webdev_hits.ds_student == True]
    ## Resample by week and plot data for Data Science students.
    #(ds_webdev_hits.resample('7d').path.count()).plot(label='Webdev Curriculum')
    #(ds_ds_hits.resample('7d').path.count()).plot(label='DS Curriculum')
    #plt.title('Weekly Data Science Codeup Activity')
    #plt.ylabel('Number of Page Visits')
    #plt.legend()
    return webdev_ds_hits, webdev_webdev_hits, ds_ds_hits, ds_webdev_hits
