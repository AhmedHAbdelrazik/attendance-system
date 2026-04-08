import streamlit as st

st.header("hello")
st.text_input("Enter your name")
pic =  st.camera_input("Take a photo")
if pic:
    st.image(pic)