import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_pdf_viewer import pdf_viewer
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
import time
import os
import re
import zipfile
import io


### Keep uploaded files
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
###

st.title("🎈 My new app  🦜")
#st.write('st.session_state.uploaded_files is EMPTY:', st.session_state.uploaded_files is None)

### FUND DB ####################################################################################
#
# Upload fund data to app from Google sheets
#
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1Mh5iqGrvVoyaeorB8jfrJdTV4oZ_tyW7ZMiMLx5dL9w/edit"
data = conn.read(spreadsheet=url, usecols=[0, 1, 2])
#
# <placeholder for future DB extension>
################################################################################################

### PDF upload and rename ######################################################################
# 1. Upload pdf files
# 2. Create df for rename preview
# 3. Rename preview button
# 4. Create df 

### 1.
upload = st.file_uploader(
    "Загружаем файлики", accept_multiple_files=True
)


if upload is not None:
    st.session_state.uploaded_files = upload
### 2.

upload_db = pd.DataFrame(columns=('old_name', 'new_name'))
   
statements = []
for uploaded_file in st.session_state.uploaded_files:
    if_found = re.search(r'\d{20}', uploaded_file.name)
    if if_found:
        #print(uploaded_file.name)
        statements.append([uploaded_file.name, if_found[0]])
upload_db = pd.DataFrame(statements, columns=['upl_filename', 'account'])
rename_db = upload_db.merge(data ,how='left', on='account')[
    ['account', 'upl_filename', 'file_name', 'class']]


################################################################################################ 

if_show_upload = st.toggle('Show upload')
if if_show_upload and not len(upload) == 0:
    st.dataframe(upload_db, use_container_width=True)
elif if_show_upload and len(upload) == 0:
    st.warning('No files uploaded')

if_show_rename = st.toggle('Show rename')
if if_show_rename and not len(upload) == 0:
    st.dataframe(rename_db, use_container_width=True)
elif if_show_rename and len(upload) == 0:
    st.warning('No files uploaded')


preview = st.button("Preview")

if 'preview_state' not in st.session_state:
    st.session_state.preview_state = False
if preview or st.session_state.preview_state:
    st.session_state.preview_state = True
    selected_fund = st.pills('test pill 💊', options=rename_db['file_name'])

    if selected_fund:
        slider_width = st.select_slider(
            "Select size",
            options=list(range(700, 2000, 100)),)
        
        pdf_viewer(upload[0].getvalue(), width=slider_width)


################################################################################################
col1, col2, col3 = st.columns(3)

upl_m = len(upload)
recogn_m = len(statements)
nonrecogn_m = upl_m - recogn_m

col1.metric(label="Файлов загружено", value=upl_m, delta=upl_m, delta_color='off')
col2.metric("Распознано", recogn_m, recogn_m)
col3.metric("Нераспознано", nonrecogn_m, nonrecogn_m, delta_color='inverse')
################################################################################################

#add_vertical_space(3)
#add_vertical_space(3)

#rename_db = upload_db.merge(data ,how='left', on='account')[['account', 'upl_filename', 'file_name', 'class']]

add_vertical_space(3)


### end of PDF rename
################################################################################################
### for Bytes objects
def recognize(faces , mirror):
    recognized = []
    for face in faces:
        if face.name in mirror:
            recognized.append(face)
    
    st.write(recognized)

    return recognized

##############################################
def create_zip(pdf_files, db=rename_db):
    zip_buffer = io.BytesIO()
    
    # Create a Zip file in memory
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:

        for pdf in pdf_files:
            try:    
                pdf_name = db[db['upl_filename'] == pdf.name]['file_name'].values[0] + '.pdf'
                st.write(pdf_name)
                zip_file.writestr(pdf_name, pdf.getvalue())
            except:
                st.markdown('''❌''' + pdf.name + ''' :red[was not added]''')
    
    zip_buffer.seek(0)  # Rewind the buffer to the beginning
    return zip_buffer


##############################################


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



if st.button('Download ZIP of PDFs'):
    if upload:
        zip_buffer = create_zip(upload)
        st.download_button(
            label="Download ZIP",
            data=zip_buffer,
            file_name="pdf_files.zip",
            mime="application/zip",
            icon=":material/barcode:"
        )
    else:
        st.warning("Please upload some PDF files first.")