import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time
import os

### Keep uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
###

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


upload = st.file_uploader(
    "Загружаем файлики", accept_multiple_files=True
)

if upload is not None:
    st.session_state.uploaded_files = upload

upload_db = pd.DataFrame(columns=('old_name', 'new_name'))

for uploaded_file in st.session_state.uploaded_files:
    #bytes_data = uploaded_file.read()
    st.write("filename is -> ", uploaded_file.name)
    #st.write(bytes_data)


#with st.sidebar:
#    with st.echo():
#        st.write("This code will be printed to the sidebar.")

#    with st.spinner("Loading..."):
#        time.sleep(1)
#    st.success("Done!")

option = st.radio("Choose one option", options=["None", "S", "W"], index=1)

conn = st.connection("gsheets", type=GSheetsConnection)

url = "https://docs.google.com/spreadsheets/d/1Mh5iqGrvVoyaeorB8jfrJdTV4oZ_tyW7ZMiMLx5dL9w/edit"

if option == "S":
    data = conn.read(spreadsheet=url, usecols=[0, 1, 2])
    st.dataframe(data[data['class'] == 'S'])
elif option == "W":
    data = conn.read(spreadsheet=url, usecols=[0, 1, 2])
    st.dataframe(data[data['class'] == 'W'])
else:
    pass


#df = conn.read()

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.Account} has a :{row.File_name}:")

#df = conn.read(worksheet="Sheet1")

#st.dataframe(df)