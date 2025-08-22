# This is the Python file for the home page of our web-app.

# Importing Streamlit.
import streamlit as st

# Page configurations.
st.set_page_config(layout = "wide", # Page will be wide by default.
                   page_title = "IARA", # Name of our web-app to be displayed in the browser tab.
                   initial_sidebar_state = "expanded") # Sidebar will be open by default.

# Home page title and definition.
st.title("IARA 📚")
st.write("Indoor Airborne Risk Assessment")

st.divider()

# Text explaining what the intended use and users are of the web-app.
st.write("")
st.write("**IARA** is a web-based application that **calculates the risk of airborne disease transmission** using both the **traditional Wells-Riley model** and an **enhanced Wells-Riley model** that captures the **residual risk** after the infectious individuals leave the indoor environment.")
st.write("🌍 Designed for public health officials, building managers, and all types of people looking to make informed decisions about how to setup and manage their space in a way that mitigates infection risk.")

st.divider()

st.write("👨‍💻 **Developed by:** Akthar Uzzaman")
st.write("🔗 **GitHub Repository:** https://github.com/arctarc/IARA")