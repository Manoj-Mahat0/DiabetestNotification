import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from pushbullet import Pushbullet

st.title("Read Google Sheet as DataFrame")

API_KEY = "o.FBicbL6OkC88g691kfxaVrajxWCv3x9d"
filename = 'resolution.txt'

with open(filename, mode='r') as f:
    text = f.read()

pb = Pushbullet(API_KEY)

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Sheet1", usecols=list(range(8)), ttl=5)
existing_data = existing_data.dropna(how="all")


with st.form(key="vendor_form"):
    Pregnancies = st.slider('Number of Pregnancies', 0, 50, 5)
    Glucose = st.slider('Glucose Level', 0, 50, 5)
    BloodPressure = st.slider('Blood Pressure value', 0, 50, 5)
    SkinThickness = st.slider('Skin Thickness value', 0, 50, 5)
    Insulin = st.slider('Insulin Level', 0, 50, 5)
    BMI = st.slider('BMI value', 0, 50, 5)
    DiabetesPedigreeFunction = st.slider("Diabetes Pedigree Function value", 0, 50, 5)
    Age = st.slider('Age of the Person', 0, 120, 5)


    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        vendor_data = pd.DataFrame(
                [
                    {
                        "Pregnancies": Pregnancies,
                        "Glucose": Glucose,
                        "Blood Pressure": BloodPressure,
                        "Skin Thickness": SkinThickness,
                        "Insulin": Insulin,
                        "BMI": BMI,
                        "Diabetes Pedigree Function": DiabetesPedigreeFunction,
                        "Age": Age,
                    }
                ]
            )
        # Add the new vendor data to the existing data
        updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

        # Update Google Sheets with the new vendor data
        conn.update(worksheet="Sheet1", data=updated_df)

        st.success("Vendor details successfully submitted!")
        # Notify in Telegram about the new submission
        push = pb.push_note("This is the title", text)
