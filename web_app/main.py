from vega_datasets import data
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

from PIL import Image
image = Image.open('heart.png')
blood_pressure_max = 120
blood_pressure_min = 50
st.sidebar.image(image)
st.sidebar.header('Добрый день _Иван_ _Иваныч_!')


def main():
    page = st.sidebar.selectbox("Выберите данные", ["Общая информация", "Частная информация"])
    if page == "Общая информация":
        st.header("Общая информация")
        st.subheader('Уведомления')
        # по умолчанию всегда смотрим на первого пациента
        id_patient = 1
        with st.form("my_form1"):
            st.write('Пациент **id3** с повышенным **пульсом**')
            submit = st.form_submit_button('Добавить в рассмотрение')
            if submit:
                id_patient = 3
        with st.form("my_form2"):

            st.write('Пациент **id2** пропускает процедуры _Метода лечения 4_')
            submit = st.form_submit_button('Добавить в рассмотрение')
            if submit:
                id_patient = 2
        df = load_data()
        st.subheader('Динамика параметров')
        id_patient = st.selectbox("Пациенты", df['id'].unique(), index=id_patient - 1)
        df_patient = get_patient_data(df, id_patient)
        draw_patient_data(df_patient)

    elif page == "Частная информация":
        df = load_data()
        st.title("Анализ результатов пациента")
        #lt = st.sidebar.slider('Просто слайдер', 0, 10, 4, 1)
        #st.checkbox('chk')
        #st.time_input('time')
        #st.multiselect('vybor', options=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon'])
        #x_axis = st.selectbox("Выберите значение x", df.columns, index=3)
        #y_axis = st.selectbox("Выберите значение y", df.columns, index=4)
        individual_analysis(df)


# дистанционный мониторинг уровня артериального давления и пульса у больных  с артериальной гипертензией
def individual_analysis(data_frame):
    id_patient = st.selectbox('Выберите id пациента', data_frame['id'].unique())
    'id выбранного пациента: ', id_patient

    df_patient = get_patient_data(data_frame, id_patient)
    s = df_patient.style.applymap(check_anomaly, subset=['pulse', 'sys', 'dia'])
    st.write(s)

    'основные показатели'
    df_stat = get_patient_stat(df_patient)
    s = df_stat.loc[['min', '25%', '50%', '75%', 'max']].style.applymap(check_anomaly)
    std = df_stat.loc[['std']]
    st.write(s)
    st.write('Среднеквадратическое отклонение измерений')
    st.write(std)

    draw_patient_data(df_patient)

    if st.button('Анализ симптомов'):
        st.write("Пациенту следует поспать")

    sentence = st.text_input('Введите рекомендации по лечению пациенту:')

    if st.button('Отправить рекомендацию'):
        if sentence:
            st.write("Рекомендация отправлена пациенту")
        else:
            st.write("Вы ничего не ввели, поле пустое")


def check_anomaly(val):
    color = 'red' if val > blood_pressure_max or val < blood_pressure_min else 'black'
    return 'color: %s' % color


def draw_patient_data(df_patient):
    # показания пульса
    df_patient_base = df_patient[['timedata', 'pulse', 'sys', 'dia']]
    df_patient_base = df_patient_base.set_index('timedata')
    df_patient_base_category = df_patient_base.reset_index().melt('timedata', var_name='измерения', value_name='y')
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['timedata'], empty='none')
    # The basic line
    line = alt.Chart(df_patient_base_category).mark_line(interpolate='basis'). \
        encode(x=alt.X('timedata', axis=alt.Axis(title='дата измерения'), scale=alt.Scale(zero=False)),
               y=alt.Y('y', axis=alt.Axis(title='пульс, давление'), scale=alt.Scale(domain=(50, 130))),
               color='измерения:N')
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(df_patient_base_category).mark_point().encode(x='timedata:Q', opacity=alt.value(0), ).add_selection(nearest)
    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-20).encode(text=alt.condition(nearest, 'y:Q', alt.value(' ')))
    # Draw a rule at the location of the selection
    rules = alt.Chart(df_patient_base_category).mark_rule(color='gray').encode(x='timedata:Q', ).transform_filter(nearest)
    # Put the five layers into a chart and bind the data
    c = alt.layer(line, selectors, points, rules, text).properties(width=700, height=500)
    # Put the five layers into a chart and bind the data
    st.write(c)


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
def load_data():
    df = pd.read_csv('dataJun-18-2021-1.csv', sep='|')
    return df


if __name__ == "__main__":
    main()


# with st.echo("below"):
#     balloons = st.text_input("Please enter awesome to see some balloons")
#     if balloons == "awesome":
#         st.balloons()
#
# st.write("This is a large text area.")
# st.text_area("A very big area", height=300)
#
# def user_input_features():
#     sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)
#     sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
#     petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
#     petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
#     data = {'sepal_length': sepal_length,
#             'sepal_width': sepal_width,
#             'petal_length': petal_length,
#             'petal_width': petal_width}
#     features = pd.DataFrame(data, index=[0])
#     return features
# df = user_input_features()
#
# st.subheader('User Input parameters')
# st.write(df)
#
# iris = datasets.load_iris()
# X = iris.data
# Y = iris.target
#
# clf = RandomForestClassifier()
# clf.fit(X, Y)
#
# prediction = clf.predict(df)
# prediction_proba = clf.predict_proba(df)
#
# st.subheader('Class labels and their corresponding index number')
# st.write(iris.target_names)
#
# st.subheader('Prediction')
# st.write(iris.target_names[prediction])
# st.write(prediction)
#
# st.subheader('Prediction Probability')
# st.write(prediction_proba)