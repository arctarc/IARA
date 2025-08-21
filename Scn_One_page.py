#====================================================================================================================================================
# GENERAL:
#====================================================================================================================================================

# This is the Python file for the Residual Risk page of our web-app.

# Imports.
import streamlit as st
import numpy as np
import pandas as pd
import math
import plotly.express as px

# Page configurations.
st.set_page_config(layout = "wide",
                   page_title = "IARA",
                   initial_sidebar_state = "expanded")

# Title.
st.title("Residual Risk Model 📗")

# Tabs.
tab1, tab2, tab3, tab4 = st.tabs(["Model overview", "Model", "Risk Assessment", "References"])

#====================================================================================================================================================
# MODEL OVERVIEW TAB:
#====================================================================================================================================================

# An overview of the mode.
with tab1:

#======================================================================
# MODEL OVERVIEW:
#======================================================================

    st.write("### ❓ What Is The Residual Risk Model")

    st.write("")
    st.write("")

    st.write("This enhanced version of the Wells-Riley model extends beyond the traditional approach by not only modelling the probability of infection during the infectors presence, but after the infector has departed.")

    st.divider()

#======================================================================
# INPUT OVERVIEW:
#======================================================================

    st.write("### 📝 Model Inputs")

    st.write("")
    st.write("")

    st.write("**👫 Number of Individuals:** This is the total number of people within the space, infected and non-infected alike. There must be at least two people within the space, one infector and one susceptible individual.")
    
    st.write("**🤧 Number of Infectors:** This is the total number of infectors within the space. There must be at least one infector within the space. The number of infectors cannot equal or exceed the total number of individuals.")
    
    st.write("**🫁  Pulmonary Breathing Rate:** This is the breathing rate of any susceptible individual. This will default to the breathing rate of an adult at rest, which is 0.465 m³/h. Users can choose a default breathing rate based on the age and activity of the person, or enter their own custom value in 'Advanced Mode'.")
    
    st.write("**🦠 Quanta Emission:** This is the quanta emission rate. Users can choose a default quanta emission rate based on the disease and activity of the infectors, and apply mask usage if any. Alternatively, users can enter their own custom value in 'Advanced Mode'.")
    
    st.write("**💨 Room Ventilation Rate:** This is the ventilation rate of the space. Users can choose a default room ventilation rate based on the setting. Alternatively, users can enter their own custom value in 'Advanced Mode'.")

    st.write("**📏 Room Volume:** This is an estimate of the room volume. Users can choose to estimate their room volume by imagining the number of small cars (FIAT 500's) they can fit into their space. Alternatively, users can enter their own custom value in 'Advanced Mode'.")

    st.write("**⏳ Time Infectors Are Present:** This is the time that the infectors are present within the space. User's can enter the time in hours or minutes. The minimum durations are 0.25 hours and 1 minute respectively.")

    st.write("**⌛️ How Long Do The Susceptibles Remain?:** This is the time that the susceptible people remain in the space after the infectors have left. User's can enter the time in hours or minutes. The minimum durations are 0.25 hours and 1 minute respectively. If the user's are unsure how long this duration will last, they do not have to input any data.")
    
    st.divider()

#======================================================================
# OUTPUT OVERVIEW:
#======================================================================

    st.write("### 🏗️ Model Outputs")

    st.write("")
    st.write("")

    st.write("**Risk During Presence:** The risk of infection whilst the infector is present.")
    st.write("**Risk After Departure:** The risk of infection after the infector has left due to remaining infectious particles within the space.") 
    st.write("**Total Combined Risk:** The total combined risk of infection, including the risk whilst the infector is present and the risk after the infector has left.")
    st.write("**Indefinite Risk:** The risk of infection for an unknown duration after the infector has left the space.")
    st.write("**🆚 Model Comparison:** A comparison between the risk estimates produced by the traditional Wells-Riley model and the enhanced Wells-Riley model.")

    st.write("")

    st.write("**📊 Bar-Chart:** A bar-chart that plots all four risk estimates produced by the enhanced Wells-Riley model beside each other.")
    st.write("**🥧 Pie-Chart:** A pie-chart dividing the total combined risk between the risk whilst the infector is present and the residual risk after the infector has left.")
    st.write("**📈 Estimated Infection Risk Graph:** A graph that showcases the estimated infection risk at various discrete time points whilst the infector is present and after the infector has departed.")

#====================================================================================================================================================
# MODEL TAB:
#====================================================================================================================================================

# Users will input their data corresponding to the models parameters.
with tab2:

#======================================================================
# INDIVIDUALS:
#======================================================================

    st.write("### 👫 Number of Individuals")

    st.write("")
    st.write("")

    # Numerical input for the total number of individuals.
    st.number_input("Total number of individuals within the space",
                    min_value = 2,
                    key = "scnone_all",
                    help = "There must be at least one infector and one susceptible individual within the space.")
    st.write("")
    st.write(f"**There is a total number of {st.session_state.scnone_all} individuals within the space.**")

    st.divider()

#======================================================================
# INFECTORS:
#======================================================================

    st.write("### 🤧 Number of Infectors")

    st.write("")
    st.write("")
    
    # Numerical input for the number of infectors.
    st.number_input("Number of infectious individuals within the space",
                    min_value = 1,
                    key = "scnone_infectors",
                    help = "There must be at least one infector within the space.")
    st.write("")
    if st.session_state.scnone_infectors == 1:
        st.write("**There is 1 infector within the space.**")
    else:
        st.write(f"**There are {st.session_state.scnone_infectors} infectors within the space.**")

    # This if-statement checks that the number of infectors is not greater than or equal to the total number of individuals.
    if st.session_state.scnone_infectors >= st.session_state.scnone_all:
        st.warning("The number of infectors must be less than the total number of individuals for a valid risk assessment.")

    # Assigning the number of infectors to the variable 'scnone_I', for the equations.
    scnone_I = st.session_state.scnone_infectors

    st.divider()

