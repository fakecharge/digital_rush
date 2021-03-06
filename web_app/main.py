import streamlit as st
import pandas as pd
import os
import numpy as np
import altair as alt
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

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
        id_patient = st.selectbox("Пациенты", df['id'].unique(), index=id_patient - 1)
        df_patient = get_patient_data(df, id_patient)
        draw_patient_data(df_patient)

    elif page == "Частная информация":
        df = load_data()
        st.title("Анализ результатов пациента")
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
        model = learn()
        x_data = df_patient[["pulse", "dia", "sys"]].head(1)
        st.write("схема лечения: ")
        result = model.predict_proba(x_data)
        result = pd.DataFrame(np.array(result), columns=["номер 1", "номер 2",  "номер 3", "номер 4"])
        result = result.rename(index={0: "эффективность"})
        s = result.style.format("{:.2%}", na_rep="-")
        st.write(s)

    sentence = st.text_input('Введите рекомендации по лечению пациенту:')

    if st.button('Отправить рекомендацию'):
        if sentence:
            st.write("Рекомендация отправлена пациенту")
        else:
            st.write("Вы ничего не ввели, поле пустое")

    if st.button("Сохранить данные"):
        path = "C:\\inNINO\\"
        file_name = 'patient_data_id_' + str(id_patient) + ".xlsx"
        full_path = path + file_name
        if not os.path.exists(path):
            os.mkdir(path)
        df_patient.to_excel(full_path)
        st.write("файл сохранен по следующему пути: " + full_path)


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


def learn():
    dt = pd.read_csv('Book.csv', sep=';')
    X_train, X_test, y_train, y_test = train_test_split(dt.drop('diag', 1), dt['diag'], test_size=.03, random_state=10)
    model = RandomForestClassifier(n_estimators=50, max_depth=7)
    model.fit(X_train, y_train)
    return model


if __name__ == "__main__":
    main()
