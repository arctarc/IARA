#====================================================================================================================================================
# GENERAL:
#====================================================================================================================================================

# This is the Python file for the Wells-Riley page of our web-app.

# Importing Streamlit, Numpy and Pandas
import streamlit as st
import numpy as np
import pandas as pd

# Importing Math for the 'e' value within the Wells-Riley equation.
import math

# Page configurations.
st.set_page_config(layout = "wide", # Page will be wide by default.
                   page_title = "IARA", # Name of our web-app to be displayed in the browser tab.
                   initial_sidebar_state = "expanded") # Sidebar will be open by default.

# Wells-Riley page title.
st.title("The Wells-Riley Model 📕")

# Adding tabs for the various sections of this page.
tab1, tab2, tab3, tab4 = st.tabs(["Model overview", "Model", "Risk Assessment", "References"])

#====================================================================================================================================================
# MODEL OVERVIEW TAB:
#====================================================================================================================================================

# An overview of the model.
with tab1:

#======================================================================
# MODEL OVERVIEW:
#======================================================================

    st.write("### ❓ What Is The Wells-Riley Model")

    st.write("")
    st.write("")

    st.write("The Wells-Riley model is a mathematical model that is used to estimate the probability of airborne disease infection in an indoor environment.")

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

    st.write("**⏱️ Exposure Time:** This is the time that the infectors are present within the space. User's can enter the time in hours or minutes. The minimum durations are 0.25 hours and 1 minute respectively.")
    
    st.write("**💨 Room Ventilation Rate:** This is the ventilation rate of the space. Users can choose a default room ventilation rate based on their setting, and estimate the volume of their room based on the number of small cars (FIAT 500's) that they predict can fit within it. Alternatively, users can enter their own custom value in 'Advanced Mode'.")
    
    st.divider()

#======================================================================
# OUTPUT OVERVIEW:
#======================================================================

    st.write("### 🏗️ Model Outputs")

    st.write("")
    st.write("")

    st.write("**📊 Infection Probability:** The estimated probability of infection for one susceptible individual.")
    
    st.write("**🤒 Number of New Infections:** A graphic depicting the number of new infections among the susceptible population.")
    
    st.write("**📈 Estimated Probability of Infection Over Time:** A graph showing the estimated probability of infection over time.")
    
    st.write("**⬆️ Increased Quanta Emission Rate Graph:** A similar graph to the one shown above, except this time the users quanta emission rate has been multiplied by 100. This will highlight to the user the effect of changing their inputs.")

#====================================================================================================================================================
# MODEL TAB:
#====================================================================================================================================================

# Users will input their data corresponding to the models parameters.
with tab2:

    # Session State is used so that user selections persist across reruns.

#======================================================================
# INDIVIDUALS:
#======================================================================

    st.write("### 👫 Number of Individuals")

    st.write("") # Gap between sub-heading and text.
    st.write("")
    
    # Numerical input for the number of individuals.
    st.number_input("Total number of individuals within the space",
                    min_value = 2,
                    key = "wls_all",
                    help = "There must be at least one infector and one susceptible individual within the space.")
    st.write("")
    st.write(f"**There is a total number of {st.session_state.wls_all} individuals within the space.**")

    # Adding a divider to space out requested inputs.
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
                    key = "wls_infectors",
                    help = "There must be at least one infector within the space.")
    st.write("")
    if st.session_state.wls_infectors == 1:
        st.write("**There is 1 infector within the space.**")
    else:
        st.write(f"**There are {st.session_state.wls_infectors} infectors within the space.**")

    # This if-statement checks that the number of infectors is not greater than or equal to the total number of individuals.
    if st.session_state.wls_infectors >= st.session_state.wls_all:
        st.warning("The number of infectors must be less than the total number of individuals for a valid risk assessment.")

    # Assigning the number of infectors to the variable 'I', for the Wells-Riley equation.
    I = st.session_state.wls_infectors

    st.divider()

