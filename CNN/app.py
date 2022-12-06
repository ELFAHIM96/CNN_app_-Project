import streamlit as st
from streamlit_option_menu import option_menu
from st_bridge import bridge, html

#EDA Pkage
import pandas as pd 
import numpy as np 
import json
#Utils

import os 
# data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
import hashlib 
from PIL import Image
# keras
from keras.models import load_model

# ML Interpretation
import lime
import lime.lime_tabular
# passlib, bcrybt

# db
from manged_db import * 


# password
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def verify_hashes(password, hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return flase


#Classes Of traffic signs
def laod_classes(json_file1):
    with open(json_file1) as json_file:
        classes = json.load(json_file)
    return classes

def image_processing(img):
    model = load_model('model/TSR.h5')
    data= []
    image = Image.open(img)
    image = image.resize((30,30))
    data.append(np.array(image))
    X_test = np.array(data)
    Y_pred = model.predict(X_test)
    Y_pred = np.argmax(Y_pred,axis=1)
    return image, Y_pred

def load_image(image_file):
	img = Image.open(image_file)
	return img 

def main():
    """Traffic Signs Classification using CNN APP"""

    im = Image.open("images/icon.png")
    st.set_page_config(
        page_title="Traffic Signs Classification App",
        page_icon=im,
        layout="wide",
    )
    st.title("Traffic Signs Classification App")

    menu = ["Home", "Login", "SignUp"]
    
    submenu = ["Plot", "Prediction"]

    st.sidebar.image("images/TSR.png", use_column_width=True)
    choice  = st.sidebar.selectbox("Menu", menu)
    if choice =="Home":
        st.subheader("Home")
        im1 = Image.open("images/home.jpg")
        st.image(im1, caption=None, width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

    elif choice == "Login":
        username = st.sidebar.text_input("Username")  
        password = st.sidebar.text_input("Password", type = 'password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_psd = generate_hashes(password)
            result = login_user(username, verify_hashes(password, hashed_psd))
            if result:
                st.success("Welcome {}".format(username))

                activity = st.selectbox("Activity", submenu)
                if activity == "Plot":
                    st.subheader("Data Vis data")
                    df = pd.read_csv("data/Test.csv")
                    st.dataframe(df)

                    if st.checkbox("Images"):
                        all_columns = df.columns.to_list()
                        feat_choices = st.multiselect("Choose a Features", all_columns)
                        new_df = df[feat_choices]
                        st.area_chart(new_df)

                elif activity == "Prediction":
                    st.subheader("Classification Analytics")
                    st.json(laod_classes("data/classes.json"))

                    img = st.file_uploader("Upload Traffic Sign Image",type=['png','jpeg','jpg'])
                    if st.button("Predict"):
                        classes = laod_classes("data/classes.json")
                        #Dict_classes = json.loads(classes)
                        #img = load_image("image")
                        plot, result = image_processing(img)
                        s = [str(i) for i in result] 
                        
                        a = int("".join(s))
                        st.write(a)
                        st.write("Predicted traffic sign is: ", classes[str(a)])
                        plt.imshow(plot)
                        st.image(plot, caption=None, width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
                        plt.show()                  


            else:
                st.warning("Incorrect Username/password")
    elif choice == "SignUp":
        new_username = st.text_input("User name")
        new_password = st.text_input("Password", type = "password")

        confirm_password = st.text_input("Confirm Password", type = "password")
        if new_password == confirm_password:
            st.success("Password Confirmed")
        else :
            st.warning("Passwords not the same")
        if st.button("Submit"):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username, hashed_new_password)
            st.success("You have successfully created a new account")
            st.info("Login to Get Strted ")

        


if __name__ == '__main__':
    main()

