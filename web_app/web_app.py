import streamlit as st
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import datasets
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier


# дистанционный мониторинг уровня артериального давления и пульса у больных  с артериальной гипертензией
def run_web_app(data_frame):
    st.write(""" # дистанционный мониторинг """)
    option = st.selectbox('Выберите id пациента', data_frame['id'].unique())
    'id выбранного пациента: ', option

    df_patient = get_patient_data(data_frame, option)
    st.write(df_patient)


def get_patient_data(df_all_patients, id_patient):
    df_patient = df_all_patients[df_all_patients["id"] == id_patient]
    df_patient = df_patient.drop(["id"], axis='columns')
    return df_patient


if __name__ == '__main__':
    dataset_name = "dataJun-18-2021-1.csv"
    df = pd.read_csv(dataset_name, sep='|')
    run_web_app(df)