#======================================================================
# PULMONARY BREATHING RATE:
#======================================================================

    st.write("### 🫁 Pulmonary Breathing Rate")

    st.write("")
    st.write("")

    # Dictionary containing breathing rate data (m³/h) for various different age groups and activities.
    breathing_dict = {
        "Adult": {"Sleep": 0.385, "Sitting/Resting": 0.465, "Light activity (Standing/Walking)": 1.375, "Heavy activity (Exercise/Sports)": 2.85},
        "15 Years Old": {"Sleep": 0.385, "Sitting/Resting": 0.44, "Light activity (Standing/Walking)": 1.34, "Heavy activity (Exercise/Sports)": 2.745},
        "10 Years Old": {"Sleep": 0.31, "Sitting/Resting": 0.38, "Light activity (Standing/Walking)": 1.12, "Heavy activity (Exercise/Sports)": 2.03},
        "5 Years Old": {"Sleep": 0.24, "Sitting/Resting": 0.32, "Light activity (Standing/Walking)": 0.57}
    }

    # Defining an empty area that will contain the default breathing rate and other presets.
    dflt_txt_breathing = st.empty()

    adv_md_breathing = st.toggle("Pulmonary Breathing Rate Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # Below the above area, the user can toggle between using the default breathing rate and other presets, or they can enter their own value.
    # 'Advanced Mode', where the user can enter their own custom value, is toggled off by default.

    st.write("")

    if not adv_md_breathing: # If Advanced Mode is toggled off.
        with dflt_txt_breathing.container(): 
            # Fill the predefined empty space with default text and other presets.
            st.write("**By default, we will use a Pulmonary Breathing Rate of 0.465 m³/h.**")
            st.write("*This is the average Pulmonary Breathing Rate for an adult at rest*")
            st.write("*However, you can adjust this below, or you can enter a custom value by activating Advanced Mode*")
            st.write("")

            # The user can choose whether or not they would like to use one of our various breathing rate presets.
            # This is turned off by default.
            breathing_adjust = st.checkbox("Adjust the default Pulmonary Breathing Rate by selecting the age-group and activity of the population", False)
            st.write("")
            if breathing_adjust: # If the user would like to adjust the default breathing rate using our presets...
                # ... the user will select the majority age group and activity of the population.
                dflt_breathing_age = st.selectbox("What is the majority age-group of the population?", ["Adult", "15 Years Old", "10 Years Old", "5 Years Old"])

                if dflt_breathing_age == "5 Years Old": # If the user selects the age group as five years old, a selectbox without Heavy Activity is used as this data is unavailable.
                    fvyrsold_breathing_activity = st.selectbox("What activity are majority of the population taking part in?", ["Sleep", "Sitting/Resting", "Light activity (Standing/Walking)"])

                    st.write("")

                    # Find the corresponding value in the dictionary based on the users inputs, and print this to the screen.
                    st.session_state.wls_breathing_fvyrsold = breathing_dict[dflt_breathing_age][fvyrsold_breathing_activity]
                    st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.wls_breathing_fvyrsold}m³/h.**")
                    st.write("")

                    # Asign this value to P, for the Wells-Riley model.
                    p = st.session_state.wls_breathing_fvyrsold

                else: # If the user is using any other age group apart from five years old, a selectbox that includes Heavy Activity is used as this data is available for all other age groups.
                
                    dflt_breathing_activity = st.selectbox("What activity are majority of the population taking part in?", ["Sleep", "Sitting/Resting", "Light activity (Standing/Walking)", "Heavy activity (Exercise/Sports)"])

                    st.write("")

                    # Find the corresponding value in the dictionary based on the users inputs, and print this to the screen.
                    st.session_state.wls_breathing_dflt = breathing_dict[dflt_breathing_age][dflt_breathing_activity]
                    st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.wls_breathing_dflt}m³/h.**")
                    st.write("")

                    # Asign this value to P, for the Wells-Riley model.
                    p = st.session_state.wls_breathing_dflt
            else: # If the user will not be adjusting the default breathing rate using our presets...
                p = 0.465 # ... asign the default breathing rate to P and print this to the screen.
                st.write("**The Pulmonary Breathing Rate for your risk assessment is 0.465m³/h.**")
                st.write("")

    else: # Advanced Mode.

        # Users can pick between measuring breathing rate by m³/h or L/min. m³/h is the default option.
        wls_breathing_units = st.radio("Units of measure:", ["m³/h", "L/min"], index = 0)

        st.write("")

        if wls_breathing_units == "m³/h":
            st.number_input("Pulmonary Breathing Rate of any susceptible person in m³/h", # Numerical input to enter breathing rate (m³/h) if selected by user.
                      key = "wls_breathing_m3h")
            st.write("")
            st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.wls_breathing_m3h}m³/h.**")
        
            # This if-statement encourages the user to enter a non-zero value for the breathing rate, helping to avoid a probability of 0%.
            if st.session_state.wls_breathing_m3h <= 0:
                st.warning("The Pulmonary Breathing Rate must be greater than 0 for a valid risk assessment.")

            # If m³/h was selected, assign the associated value to the variable 'P', for the Wells-Riley model.
            p = st.session_state.wls_breathing_m3h
            
        else:
            st.number_input("Pulmonary Breathing Rate of any susceptible person in L/min", # Numerical input to enter breathing rate (L/min) if selected by user.
                            key = "wls_breathing_lmin",
                            help = "Pulmonary Breathing Rate can vary depending on age and type of activity.")
            st.write("")
            st.write(f"**The Pulmonary Breathing Rate for your risk assessment is {st.session_state.wls_breathing_lmin}L/min.**")

            if st.session_state.wls_breathing_lmin <= 0:
                st.warning("The Pulmonary Breathing Rate must be greater than 0 for a valid risk assessment.")

            # If L/min was selected, use the associated value and convert to m³/h.
            p = st.session_state.wls_breathing_lmin * 0.06

    # Reference: https://www.icrp.org/publication.asp?id=ICRP%20Supporting%20Guidance%203
    
    st.divider()

