import streamlit as st
import requests

st.title("Streamlit Frontend")

# Example of calling the backend API
response = requests.get("http://backend:8000/api/example")
st.write(response.json())
