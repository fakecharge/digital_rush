import streamlit as st
import pandas as pd
import altair as alt

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

    'основные показатели'
    df_stat = get_patient_stat(df_patient)
    st.write(df_stat)

    # показания пульса
    df_pulse = df_patient[['timedata', 'pulse', 'sys', 'dia']]
    df_pulse = df_pulse.set_index('timedata')
    df_pulse = df_pulse.reset_index().melt('timedata', var_name='измерения', value_name='y')
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['timedata'], empty='none')
    # The basic line
    line = alt.Chart(df_pulse).mark_line(interpolate='basis').\
        encode(x=alt.X('timedata', axis=alt.Axis(title='дата измерения'), scale=alt.Scale(zero=False)),
               y=alt.Y('y', axis=alt.Axis(title='пульс, давление'), scale=alt.Scale(domain=(50, 130))),
               color='измерения:N')
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(df_pulse).mark_point().encode(x='timedata:Q', opacity=alt.value(0),).add_selection(nearest)
    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-20).encode(text=alt.condition(nearest, 'y:Q', alt.value(' ')))
    # Draw a rule at the location of the selection
    rules = alt.Chart(df_pulse).mark_rule(color='gray').encode(x='timedata:Q',).transform_filter(nearest)
    # Put the five layers into a chart and bind the data
    c = alt.layer(line, selectors, points, rules, text).properties(width=800, height=600)
    # Put the five layers into a chart and bind the data
    st.write(c)

    if st.button('Анализ симптомов'):
        st.write("Пациенту следует поспать")


@st.cache
def get_patient_stat(df_patient):
    df_stat = df_patient.describe()
    df_stat = df_stat.drop(df_stat.index[[0]])
    df_stat = df_stat[["pulse", "dia", "sys"]]
    return df_stat


@st.cache
def get_patient_data(df_all_patients, id_patient):
    df_patient = df_all_patients[df_all_patients["id"] == id_patient]
    df_patient = df_patient.drop(["id"], axis='columns')
    return df_patient


@st.cache
def load():
    dataset_name = "dataJun-18-2021-1.csv"
    df = pd.read_csv(dataset_name, sep='|')
    return df


if __name__ == '__main__':
    df = load()
    run_web_app(df)
