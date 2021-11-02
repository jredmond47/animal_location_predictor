import json

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import seaborn as sn
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os

pd.set_option('display.max_columns', None)


def missing_data(data):
    # Count number of missing value in a column
    total = data.isnull().sum()

    # Get Percentage of missing values
    percent = (data.isnull().sum() / data.isnull().count() * 100)
    temp = pd.concat([total, percent], axis=1, keys=['Total', 'Percent(%)'])

    # Create a Type column, that indicates the data-type of the column.
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    temp['Types'] = types

    return (np.transpose(temp))


if __name__ == '__main__':

    file_input = 'gps_events_s21231406_i24563363_ss653'

    path = os.path.join('data', 'movebank', f'{file_input}.csv')

    data = pd.read_csv(path)

    data[['year', 'week', 'weekday']] = pd.to_datetime(data.timestamp).dt.isocalendar()
    data['week_year'] = data.year.astype(str) + '-' + data.week.astype(str)
    data['weekday_year'] = data.year.astype(str) + '-' + data.weekday.astype(str)

    usable_columns = ['location_lat', 'location_long', 'ground_speed', 'heading', 'week', 'weekday', 'eobs_temperature', 'eobs_speed_accuracy_estimate']

    model_data = data[usable_columns].dropna().drop_duplicates()

    X = model_data[['ground_speed', 'heading', 'week', 'weekday', 'eobs_temperature', 'eobs_speed_accuracy_estimate']]

    predictions = defaultdict(dict)

    for pred_var in ['location_lat', 'location_long']:
        y = model_data[pred_var]

        seed = 101

        np.random.seed(101)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        print(f'--- running model for: {pred_var}')

        clf = RandomForestRegressor()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        print(f'--- finished {pred_var}')

        actual = y_test
        predicted = y_pred

        r2 = metrics.r2_score(actual, predicted)
        N = actual.shape[0]
        p = 3
        x = (1 - r2)
        y = (N - 1) / (N - p - 1)
        adj_r2 = (1 - (x * y))
        mape = metrics.mean_absolute_percentage_error(y_test, y_pred)

        predictions[pred_var] = {
            'seed': seed
            , 'metrics': {
                'r2': r2
                , 'adj_r2': adj_r2
                , 'mape': mape
            }
        }

    pred_json = json.dumps(predictions)
    json_file = open(f'pred_{file_input}.json', 'w')
    json_file.write(pred_json)
    json_file.close()

    # filename='gulls50.csv'
    # data_in=pd.read_csv(filename, sep=',',header=0)
    # data_in.columns
    #
    # data_std=data_in
    #
    # data_transform=data_std.iloc[:, np.r_[10:213]]
    #
    # # Step 1: Classification
    #
    # #Normalize the input variables
    #
    # from sklearn import preprocessing
    #
    # scaler_in = preprocessing.StandardScaler()
    #
    # scaler_in.fit(data_transform)
    #
    # data_transform=scaler_in.transform(data_transform)
    #
    # scaler_out = preprocessing.StandardScaler()
    # scaler_out.fit(data_in[['vx','vy']])
    # data_out_transform=scaler_out.transform(data_in[['vx','vy']])
    #
    # id1=np.where(data_std['state']==1)[0]
    # id2=np.where(data_std['state']==2)[0]
    # id4=np.where(data_std['state']==4)[0]
    # id5=np.where(data_std['state']==5)[0]
    #
    # data_std1=data_std[data_std['state']==1]
    # data_std2=data_std[data_std['state']==2]
    # data_std4=data_std[data_std['state']==4]
    # data_std5=data_std[data_std['state']==5]
    #
    # data_transform1=data_transform[id1]
    # data_transform2=data_transform[id2]
    # data_transform4=data_transform[id4]
    # data_transform5=data_transform[id5]
    #
    # data_out_transform1=data_out_transform[id1]
    # data_out_transform2=data_out_transform[id2]
    # data_out_transform4=data_out_transform[id4]
    # data_out_transform5=data_out_transform[id5]
    #
    # fold_mspe=np.zeros(5)
    #
    #
    # for f in range(1,6,1):
    #
    #  #Fit models using the data not in fold
    #  #Classification model for state
    #  idx_nofold=np.where((data_std['fold']==f) & (data_std['common']==1))[0]
    #  idx_fold=np.where(data_std['fold']!=f)[0]
    #  fold_vel_act=data_in[['vx','vy']].values[idx_fold]
    #  fold_vel_pred=np.zeros((fold_vel_act.shape[0], 2))
    #  fold_in=data_transform[idx_fold]
    #  fold_out=data_transform[idx_nofold]
    #  classfr = RandomForestClassifier( max_depth=9, min_samples_split=2, min_samples_leaf=3,
    #                               n_estimators=5, n_jobs=-2)
    #  classfr.fit(fold_in, data_in['state'].values[idx_fold])
    #  #Velocity model for state 1
    #  idx_nofold1=np.where((data_std1['fold']==f) & (data_std1['common']==1))[0]
    #  idx_fold1=np.where(data_std1['fold']!=f)[0]
    #  fold_in1=data_transform1[idx_fold1]
    #  fold_out1=data_transform1[idx_nofold1]
    #  regr1 = RandomForestRegressor( max_depth=9, min_samples_split=10, min_samples_leaf=3,
    #                               n_estimators=5, n_jobs=-1)
    #  regr1.fit(fold_in1, data_out_transform1[idx_fold1])
    #  #Velocity model for state 2
    #  idx_nofold2=np.where((data_std2['fold']==f) & (data_std2['common']==1))[0]
    #  idx_fold2=np.where(data_std2['fold']!=f)[0]
    #  fold_in2=data_transform2[idx_fold2]
    #  fold_out2=data_transform2[idx_nofold2]
    #  regr2 = RandomForestRegressor( max_depth=2, min_samples_split=2, min_samples_leaf=5,
    #                               n_estimators=5, n_jobs=-1)
    #  regr2.fit(fold_in2, data_out_transform2[idx_fold2])
    #  #Velocity model for state 4
    #  idx_nofold4=np.where((data_std4['fold']==f) & (data_std4['common']==1))[0]
    #  idx_fold4=np.where(data_std4['fold']!=f)[0]
    #  fold_in4=data_transform4[idx_fold4]
    #  fold_out4=data_transform4[idx_nofold4]
    #  regr4 = RandomForestRegressor( max_depth=7, min_samples_split=4, min_samples_leaf=1,
    #                               n_estimators=5, n_jobs=-1)
    #  regr4.fit(fold_in4, data_out_transform4[idx_fold4])
    #  #Velocity model for state 5
    #  idx_nofold5=np.where((data_std5['fold']==f) & (data_std5['common']==1))[0]
    #  idx_fold5=np.where(data_std5['fold']!=f)[0]
    #  fold_in5=data_transform5[idx_fold5]
    #  fold_out5=data_transform5[idx_nofold5]
    #  regr5 = RandomForestRegressor( max_depth=4, min_samples_split=8, min_samples_leaf=1,
    #                               n_estimators=5, n_jobs=-1)
    #  regr5.fit(fold_in5, data_out_transform5[idx_fold5])
    #  #Predict state for all in fold==f
    #  test_pred=classfr.predict(fold_out)
    #  for j in range(test_pred.shape[0]):
    #     if test_pred[j]==1:
    #         fold_vel_pred[j,:]=scaler_out.inverse_transform(regr1.predict(fold_out[j:(j+1),:]))
    #     elif test_pred[j]==2:
    #         fold_vel_pred[j,:]=scaler_out.inverse_transform(regr2.predict(fold_out[j:(j+1),:]))
    #     elif test_pred[j]==4:
    #         fold_vel_pred[j,:]=scaler_out.inverse_transform(regr4.predict(fold_out[j:(j+1),:]))
    #     else:
    #         fold_vel_pred[j,:]=scaler_out.inverse_transform(regr5.predict(fold_out[j:(j+1),:]))
    #  fold_mspe[f]=np.mean(((fold_vel_pred.iloc[:,0]-fold_vel_act.iloc[:,0])**2+(fold_vel_pred.iloc[:,1]-fold_vel_act.iloc[:,1])**2)**0.5)
    #  np.save('RFlag50best.npy', fold_mspe)
    #
    #