#======================================================================
# QUANTA EMISSION:
#======================================================================

    st.write("### 🦠 Quanta Emission")

    st.write("")
    st.write("")

    # Dictionary containing quanta emission data for COVID-19, Influenza, and TB
    quanta_em_dict = {
        "SARS-CoV-2/COVID-19": {"Resting/Oral Breathing": 0.55, "Standing/Speaking": 2.7, "Light Activity/Speaking Loudly": 46},
        "Influenza": {"Resting/Oral Breathing": 0.035, "Standing/Speaking": 0.17, "Light Activity/Speaking Loudly": 3.0},
        "TB (On Treatment)": {"Resting/Oral Breathing": 0.020, "Standing/Speaking": 0.098, "Light Activity/Speaking Loudly": 1.7},
        "TB (Untreated)": {"Resting/Oral Breathing": 0.62, "Standing/Speaking": 3.1, "Light Activity/Speaking Loudly": 52}
    }

    # Dictionary containing mask efficiency data for various masks.
    msk_eff_dict = {
        "KN95": 0.05, # 95% efficiency.
        "R95": 0.04, # 96% efficiency.
        "Blue surgical mask": 0.53, # 47% efficiency.
        "Cloth mask": 0.6, # 40% efficiency.
        "No mask": 1.0 # 0% efficiency.
    }

    # Defining an empty area that will allow the user to pick a predefined quanta emission rate and mask usage, if any.
    dflt_quanta_em_space = st.empty()

    adv_md_quanta = st.toggle("Quanta Emission Rate Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # Below the above area, the user can toggle between using one of our predefined quanta emission rates, or they can enter their own value.
    # 'Advanced Mode', where the user can enter their own quanta emission rate, is toggled off by default.

    st.write("")

    if not adv_md_quanta: # If Advanced Mode is toggled off.
        with dflt_quanta_em_space.container():
            # Fill the predefined empty space with choices for the type of disease, activity, and mask usage, if any.
            
            # The user will select what disease they're focusing on, the activity of the infector(s), and indicate the type of mask usage. 
            quanta_disease_choice = st.selectbox("Which disease are you modelling for?", ["SARS-CoV-2/COVID-19", "Influenza", "TB (On Treatment)", "TB (Untreated)"])
            if I == 1:
                quanta_activity_choice = st.selectbox("What activity is the infectious individual taking part in?", ["Resting/Oral Breathing", "Standing/Speaking", "Light Activity/Speaking Loudly"])
            else:
                quanta_activity_choice = st.selectbox("What activity are majority of the infectors taking part in?", ["Resting/Oral Breathing", "Standing/Speaking", "Light Activity/Speaking Loudly"])
            quanta_mask_usage = st.selectbox("What type of mask is being worn?", ["KN95", "R95", "Blue surgical mask", "Cloth mask", "No mask"],
                                             help = "Mask efficiency is calculated in the context of COVID-19, but is assumed to be broadly applicable to other airborne diseases.")

            st.write("")

            # Find the corresponding values in the dictionaries based on the users input. Calculate final quanta emission rate based on mask usage and print this to the screen.
            init_quanta = quanta_em_dict[quanta_disease_choice][quanta_activity_choice]
            st.session_state.wls_quanta_dflt = round(init_quanta * (msk_eff_dict[quanta_mask_usage]), 5) # Rounds the final value to five decimal places, to avoid saving and printing several zeros.
            st.write(f"**The Quanta emission rate is {st.session_state.wls_quanta_dflt}/h.**")
            st.write("")

            # Asign this value to q, for the Wells-Riley model.
            q = st.session_state.wls_quanta_dflt

    else: # Advanced Mode
        
        # Numerical input for the quanta emission rate.
        st.number_input("Quanta emission rate per hour",
                        min_value = 1,
                        key = "wls_quanta",
                        help = "There must be at least one quanta emitted per hour. This can vary by disease and activity.")
        st.write("")
        st.write(f"**The Quanta emission rate is {st.session_state.wls_quanta}/h.**")

        # Assigning the quanta emission rate to the variable 'q', for the Wells-Riley equation.
        q = st.session_state.wls_quanta

    # Reference for quanta emission rate data: Mikszewski, 2022, "The airborne contagiousness of respiratory viruses: A comparative analysis and implications for mitigation", Volume 13, Issue 6.
    # Reference for mask efficiency data: Shah, 2021, "Experimental investigation of indoor aerosol dispersion and accumulation in the context of COVID-19: Effects of masks and ventilation", Volume 33, Issue 7.

    st.divider()

#======================================================================
# EXPOSURE TIME:
#======================================================================
    
    st.write("### ⏱️ Exposure Time")

    st.write("")
    st.write("")

    # Users can pick between measuring exposure time by hours or minutes. Hours is the default option.
    wls_time_units = st.radio("Units of measure:", ["Hours", "Minutes"], index = 0)

    st.write("")

    if wls_time_units == "Hours":
        st.slider("Exposure time in hours", # Slider to input hours if selected by user.
                  min_value = 0.25,
                  max_value = 24.0,
                  step = 0.25,
                  key = "wls_time_hours",
                  help = "Quater-hour inputs allow for greater precision.")
        st.write("")
        
        if st.session_state.wls_time_hours == 1.0:
            st.write("**The total exposure time was 1 hour.**")
        else:
            st.write(f"**The total exposure time was {st.session_state.wls_time_hours} hours.**")

        # If hours were selected, assign the associated value to the variable 't', for the Wells-Riley equation.
        t = st.session_state.wls_time_hours
            
    else:
        st.number_input("Exposure time in minutes", # Numerical input to enter minutes if selected by user.
                        min_value = 1,
                        key = "wls_time_minutes",
                        help = "Exposure time must have lasted for at least one minute.")
        st.write("")
        
        if st.session_state.wls_time_minutes == 1.0:
            st.write("**The total exposure time was 1 minute.**")
        else:
            st.write(f"**The total exposure time was {st.session_state.wls_time_minutes} minutes.**")

        # If minutes were selected, use the associated value and convert to hours.
        t = st.session_state.wls_time_minutes / 60

    st.divider()

#======================================================================
# ROOM VENTILATION RATE:
#======================================================================

    st.write("### 💨 Room Ventilation Rate")

    st.write("")
    st.write("")

    # Dictionary containing room ventilation rate data (ACH) for various different settings.
    ventilation_dict = {
        "Education": {"Assembly Halls": 4, "Classrooms": 6, "Computer Rooms": 15},
        "Healthcare": {"Dental Centres": 8, "Pharmacies": 6, "Hospital Rooms (Sterilising)": 15, "Hospital Rooms (Wards)": 6, "Hospital Rooms (X-Ray)": 10, "Medical Centres": 8, "Medical Clinics": 8, "Medical Offices": 8},
        "Hospitality": {"Bars": 20, "Cafeterias": 12, "Cocktail Lounges": 20, "Lunch Rooms": 12, "Nightclubs": 20, "Restaurants (Dining Area)": 8, "Restaurants (Food Staging)": 10, "Restaurants (Kitchens)": 30, "Restaurants (Bars)": 15, "Tavern": 20},
        "Commercial": {"Banks": 4, "Court Houses": 4, "Conference Rooms": 8, "Fire Stations": 4, "Offices (Public)": 3, "Offices (Business)": 6, "Office Lunch Rooms": 7, "Police Stations": 4, "Post Offices": 4, "Retail": 6, "Shopping Centres": 6, "Supermarkets": 4},
        "Recreational": {"Auditoriums": 12, "Bowling Alleys": 10, "Clubhouses": 20, "Dance Halls": 6, "Gyms": 6, "Museums": 12, "Swimming Pools": 20, "Theatres": 8},
        "Industrial/Technical": {"Factory Buildings": 2, "Factory Buildings with Fumes/Moisture": 10, "Laboratories": 6, "Pig Houses": 6, "Poultry Houses": 6, "Warehouses": 6}
    }

    fiat500_size_m3 = 8.65
    # This is the size of a FIAT 500 in m³, rounded to two decimal places. The users can use the number of FIAT 500's that they can fit into their setting to estimate the volume of their room.

    # Defining an empty area that will allow the user to pick from our list of default ACH values depending on what their setting is.
    dflt_vent_space = st.empty()

    adv_md_vent = st.toggle("Room Ventilation Rate Advanced Mode", value = False, help = "*Activate Advanced Mode to enter your own custom value*")
    # Below the above area, the user can toggle between using one of our predefined ACH values, or they can enter their own value.
    # 'Advanced Mode', where the user can enter their own ACH value, is toggled off by default.

    st.write("")

    if not adv_md_vent: # If Advanced Mode is toggled off.
        with dflt_vent_space.container():
            # Fill the predefined empty space with choices for several ACH values associated with various settings. Users will also describe their space by the number of small cars (FIAT 500's) that they can fit into it.
            st.write("**ACH:**")
            # The user will pick which of these categories their setting would fall in.
            user_cat_choice = st.selectbox("Which of these categories would your setting fall in?", ["Education", "Healthcare", "Hospitality", "Commercial", "Recreational", "Industrial/Technical"])
            # Depending on the category chosen by the user, they will then pick their setting.
            if user_cat_choice == "Education":
                user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Assembly Halls", "Classrooms", "Computer Rooms"])
            elif user_cat_choice == "Healthcare":
                user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Dental Centres", "Pharmacies", "Hospital Rooms (Sterilising)", "Hospital Rooms (Wards)", "Hospital Rooms (X-Ray)", "Medical Centres", "Medical Clinics", "Medical Offices"])
            elif user_cat_choice == "Hospitality":
                user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Bars", "Cafeterias", "Cocktail Lounges", "Lunch Rooms", "Nightclubs", "Restaurants (Dining Area)", "Restaurants (Food Staging)", "Restaurants (Kitchens)", "Restaurants (Bars)", "Tavern"])
            elif user_cat_choice == "Commercial":
                user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Banks", "Court Houses", "Conference Rooms", "Fire Stations", "Offices (Public)", "Offices (Business)", "Office Lunch Rooms", "Police Stations", "Post Offices", "Retail", "Shopping Centres", "Supermarkets"])
            elif user_cat_choice == "Recreational":
                user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Auditoriums", "Bowling Alleys", "Clubhouses", "Dance Halls", "Gyms", "Museums", "Swimming Pools", "Theatres"])
            elif user_cat_choice == "Industrial/Technical":
                user_stng_choice = st.selectbox("Please choose the setting that applies to you", ["Factory Buildings", "Factory Buildings with Fumes/Moisture", "Laboratories", "Pig Houses", "Poultry Houses", "Warehouses"])

            # Find the corresponding values in the dictionary based on the users input and print this to the screen.
            dflt_ach = ventilation_dict[user_cat_choice][user_stng_choice]
            st.write(f"**The minimum ACH of your setting should be {dflt_ach}, according to government and legislative advice correct as of December 2021.**")
            st.write("")

            st.write("**ROOM VOLUME (m³):**")
            # The user will input how many FIAT 500's they believe can fit into their space.
            user_car_num = st.number_input("How many small cars (FIAT 500's) can you fit into the space",
                            min_value = 1,
                            help = "For this risk assessment, we have taken the volume of a FIAT 500 to be 8.65m³")
            dflt_room_vol = round(fiat500_size_m3 * user_car_num, 2) # The volume of one FIAT 500 is multiplied by the users input to estimate the total volume of their space. This is then printed to the screen to give the user some idea.
            st.write(f"**The volume of your space is estimated to be {dflt_room_vol}m³.**")
            st.write("")

            # We convert the ACH into m³/h by multiplying it with the Room Volume and store this in the respective variables.
            st.session_state.wls_ventilation_dflt = dflt_ach * dflt_room_vol
            Q = st.session_state.wls_ventilation_dflt

    else: # Advanced Mode
    
        # Users can pick between various units of measure. m³/h is the default option.
        wls_ventilation_unit = st.radio("Units of measure:", ["m³/h", "ACH", "L/s"], index = 0)

        st.write("")

        if wls_ventilation_unit == "m³/h":
            st.number_input("Room ventilation rate in m³/h", # Numerical input for ventilation rate (m³/h) if selected by user.
                            key = "wls_ventilation_m3h")
            st.write("")
            st.write(f"**The room ventilation rate is {st.session_state.wls_ventilation_m3h}m³/h.**")
    
            # This if-statement encourages the user to enter a non-zero value for the ventilation rate, helping to avoid a ZeroDivisionError.
            if st.session_state.wls_ventilation_m3h <= 0:
                st.warning("The room ventilation rate must be greater than 0 for a valid risk assessment.")

            # If m³/h was selected, assign the associated value to the variable 'Q', for the Wells-Riley equation.
            Q = st.session_state.wls_ventilation_m3h

        elif wls_ventilation_unit == "ACH":
            st.write("**ACH:**")
            ACH = st.number_input("Room ventilation rate in ACH") # Numerical input for ventilation rate (ACH) if selected by user.)
            st.write(f"**The room ventilation rate is {ACH}ACH.**")

            # This if-statement encourages the user to enter a non-zero value for the ventilation rate, helping to avoid a ZeroDivisionError.
            if ACH <= 0:
                st.warning("The room ventilation rate must be greater than 0 for a valid risk assessment.")

            st.write("")

            st.write("**ROOM VOLUME (m³):**") # Room volume is required alongside ACH to calculate room ventilation rate.
            vol_inp = st.checkbox("I'm not sure what the volume of my room is", False) # Users can select if they do not know their room volume.
            if not vol_inp:
                vol = st.number_input("Room volume in m³") # Numerical input for room volume.
                st.write(f"**The room volume is {vol}m³**")

                # This if-statement encourages the user to enter a non-zero value for the ventilation rate, helping to avoid a ZeroDivisionError.
                if vol <= 0:
                    st.warning("The room volume must be greater than 0 for a valid risk assessment")
        
            else: # If the users do not know their room volume, they will input the length, width, and height of their room.
                vol_col1, vol_col2, vol_col3 = st.columns(3)
                with vol_col1:
                    length = st.number_input("Length (m)")
                with vol_col2:
                    width = st.number_input("Width (m)")
                with vol_col3:
                    height = st.number_input("Height (m)")
                vol = length * width * height # Calculating volume.
                st.write(f"**The room volume is {vol}m³**")

                # This if-statement encourages the user to enter a non-zero value for the ventilation rate, helping to avoid a ZeroDivisionError.
                if vol <= 0:
                    st.warning("The room volume must be greater than 0 for a valid risk assessment")

            # Calculating room ventilation rate.
            st.session_state.wls_ventilation_ach = ACH * vol

            # If ACH was selected, convert and assign the associated value.
            Q = st.session_state.wls_ventilation_ach

        elif wls_ventilation_unit == "L/s":
            st.number_input("Room ventilation rate in L/s", # Numerical input for ventilation rate (L/s) if selected by user.
                            key = "wls_ventilation_ls")
            st.write("")
            st.write(f"**The room ventilation rate is {st.session_state.wls_ventilation_ls}L/s.**")
    
            # This if-statement encourages the user to enter a non-zero value for the ventilation rate, helping to avoid a ZeroDivisionError.
            if st.session_state.wls_ventilation_ls <= 0:
                st.warning("The room ventilation rate must be greater than 0 for a valid risk assessment.")

            # If L/s was selected, use the associated value and convert to m³/h.
            Q = st.session_state.wls_ventilation_ls * 3.6

# Reference for recommended ACH values: https://www.axaironline.co.uk/media/attachment/attachment/Air-Change-per-Hour-Document.pdf
# Reference for FIAT 500 dimensions: https://www.carwow.co.uk/fiat/500/specifications#gref

#====================================================================================================================================================
# OUTPUT TAB:
#====================================================================================================================================================

# This tab will present the risk assessment.
with tab3:

#======================================================================
# INFECTION PROBABILITY:
#======================================================================

    st.write("### 📊 Infection Probability")

    st.write("")
    st.write("")
    
    @st.cache_data # Caches the models output to avoid recomputing when previous inputs are used.
    def wells_riley(I, p, q, t, Q):
        """
        This function calculates the probability of infection using the Wells-Riley model.

        Args:
            I (int): The number of infected individuals.
            p (float): The breathing rate of any susceptible individual.
            q (int): The quanta emission rate.
            t (float): The exposure time.
            Q (float): The ventilation rate.

        Returns:
            float: The probability of infection (P)
        """
        try:
            P = 1 - math.exp(- (I * p * q * t) / Q)
        except ZeroDivisionError: # If Q <= 0, instead of a ZeroDivisionError, P will equal 0.
            P = 0
        return P

    st.write(f"The estimated probability of infection for one susceptible individual is: **{wells_riley(I, p, q, t, Q):.2%}**")
    
    st.divider()

#======================================================================
# TOTAL NUMBER OF INFECTIONS:
#======================================================================

    st.write("### 🤒 Number Of New Infections")

    st.write("")
    st.write("")
    
    # Calculating the estimated total number of infections.
    wls_prob = wells_riley(I, p, q, t, Q) # Probability of infection.
    wls_diff = st.session_state.wls_all - st.session_state.wls_infectors # Susceptible.
    wls_est_infs = math.ceil(wls_diff * wls_prob) # Number of new infections.
    # 'math.ceil' rounds the value up. For example, if the value is 2.3, you cannot have 0.3 of an infection - the value is rounded up as the third individual is still susceptible to infection.

    # Visualising the number of new infections among the susceptible population.
    wls_healthy = wls_diff - wls_est_infs # Susceptible - new infections = Number of uninfected.
    st.write("🧍‍♂️" * wls_est_infs + " **|** " + "🧍" * wls_healthy)
    st.caption("🧍‍♂️ - Infected | 🧍 - Uninfected")

    # This if-statement avoids printing a negative number, in case the user has entered invalid inputs.
    if wls_est_infs > 0:
        st.write(f"The estimated number of new infections is: **{wls_est_infs}**")
    else:
        st.write(f"The estimated number of new infections is: **0**")

    st.divider()

#======================================================================
# ESTIMATED PROBABILITY OF INFECTION OVER TIME:
#======================================================================

    st.write("### 📈 Estimated Probability Of Infection Over Time")

    st.write("")
    st.write("")

    # Creating a time range:
    # Calculate the maximum time for the time range.
    wls_max_time = t * 3
    # We want a time point every five minutes.
    wls_time_res = 5 / 60
    # We need to calculate the number of time points we need.
    wls_num_time_points = int(wls_max_time / wls_time_res) + 1 # Add one to ensure the final time point is included.
    # Finally, we can create a NumPy array containing the entire range of time points.
    wls_time_range = np.linspace(0, wls_max_time, wls_num_time_points)

    @st.cache_data
    def wls_plot(wls_time_range, I, p, q, Q):
        """
        This function produces a line chart that plots the estimated probability of infection over time

        Args:
            wls_time_range (NumPy array): A NumPy array of time points.
            I (int): The number of infected individuals.
            p (float): The breathing rate of any susceptible individual.
            q (int): The quanta emission rate.
            Q (float): The ventilation rate.
        """

        wls_list_probs = [] # Create an empty list to store the probability of infection at each time point.
        for time in wls_time_range:
            wls_list_probs.append(wells_riley(I, p, q, time, Q) * 100) # For each time point in the time range, calculate and store the probability of infection.

        # Pandas DataFrame containing all time points in the time range, and their respective probability of infection.
        wls_probvtime_data = pd.DataFrame({
            "Time (hours)": wls_time_range,
            "Probability Of Infection": wls_list_probs})

        # Plotting the DataFrame
        st.line_chart(
            data = wls_probvtime_data,
            x = "Time (hours)",
            y = "Probability Of Infection",
            x_label = "Exposure Time (hours)",
            y_label = "Probability of Infection (%)"
        )

    # Call the above function to produce the plot.
    wls_plot(wls_time_range, I, p, q, Q)

    # Adding an alternate scenario where the Quanta Emission Rate has increased, this should encourage the user to further explore their data by changing their inputs.
    st.write("")
    st.write("In the above graph, we have captured the relationship between the duration of exposure and the estimated probability of infection.")
    st.write("But what would this graph look like if your data were different?")
    wls_quanta_explr = st.checkbox("Show what would happen if we multiplied your current Quanta Emission Rate by 100", False) # User's can tick this checkbox to explore what changes an increase in Quanta emission rate would lead to.

    if wls_quanta_explr: # If the checkbox is ticked...
        q = q * 100 # ... increase the users Quanta Emission Rate...
        st.write("")
        st.write("### ⬆️ Increased Quanta Emission Rate")
        st.write("")
        wls_plot(wls_time_range, I, p, q, Q) # ... and produce a new plot using this alternate Quanta emission rate value.

        st.write("")
        st.write("As we can see in the above graph, raising your Quanta Emission Rate increases the estimated probability of infection.")
        st.write("Why don't you go back and see what impact changing your data has on your risk assessment?")
    
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