#======================================================================
# PULMONARY BREATHING RATE:
#======================================================================

    st.write("### 🫁 Pulmonary Breathing Rate")

    st.write("")
    st.write("")

    # Dictionary containing breathing rate data (m³/h).
    scnone_breathing_dict = {
        "Adult": {"Sleep": 0.385, "Sitting/Resting": 0.465, "Light activity (Standing/Walking)": 1.375, "Heavy activity (Exercise/Sports)": 2.85},
        "15 Years Old": {"Sleep": 0.385, "Sitting/Resting": 0.44, "Light activity (Standing/Walking)": 1.34, "Heavy activity (Exercise/Sports)": 2.745},
        "10 Years Old": {"Sleep": 0.31, "Sitting/Resting": 0.38, "Light activity (Standing/Walking)": 1.12, "Heavy activity (Exercise/Sports)": 2.03},
        "5 Years Old": {"Sleep": 0.24, "Sitting/Resting": 0.32, "Light activity (Standing/Walking)": 0.57}
    }

    # Defining an empty area that will contain presets.
    scnone_dflt_txt_breathing = st.empty()

    scnone_adv_md_breathing = st.toggle("Pulmonary Breathing Rate Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # 'Advanced Mode' toggle where the user can enter their own custom value - toggled off by default.

    st.write("")

    if not scnone_adv_md_breathing: # If Advanced Mode is toggled off.
        with scnone_dflt_txt_breathing.container(): 
            # Fill the predefined empty space with presets.
            st.write("**By default, we will use a Pulmonary Breathing Rate of 0.465 m³/h.**")
            st.write("*This is the average Pulmonary Breathing Rate for an adult at rest*")
            st.write("*However, you can adjust this below, or you can enter a custom value by activating Advanced Mode*")
            st.write("")

            # The user can choose to use presets, this is turned off by default.
            scnone_breathing_adjust = st.checkbox("Adjust the default Pulmonary Breathing Rate by selecting the age-group and activity of the population", False)
            st.write("")
            if scnone_breathing_adjust: # If the user would like to use our presets...
                # ... they will select the majority age group and activity of the population.
                scnone_dflt_breathing_age = st.selectbox("What is the majority age-group of the population?", ["Adult", "15 Years Old", "10 Years Old", "5 Years Old"])

                if scnone_dflt_breathing_age == "5 Years Old": # If the user selects five years old, a selectbox without Heavy Activity is used as this data is unavailable.
                    scnone_fvyrsold_breathing_activity = st.selectbox("What activity are majority of the population taking part in?", ["Sleep", "Sitting/Resting", "Light activity (Standing/Walking)"])

                    st.write("")

                    # Find the corresponding value in the dictionary.
                    st.session_state.scnone_breathing_fvyrsold = scnone_breathing_dict[scnone_dflt_breathing_age][scnone_fvyrsold_breathing_activity]
                    st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.scnone_breathing_fvyrsold}m³/h.**")
                    st.write("")

                    # Convert and asign this value to scnone_P, for the equations.
                    scnone_p = st.session_state.scnone_breathing_fvyrsold / 60

                else: # If the user is using other age groups, a selectbox that includes Heavy Activity is used as this data is available for all other age groups.
                
                    scnone_dflt_breathing_activity = st.selectbox("What activity are majority of the population taking part in?", ["Sleep", "Sitting/Resting", "Light activity (Standing/Walking)", "Heavy activity (Exercise/Sports)"])

                    st.write("")

                    # Find the value in the dictionary.
                    st.session_state.scnone_breathing_dflt = scnone_breathing_dict[scnone_dflt_breathing_age][scnone_dflt_breathing_activity]
                    st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.scnone_breathing_dflt}m³/h.**")
                    st.write("")

                    # Convert and asign this value to scnone_P, for the equations.
                    scnone_p = st.session_state.scnone_breathing_dflt / 60
            else: # If the user will not be using our presets...
                scnone_p = 0.00775 # ... asign the default breathing rate to scnone_p.
                st.write("**The Pulmonary Breathing Rate for your risk assessment is 0.465m³/h.**")
                st.write("")

    else: # Advanced Mode.

        # Users can pick between measuring breathing rate by m³/h or L/min. m³/h is the default option.
        scnone_breathing_units = st.radio("Units of measure:", ["m³/h", "L/min"], index = 0)

        st.write("")

        if scnone_breathing_units == "m³/h":
            st.number_input("Pulmonary Breathing Rate of any susceptible person in m³/h", # Numerical input to enter breathing rate (m³/h).
                      key = "scnone_breathing_m3h")
            st.write("")
            st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.scnone_breathing_m3h}m³/h.**")
        
            # This if-statement encourages the user to enter a non-zero value.
            if st.session_state.scnone_breathing_m3h <= 0:
                st.warning("The Pulmonary Breathing Rate must be greater than 0 for a valid risk assessment.")

            # Convert and assign the associated value to the variable 'scnone_p', for the equations.
            scnone_p = st.session_state.scnone_breathing_m3h / 60
            
        else:
            st.number_input("Pulmonary Breathing Rate of any susceptible person in L/min", # Numerical input to enter breathing rate (L/min).
                            key = "scnone_breathing_lmin",
                            help = "Pulmonary Breathing Rate can vary depending on age and type of activity.")
            st.write("")
            st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.scnone_breathing_lmin}L/min.**")

            if st.session_state.scnone_breathing_lmin <= 0:
                st.warning("The Pulmonary Breathing Rate must be greater than 0 for a valid risk assessment.")

            # Convert and assign.
            scnone_p = st.session_state.scnone_breathing_lmin / 1000

    # Reference: https://www.icrp.org/publication.asp?id=ICRP%20Supporting%20Guidance%203
    
    st.divider()

