from unicodedata import numeric
from git import GitCommandNotFound
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

db_file = 'eval_data.db'
@st.cache
def data_by_user(name):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM eval_data_tbl")
    rows = cur.fetchall()
    #convert rows to a dataframe
    df = pd.DataFrame(rows)
    df.columns = ['name', 'moc', 'hra', 'attendance']
    user_df = df.copy()
    mask = (user_df.name != name) & (user_df.name != 'Average')
    user_df.loc[mask, 'name'] = ''
    # user_df.style.format('{:.2}')
    return user_df, df
#plotting
def data_plot(df, stat='moc'):
    fig = px.scatter(
        x=df["name"],
        y=df[stat],
        text=df[stat],
        
    )
    fig.update_layout(
        xaxis_title="NP",
        yaxis_title=stat,
    )

    fig.update_traces(textposition='top center')
    return fig
# moc_plot = data_plot(user_data, 'moc')
# hra_plot = data_plot(user_data, 'hra')
# attendance_plot = data_plot(user_data, 'attendance')

#add a login form
st.sidebar.header("Login")
name = st.sidebar.text_input("Your name", "", key="name") #the key assigns the word name in session variable to the input here
password = st.sidebar.text_input("Your password", "", type="password")
login_name = st.session_state.name
user_df, df = data_by_user(name)
all_data = ['Gina','Nadia', 'Lisa', 'Michael']
plot_area = st.empty()


if st.sidebar.button("Login"):
    if login_name in all_data:
        with st.expander("Total NP Data"):
            st.dataframe(df.style.format(subset=df.columns[1:], formatter="{:.2f}"))
        plot_area = st.plotly_chart(data_plot(df))
    else:
        with st.expander("Your Data"):
            st.dataframe(user_df.style.format(subset=user_df.columns[1:], formatter="{:.2f}"))
        plot_area = st.plotly_chart(data_plot(user_df))

# st.header("Select a stat")
# stat = st.radio("Stat", ("moc", "hra", "attendance"))

#create empty element




# st.write(f'this is the name from the session {login_name}')
# This exists now:
# st.write(st.session_state.name)

# placeholder = st.empty()

# # Replace the placeholder with some text:
# placeholder.text("Hello")

# # Replace the text with a chart:
# placeholder.line_chart({"data": [1, 5, 2, 6]})

# # Replace the chart with several elements:
# with placeholder.container():
#      st.write("This is one element")
#      st.write("This is another")

# Clear all those elements:
# placeholder.empty()

# st.write(f'where the heck is {st.session_state.name}?')

# def form_callback():
#     st.write(st.session_state.my_slider)
#     st.write(st.session_state.my_checkbox)

# with st.form(key='my_form'):
#     slider_input = st.slider('My slider', 0, 10, 5, key='my_slider')
#     checkbox_input = st.checkbox('Yes or No', key='my_checkbox')
#     submit_button = st.form_submit_button(label='Submit', on_click=form_callback)