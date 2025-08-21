# This is the main script for our web-app. In this script, the various pages will be declared and navigation will be setup.

# Importing Streamlit.
import streamlit as st

# Defining the pages for our web-app. More pages will be added as needed throughout development.
home_page = st.Page("home_page.py", title = "Home", icon = "🏠")
Wells_Riley_page = st.Page("Wls_Rly_page.py", title = "The Wells-Riley Model", icon = "📕")
Scn_One_page = st.Page("Scn_One_page.py", title = "Residual Risk Model", icon = "📗")

# Navigation between pages.
all_pgs = st.navigation([home_page, Wells_Riley_page, Scn_One_page])

# Running pages.
all_pgs.run()