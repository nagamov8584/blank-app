import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_pdf_viewer import pdf_viewer
from streamlit_extras.add_vertical_space import add_vertical_space
import time
import os
import re

### Keep uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
###

st.title("🎈 My new app")
st.write()

### FUND DB
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1Mh5iqGrvVoyaeorB8jfrJdTV4oZ_tyW7ZMiMLx5dL9w/edit"
data = conn.read(spreadsheet=url, usecols=[0, 1, 2])
###


### PDF upload
upload = st.file_uploader(
    "Загружаем файлики", accept_multiple_files=True
)

if upload is not None:
    st.session_state.uploaded_files = upload

upload_db = pd.DataFrame(columns=('old_name', 'new_name'))

for uploaded_file in st.session_state.uploaded_files:
    st.write("filename is -> ", uploaded_file.name)
### end of PDF upload   










add_vertical_space(3)






### PDF rename
statements = []
for uploaded_file in st.session_state.uploaded_files:
    if re.search(r'\d{20}', uploaded_file.name):
        print(uploaded_file.name)
        statements.append([uploaded_file.name, re.search(r'\d{20}', uploaded_file.name)[0]])
upload_db = pd.DataFrame(statements, columns=['upl_filename', 'account'])
st.dataframe(upload_db)

add_vertical_space(3)

rename_db = upload_db.merge(data ,how='left', on='account')[['account', 'upl_filename', 'file_name', 'class']]
st.dataframe(rename_db)
### end of PDF rename






add_vertical_space(3)






### Fund DB
option = st.radio("Choose one option", options=["None", "S", "W"], index=0)

if option == "S":
    st.dataframe(data[data['class'] == 'S'])
elif option == "W":
    st.dataframe(data[data['class'] == 'W'])
else:
    pass
###