#======================================================================
# QUANTA EMISSION:
#======================================================================

    st.write("### 🦠 Quanta Emission")

    st.write("")
    st.write("")

    # Dictionary containing quanta emission data.
    scnone_quanta_em_dict = {
        "SARS-CoV-2/COVID-19": {"Resting/Oral Breathing": 0.55, "Standing/Speaking": 2.7, "Light Activity/Speaking Loudly": 46},
        "Influenza": {"Resting/Oral Breathing": 0.035, "Standing/Speaking": 0.17, "Light Activity/Speaking Loudly": 3.0},
        "TB (On Treatment)": {"Resting/Oral Breathing": 0.020, "Standing/Speaking": 0.098, "Light Activity/Speaking Loudly": 1.7},
        "TB (Untreated)": {"Resting/Oral Breathing": 0.62, "Standing/Speaking": 3.1, "Light Activity/Speaking Loudly": 52}
    }

    # Dictionary containing mask efficiency data.
    scnone_msk_eff_dict = {
        "KN95": 0.05, # 95% efficiency.
        "R95": 0.04, # 96% efficiency.
        "Blue surgical mask": 0.53, # 47% efficiency.
        "Cloth mask": 0.6, # 40% efficiency.
        "No mask": 1.0 # 0% efficiency.
    }

    # Defining an empty area that will allow the user to pick presets.
    scnone_dflt_quanta_em_space = st.empty()

    scnone_adv_md_quanta = st.toggle("Quanta Emission Rate Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # 'Advanced Mode' where the user can enter their own quanta emission rate - toggled off by default.

    st.write("")

    if not scnone_adv_md_quanta: # If Advanced Mode is toggled off.
        with scnone_dflt_quanta_em_space.container():
            # Fill the predefined empty space with presets.
            
            # The user will select what disease, the activity of the infector(s), and mask usage. 
            scnone_quanta_disease_choice = st.selectbox("Which disease are you modelling for?", ["SARS-CoV-2/COVID-19", "Influenza", "TB (On Treatment)", "TB (Untreated)"])
            if scnone_I == 1:
                scnone_quanta_activity_choice = st.selectbox("What activity is the infectious individual taking part in?", ["Resting/Oral Breathing", "Standing/Speaking", "Light Activity/Speaking Loudly"])
            else:
                scnone_quanta_activity_choice = st.selectbox("What activity are majority of the infectors taking part in?", ["Resting/Oral Breathing", "Standing/Speaking", "Light Activity/Speaking Loudly"])
            scnone_quanta_mask_usage = st.selectbox("What type of mask is being worn?", ["KN95", "R95", "Blue surgical mask", "Cloth mask", "No mask"],
                                             help = "Mask efficiency is calculated in the context of COVID-19, but is assumed to be broadly applicable to other airborne diseases.")

            st.write("")

            # Find the values in the dictionaries. Convert and calculate final quanta emission rate incorporating mask usage.
            scnone_init_quanta = scnone_quanta_em_dict[scnone_quanta_disease_choice][scnone_quanta_activity_choice]
            st.session_state.scnone_quanta_dflt = scnone_init_quanta * (scnone_msk_eff_dict[scnone_quanta_mask_usage])
            st.write(f"**The Quanta emission rate is {st.session_state.scnone_quanta_dflt:.4f}/h.**")
            st.write("")

            # Asign this value to scnone_q, for the equations.
            scnone_q = st.session_state.scnone_quanta_dflt / 60

    else: # Advanced Mode
        
        # Numerical input for the quanta emission rate.
        st.number_input("Quanta emission rate per hour",
                        min_value = 1,
                        key = "scnone_quanta",
                        help = "There must be at least one quanta emitted per hour. This can vary by disease and activity.")
        st.write("")
        st.write(f"**The Quanta emission rate is {st.session_state.scnone_quanta}/h.**")

        # Assigning the quanta emission rate to the variable 'scnone_q', for the equations.
        scnone_q = st.session_state.scnone_quanta / 60

    # Reference for quanta emission rate data: Mikszewski, 2022, "The airborne contagiousness of respiratory viruses: A comparative analysis and implications for mitigation", Volume 13, Issue 6.
    # Reference for mask efficiency data: Shah, 2021, "Experimental investigation of indoor aerosol dispersion and accumulation in the context of COVID-19: Effects of masks and ventilation", Volume 33, Issue 7.

    st.divider()

#======================================================================
# ROOM VENTILATION RATE:
#======================================================================

    st.write("### 💨 Room Ventilation Rate")

    st.write("")
    st.write("")

    # Dictionary containing room ventilation rate data (ACH).
    scnone_ventilation_dict = {
        "Education": {"Assembly Halls": 4, "Classrooms": 6, "Computer Rooms": 15},
        "Healthcare": {"Dental Centres": 8, "Pharmacies": 6, "Hospital Rooms (Sterilising)": 15, "Hospital Rooms (Wards)": 6, "Hospital Rooms (X-Ray)": 10, "Medical Centres": 8, "Medical Clinics": 8, "Medical Offices": 8},
        "Hospitality": {"Bars": 20, "Cafeterias": 12, "Cocktail Lounges": 20, "Lunch Rooms": 12, "Nightclubs": 20, "Restaurants (Dining Area)": 8, "Restaurants (Food Staging)": 10, "Restaurants (Kitchens)": 30, "Restaurants (Bars)": 15, "Tavern": 20},
        "Commercial": {"Banks": 4, "Court Houses": 4, "Conference Rooms": 8, "Fire Stations": 4, "Offices (Public)": 3, "Offices (Business)": 6, "Office Lunch Rooms": 7, "Police Stations": 4, "Post Offices": 4, "Retail": 6, "Shopping Centres": 6, "Supermarkets": 4},
        "Recreational": {"Auditoriums": 12, "Bowling Alleys": 10, "Clubhouses": 20, "Dance Halls": 6, "Gyms": 6, "Museums": 12, "Swimming Pools": 20, "Theatres": 8},
        "Industrial/Technical": {"Factory Buildings": 2, "Factory Buildings with Fumes/Moisture": 10, "Laboratories": 6, "Pig Houses": 6, "Poultry Houses": 6, "Warehouses": 6}
    }

    # Defining an empty area where the user can pick a preset ACH.
    scnone_dflt_vent_space = st.empty()

    scnone_adv_md_vent = st.toggle("Room Ventilation Rate Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # 'Advanced Mode' where the user can enter their own ACH value - this is toggled off by default.

    st.write("")

    if not scnone_adv_md_vent: # If Advanced Mode is toggled off.
        with scnone_dflt_vent_space.container():
            # Fill the predefined empty space with preset ACH values.
            # Pick the category.
            scnone_user_cat_choice = st.selectbox("Which of these categories would your setting fall in?", ["Education", "Healthcare", "Hospitality", "Commercial", "Recreational", "Industrial/Technical"])
            # Pick the setting depending on the category.
            if scnone_user_cat_choice == "Education":
                scnone_user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Assembly Halls", "Classrooms", "Computer Rooms"])
            elif scnone_user_cat_choice == "Healthcare":
                scnone_user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Dental Centres", "Pharmacies", "Hospital Rooms (Sterilising)", "Hospital Rooms (Wards)", "Hospital Rooms (X-Ray)", "Medical Centres", "Medical Clinics", "Medical Offices"])
            elif scnone_user_cat_choice == "Hospitality":
                scnone_user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Bars", "Cafeterias", "Cocktail Lounges", "Lunch Rooms", "Nightclubs", "Restaurants (Dining Area)", "Restaurants (Food Staging)", "Restaurants (Kitchens)", "Restaurants (Bars)", "Tavern"])
            elif scnone_user_cat_choice == "Commercial":
                scnone_user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Banks", "Court Houses", "Conference Rooms", "Fire Stations", "Offices (Public)", "Offices (Business)", "Office Lunch Rooms", "Police Stations", "Post Offices", "Retail", "Shopping Centres", "Supermarkets"])
            elif scnone_user_cat_choice == "Recreational":
                scnone_user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Auditoriums", "Bowling Alleys", "Clubhouses", "Dance Halls", "Gyms", "Museums", "Swimming Pools", "Theatres"])
            elif scnone_user_cat_choice == "Industrial/Technical":
                scnone_user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Factory Buildings", "Factory Buildings with Fumes/Moisture", "Laboratories", "Pig Houses", "Poultry Houses", "Warehouses"])

            st.write("")

            # Find the value in the dictionary..
            st.session_state.scnone_dflt_ach = scnone_ventilation_dict[scnone_user_cat_choice][scnone_user_stng_choice]
            st.write(f"**The minimum ACH of your setting should be {st.session_state.scnone_dflt_ach}, according to government and legislative advice correct as of December 2021.**")
            st.write("")

    else: # Advanced Mode
    
        # Users pick unit of measure. m³/h is the default option.
        scnone_ventilation_unit = st.radio("Units of measure:", ["m³/h", "ACH", "L/s"], index = 0)

        st.write("")

        if scnone_ventilation_unit == "m³/h":
            st.number_input("Room ventilation rate in m³/h",
                            key = "scnone_ventilation_m3h")
            st.write("")
            st.write(f"**The room ventilation rate is {st.session_state.scnone_ventilation_m3h}m³/h.**")
    
            # This if-statement encourages the user to enter a non-zero value for the ventilation rate.
            if st.session_state.scnone_ventilation_m3h <= 0:
                st.warning("The room ventilation rate must be greater than 0 for a valid risk assessment.")

            # Convert and assign 'scnone_Q', for the equations.
            scnone_Q = st.session_state.scnone_ventilation_m3h / 60

        elif scnone_ventilation_unit == "ACH":
            st.number_input("Room ventilation rate in ACH",
                            key = "scnone_adv_ach")
            st.write("")
            st.write(f"**The room ventilation rate is {st.session_state.scnone_adv_ach}ACH.**")

            # This if-statement encourages the user to enter a non-zero value for the ventilation rate.
            if st.session_state.scnone_adv_ach <= 0:
                st.warning("The room ventilation rate must be greater than 0 for a valid risk assessment.")

        elif scnone_ventilation_unit == "L/s":
            st.number_input("Room ventilation rate in L/s",
                            key = "scnone_ventilation_ls")
            st.write("")
            st.write(f"**The room ventilation rate is {st.session_state.scnone_ventilation_ls}L/s.**")
    
            # This if-statement encourages the user to enter a non-zero value for the ventilation rate.
            if st.session_state.scnone_ventilation_ls <= 0:
                st.warning("The room ventilation rate must be greater than 0 for a valid risk assessment.")

            # Convert and assign the value.
            scnone_Q = st.session_state.scnone_ventilation_ls / 16.667

# Reference for recommended ACH values: https://www.axaironline.co.uk/media/attachment/attachment/Air-Change-per-Hour-Document.pdf
    
    st.divider()

#======================================================================
# ROOM VOLUME:
#======================================================================

    st.write("### 📏 Room Volume")

    st.write("")
    st.write("")

    scnone_fiat500_size = 8.65
    # This is the size of a FIAT 500 in m³, rounded to two decimal places.

    # Defining an empty area where the user can describe their Room Volume using FIAT 500's.
    scnone_dflt_vol_space = st.empty()

    scnone_adv_md_vol = st.toggle("Room Volume Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # 'Advanced Mode' where the user can enter their own Room Volume - toggled off by default.

    st.write("")

    if not scnone_adv_md_vol: # If Advanced Mode is toggled off.
        with scnone_dflt_vol_space.container():
            # Fill the predefined empty space.

            # The user will input how many FIAT 500's they believe can fit into their space.
            scnone_user_car_num = st.number_input("How many small cars (FIAT 500's) can you fit into the space",
                            min_value = 1,
                            help = "For this risk assessment, we have taken the volume of a FIAT 500 to be 8.65m³")

            st.write("")
            
            st.session_state.scnone_dflt_room_vol = round(scnone_fiat500_size * scnone_user_car_num, 2) # Estimate the Room Volume.
            st.write(f"**The volume of your space is estimated to be {st.session_state.scnone_dflt_room_vol}m³.**")
            
            st.write("")
            
            if not scnone_adv_md_vent: # If ACH was used for Room Ventilation rate input...
            # ... calculate, convert, and asign Room Ventilation rate to variable.
                scnone_Q = (st.session_state.scnone_dflt_ach * st.session_state.scnone_dflt_room_vol) / 60
            elif scnone_ventilation_unit == "ACH":
                scnone_Q = (st.session_state.scnone_adv_ach * st.session_state.scnone_dflt_room_vol) / 60

            scnone_v = st.session_state.scnone_dflt_room_vol

    else: # Advanced Mode

        scnone_vol_inp = st.checkbox("I'm not sure what the volume of my room is", False) # Users can select to use individual dimensions.

        st.write("")
        
        if not scnone_vol_inp:
            scnone_vol = st.number_input("Room volume in m³")

            st.write("")
            
            st.write(f"**The room volume is {scnone_vol}m³**")

            # This if-statement encourages the user to enter a non-zero value for the ventilation rate.
            if scnone_vol <= 0:
                st.warning("The room volume must be greater than 0 for a valid risk assessment")

            # Asign Room Volume to variable.
            scnone_v = scnone_vol

            if not scnone_adv_md_vent: # If ACH was used for Room Ventilation rate input...
                # ... calculate, convert, and asign Room Ventilation rate to variable.
                scnone_Q = (st.session_state.scnone_dflt_ach * scnone_v) / 60
            elif scnone_ventilation_unit == "ACH":
                scnone_Q = (st.session_state.scnone_adv_ach * scnone_v) / 60
        
        else: # If the user does not know their Room Volume, they can enter each dimension.
            scnone_vol_col1, scnone_vol_col2, scnone_vol_col3 = st.columns(3)
            with scnone_vol_col1:
                scnone_length = st.number_input("Length (m)")
            with scnone_vol_col2:
                scnone_width = st.number_input("Width (m)")
            with scnone_vol_col3:
                scnone_height = st.number_input("Height (m)")

            st.write("")
            
            st.session_state.scnone_adv_room_vol = scnone_length * scnone_width * scnone_height # Calculating volume.
            st.write(f"**The room volume is {st.session_state.scnone_adv_room_vol}m³**")

            if st.session_state.scnone_adv_room_vol <= 0:
                st.warning("The room volume must be greater than 0 for a valid risk assessment")

            # Asign Room Volume to variable.
            scnone_v = st.session_state.scnone_adv_room_vol

            if not scnone_adv_md_vent: # If ACH was used for Room Ventilation rate input...
                # ... calculate, convert, and asign Room Ventilation rate to variable.
                scnone_Q = (st.session_state.scnone_dflt_ach * scnone_v) / 60
            elif scnone_ventilation_unit == "ACH":
                scnone_Q = (st.session_state.scnone_adv_ach * scnone_v) / 60

# Reference for FIAT 500 dimensions: https://www.carwow.co.uk/fiat/500/specifications#gref

    st.divider()

#======================================================================
# TIME INFECTORS ARE PRESENT:
#======================================================================
    
    st.write("### ⏳ Time Infectors Are Present")

    st.write("")
    st.write("")

    scnone_time_units = st.radio("Units of measure:", ["Hours", "Minutes"], index = 0)

    st.write("")

    if scnone_time_units == "Hours":
        st.slider("How many hours were the infectors present within the space?",
                  min_value = 0.25,
                  max_value = 24.0,
                  step = 0.25,
                  key = "scnone_time_hours",
                  help = "Quater-hour inputs allow for greater precision.")

        st.write("")
        
        if st.session_state.scnone_time_hours == 1.0:
            st.write("**The infector was present for 1 hour.**")
        else:
            st.write(f"**The infector was present for {st.session_state.scnone_time_hours} hours.**")

        # Convert and assign to variable 'scnone_T', for the equations.
        scnone_T = st.session_state.scnone_time_hours * 60
            
    else:
        st.number_input("How many minutes were the infectors present within the space?",
                        min_value = 1,
                        key = "scnone_time_minutes",
                        help = "Exposure time must have lasted for at least one minute.")

        st.write("")
        
        if st.session_state.scnone_time_minutes == 1.0:
            st.write("**The infector was present for 1 minute.**")
        else:
            st.write(f"**The infector was present for {st.session_state.scnone_time_minutes} minutes.**")

        # Asign value to variable.
        scnone_T = st.session_state.scnone_time_minutes

    st.write("")
    st.write("")

    scnone_inf_time = st.checkbox("**Do the susceptible individuals leave with the infectors?**", False)
    # User can choose to model for infinite 'post-infector' time, or set a fixed time duration.

    if not scnone_inf_time: # If not modelling for infinite time...

        st.divider()

#======================================================================
# TIME AFTER INFECTORS LEAVE (OPTIONAL):
#======================================================================

        st.write("### ⌛️ How Long Do The Susceptibles Remain?")

        st.write("")
        st.write("")
    
        scnone_extra_time_units = st.radio("Units of measure: ", ["Hours", "Minutes"], index = 0)

        st.write("")

        if scnone_extra_time_units == "Hours":
            st.slider("How many hours did the susceptibles remain after the infectors left?",
                      min_value = 0.25,
                      max_value = 24.0,
                      step = 0.25,
                      key = "scnone_extra_time_hours",
                      help = "Quater-hour inputs allow for greater precision.")

            st.write("")
        
            if st.session_state.scnone_extra_time_hours == 1.0:
                st.write("**The additional exposure time was 1 hour.**")
            else:
                st.write(f"**The additional exposure time was {st.session_state.scnone_extra_time_hours} hours.**")

            # Convert and assign to variable 'scnone_t', for the equations.
            scnone_t = st.session_state.scnone_extra_time_hours * 60
            
        else:
            st.number_input("How many minutes did the susceptibles remain after the infectors left??",
                            min_value = 1,
                            key = "scnone_extra_time_minutes",
                            help = "Exposure time must have lasted for at least one minute.")

            st.write("")
        
            if st.session_state.scnone_extra_time_minutes == 1.0:
                st.write("**The additional exposure time was 1 minute.**")
            else:
                st.write(f"**The additional exposure time was {st.session_state.scnone_extra_time_minutes} minutes.**")

            # Asign value to variable.
            scnone_t = st.session_state.scnone_extra_time_minutes

#====================================================================================================================================================
# OUTPUT TAB:
#====================================================================================================================================================

# This tab will present the risk assessment.
with tab3:

#======================================================================
# INFECTION PROBABILITIES:
#======================================================================

    st.write("### 📊 Infection Probabilities")

    st.write("")
    st.write("")

    @st.cache_data # Cache model output to avoid recomputation for reused inputs.
    def scnone_equations(scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v, scnone_t = None):
        """
        This function calculates the risks of infection using an enhanced Wells-Riley model from Edwards et al. (2024).
        If t remains as none, it is assumed that the susceptibles remain indefinitely.

        Args:
            scnone_I (int): The number of infected individuals.
            scnone_T (float): The time the infectors are present.
            scnone_p (float): The breathing rate of any susceptible individual.
            scnone_q (int): The quanta emission rate.
            scnone_Q (float): The ventilation rate.
            scnone_v (float): The Room Volume.
            scnone_t (float, optional): Modelling time after the infectors leave. Defaults to None.

        Returns:
            float: Infection risk whilst infectors are present (P1)
            float: Infection risk after infectors leave (P2). Defaults to None if scnone_t is None
            float: Combined infection risk (P_comb). Defaults to None if scnone_t is None
            float: Infection risk if susceptibles remain indefinitely (P_inf)
        """

        try:
        
            # Equation 9: Risk whilst infector is present
            exp_p1 = (scnone_p * scnone_q * scnone_I / scnone_Q**2) * (scnone_v * (1 - math.exp(-(scnone_Q / scnone_v) * scnone_T)) - scnone_Q * scnone_T)
            P1 = 1 - math.exp(exp_p1)

            # Equation 14: Indefinite time risk
            exp_inf = -(scnone_p * scnone_q * scnone_I / scnone_Q) * scnone_T
            P_inf = 1 - math.exp(exp_inf)

            # If scnone_t is None (modelling for indefinite time), return the above, skip Equations 11 and 13.
            if scnone_t == None:
                return P1, None, None, P_inf

            # Equation 11: Risk after the infector leaves
            exp_p2 = -((scnone_p * scnone_q * scnone_v * scnone_I)/scnone_Q**2) * (1-math.exp(-(scnone_Q / scnone_v) * scnone_T)) * (1-math.exp(-(scnone_Q / scnone_v) * scnone_t))
            P2 = 1 - math.exp(exp_p2)

            # Equation 13: Combined risk
            exp_comb = ((scnone_p * scnone_q * scnone_v * scnone_I) / scnone_Q**2) * ((math.exp(-(scnone_Q / scnone_v) * scnone_t)) * (1 - math.exp(-(scnone_Q / scnone_v) * scnone_T)) - (scnone_Q / scnone_v) * scnone_T)
            P_comb = 1 - math.exp(exp_comb)

            # If scnone_t is not None (modelling for fixed time duration), return all.
            return P1, P2, P_comb, P_inf
        
        except ZeroDivisionError: # If any value equals 0, instead of ZeroDivisionError's, return 0's.
        
            P1, P2, P_comb, P_inf = 0, 0, 0, 0
        
        return P1, P2, P_comb, P_inf # Return respective values in case of ZeroDivisionError.

    # If scnone_t is used, call function and asign.
    if not scnone_inf_time:
        P1, P2, P_comb, P_inf = scnone_equations(scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v, scnone_t)

    # If scnone_t is NOT used, call function and asign
    else:
        P1, P2, P_comb, P_inf = scnone_equations(scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v)

    
    # Columns for output.
    scnone_out_col1, scnone_out_col2, scnone_out_col3, scnone_out_col4 = st.columns(4)
    
    # If additional time is not declared (modelling for infinite time)
    if P2 == None:
        with scnone_out_col1:
            st.metric("**Risk Whilst Infectors Present:**", f"{P1*100:.2f}%")
        with scnone_out_col2:
            st.metric("**Risk When Staying Indefinitely**", f"{P_inf*100:.2f}%")

        # User data in DataFrame for Bar Chart
        scnone_bar_data = pd.DataFrame({
            "Risk Type": ["During Presence", "Staying Indefinitely"],
            "Probability (%)": [P1*100, P_inf*100]
        })
        
    # If modelling for a fixed post-depature duration
    else:
        with scnone_out_col1:
            st.metric("**Risk Whilst Infectors Present:**", f"{P1*100:.2f}%")
        with scnone_out_col2:
            st.metric("**Risk After Infectors Depart:**", f"{P2*100:.2f}%")
        with scnone_out_col1:
            st.metric("**Total Combined Risk:**", f"{P_comb*100:.2f}%")
        with scnone_out_col2:
            st.metric("**Risk When Staying Indefinitely:**", f"{P_inf*100:.2f}%")

        # Returned data in DataFrame for Bar Chart
        scnone_bar_data = pd.DataFrame({
            "Risk Type": ["During Presence", "After Depature", "Total Risk", "Staying Indefinitely"],
            "Probability (%)": [P1*100, P2*100, P_comb*100, P_inf*100]
        })

    st.write("")
    st.write("")

    # Print Bar Chart using respective data depending on what was modelled.
    st.bar_chart(scnone_bar_data.set_index("Risk Type")["Probability (%)"])

    st.divider()

    # If modelling for a fixed post-departure time, plot a pie chart breaking down the total combined risk.
    if not scnone_inf_time:

#======================================================================
# TOTAL COMBINED RISK BREAKDOWN:
#======================================================================

        st.write("### 🥧 Total Combined Risk Breakdown")

        st.write("")
        st.write("")
    
        # Calculate what percentage P1 and P2 make up of the total combined risk.
        scnone_perc_pres = (P1 / P_comb) * 100
        scnone_perc_dep = (P2 / P_comb) * 100
    
        # Create a Pandas DataFrame with the above percentages.
        scnone_pie_data = pd.DataFrame({
            'Risk Type': ['During Infector Presence', 'After Infector Departure'],
            'Percentage': [scnone_perc_pres, scnone_perc_dep]
        })
    
        # Create the pie chart using Plotly.
        scnone_pie_fig = px.pie(scnone_pie_data, 
                                values = 'Percentage', 
                                names = 'Risk Type',
                                color_discrete_sequence = ['#ff6b6b', '#4ecdc4'])  # Red slice for infector presence, teal slice for after infector departure.
    
        # Ensure text is inside the pie chart, and both the percentage and label names are shown.
        scnone_pie_fig.update_traces(textposition = 'inside', textinfo = 'percent+label')
    
        # Display the pie chart using the entire available width
        st.plotly_chart(scnone_pie_fig, use_container_width=True)

        st.divider()

#======================================================================
# TRADITIONAL VS. ENHANCED WELLS-RILEY MODEL:
#======================================================================

    st.write("### 🆚 Traditional VS. Enhanced Wells-Riley Model")

    st.write("")
    st.write("")

    # Calculate traditional Wells-Riley risk.
    scnone_trad_risk = 1 - math.exp(- (scnone_I * scnone_p * scnone_q * scnone_T) / scnone_Q)

    # Columns for output.
    scnone_comp_col1, scnone_comp_col2 = st.columns(2)

    with scnone_comp_col1: # Output traditional risk.
        st.write("**Traditional Wells-Riley Model:**")
        st.metric("Single Risk Estimate", f"{scnone_trad_risk*100:.2f}%")
        st.caption("• Assumes a constant concentration")
        st.caption("• Does **NOT** model residual risk")

    with scnone_comp_col2:
        st.write("**Enhanced Wells-Riley Model:**")
        if not scnone_inf_time: # Output risk if post-departure time duration is fixed.
            st.metric("Total Combined Risk Estimate", f"{P_comb*100:.2f}%")
            st.write(f"• During presence: {P1*100:.2f}%")
            st.write(f"• After departure: {P2*100:.2f}%")
        else: # Output risk for indefinite time.
            st.metric("Total Combined Risk Estimate", f"{P_inf*100:.2f}%")
            st.write(f"• During presence: {P1*100:.2f}%")
            st.write(f"• Staying indefinitely: {P_inf*100:.2f}%")

    st.divider()

#======================================================================
# ESTIMATED RISK ACCUMULATION OVER TIME:
#======================================================================

    st.write("### 📈 Estimated Infection Risk At Discrete Time Points")

    st.write("")
    st.write("")

    # Creating a time range:
    if not scnone_inf_time:
        # If we are NOT modelling for indefinite time, the maximum time is the duration in which the infectors are present + the duration after the infectors have departed.
        scnone_max_time = scnone_T + scnone_t
    else:
        # If we ARE modelling for indefinite time, the maximum time will be two hours after the infectors have departed.
        scnone_max_time = scnone_T + 120
    # We want a time point every five minutes.
    scnone_time_res = 5
    # We need to calculate the number of time points we need across our time range.
    scnone_num_time_points = int(scnone_max_time / scnone_time_res) + 1 # Add one to ensure that the final time point is included.
    # Finally, create a NumPy array containing the entire range of time points.
    scnone_time_range = np.linspace(0, scnone_max_time, scnone_num_time_points)

    @st.cache_data
    def scnone_rsk_plot(scnone_time_range, scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v, scnone_t = None):
        """
        This function produces an area chart that plots the estimated risk of infection at different time points using an enhanced Wells-Riley model from Edwards et al. (2024).
        If t remains as none, it is assumed that the susceptibles remain indefinitely.

        Args:
            scnone_time_range (NumPy array): A NumPy array of time points.
            scnone_I (int): The number of infected individuals.
            scnone_T (float): The time the infectors are present.
            scnone_p (float): The breathing rate of any susceptible individual.
            scnone_q (int): The quanta emission rate.
            scnone_Q (float): The ventilation rate.
            scnone_v (float): The Room Volume.
            scnone_t (float, optional): Modelling time after the infectors leave. Defaults to None.
        """

        scnone_list_probs = [] # Create an empty list to store the risk of infection at each time point.

        for time in scnone_time_range:
            # Loop over each time point in our time range.

            if time <= scnone_T:
                # If the current time falls within the time that the infector is present, calculate the risk using the appropriate equation and append to the list as a percentage.
                P1_at_time, _, _, _ = scnone_equations(scnone_I, time, scnone_p, scnone_q, scnone_Q, scnone_v)
                scnone_list_probs.append(P1_at_time * 100)
            else:
                # If the current time falls within the time after the infector departs, calculate the time since departure and do the same as above using the appropriate equation.
                scnone_post_time = time - scnone_T
                _, P2_at_time, _, _ = scnone_equations(scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v, scnone_post_time)
                scnone_list_probs.append(P2_at_time * 100)

        # Pandas DataFrame containing all time points in the time range, and their respective risks.
        scnone_riskvtime_data = pd.DataFrame({
            "Time (minutes)": scnone_time_range,
            "Risk Of Infection": scnone_list_probs})

        # Plot the DataFrame
        st.area_chart(
            data = scnone_riskvtime_data,
            x = "Time (minutes)",
            y = "Risk Of Infection",
            x_label = "Exposure Time (minutes)",
            y_label = "Risk of Infection (%)"
        )

    # Call the above function to produce the plot.
    if not scnone_inf_time:
        # If we are NOT modelling for indefinite time...
        scnone_rsk_plot(scnone_time_range, scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v, scnone_t)
    else:
        # If we ARE modelling for indefinite time...
        scnone_rsk_plot(scnone_time_range, scnone_I, scnone_T, scnone_p, scnone_q, scnone_Q, scnone_v)

    st.divider()

#======================================================================
# OTHER:
#======================================================================

    st.write("")
    st.info("You can find all of the references we have used in the 'References' tab.")

#====================================================================================================================================================
# REFERENCES TAB:
#====================================================================================================================================================

# Tab containing references for the information used.
with tab4:

    st.write("### 📑 Primary Research")
    
    st.write("")
    st.write("")
    
    st.write("**The Wells-Riley Model:**")
    st.write("E.C. Riley, 'AIRBORNE SPREAD OF MEASLES IN A SUBURBAN ELEMENTARY SCHOOL', American Journal of Epidemiology, Volume 107, Issue 5, May 1978, Pages 421–432")
    
    st.write("")

    st.write("**The Residual Risk Model:**")
    st.write("Alexander Edwards, 'The Wells–Riley model revisited: Randomness, heterogeneity, and transient behaviours', Risk Analysis, Volume 44, Issue 9, September 2024, Pages 2125-2147")

    st.divider()

    st.write("### 📃 Supporting Data")

    st.write("")
    st.write("")

    st.write("**Pulmonary Ventilation Rate Data:**")
    st.write("ICRP, 'Guide for the Practical Application of the ICRP Human Respiratory Tract Model', ICRP Supporting Guidance 3, Annals of the ICRP, Volume 32, Issues 1-2, 2002")

    st.write("")

    st.write("**Quanta Emission Rate Data:**")
    st.write("Alex Mikszewsk, 'The airborne contagiousness of respiratory viruses: A comparative analysis and implications for mitigation', Geoscience Frontiers, Volume 13, Issue 6, November 2022")

    st.write("")

    st.write("**Mask Efficiency Data:**")
    st.write("Yash Shah, 'Experimental investigation of indoor aerosol dispersion and accumulation in the context of COVID-19: Effects of masks and ventilation', Physics of Fluids, Volume 33, Issue 7, July 2021")

    st.write("")

    st.write("**ACH Data:**")
    st.write("https://www.axaironline.co.uk/media/attachment/attachment/Air-Change-per-Hour-Document.pdf")

    st.write("")

    st.write("**Small car (FIAT 500) dimensions:**")
    st.write("https://www.carwow.co.uk/fiat/500/specifications#gref")