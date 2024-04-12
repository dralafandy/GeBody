import streamlit as st
import pandas as pd
import sqlite3

# Function to insert patient data into the database
def insert_patient_data(name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage):
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO patients (name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage))
    conn.commit()
    conn.close()

# Function to fetch patient data for the current user
def fetch_patient_data(name):
    conn = sqlite3.connect('patient_data.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM patients WHERE name = ?''', (name,))
    data = c.fetchall()
    conn.close()
    return data

# Define normal ranges for each parameter
normal_ranges = {
    'BMI': (18.5, 24.9),
    'BMR': (1500, 2500),  
    'Lean Body Mass': (50, 90),  
    'Body Fat Mass': (10, 30),  
    'Waist-to-Hip Ratio': (0.8, 0.85),  # Updated to commonly accepted range
    'Muscle Mass': (40, 60),  
    'Visceral Fat Level': (1, 12),  # Updated to commonly accepted range
    'Body Water Percentage': (45, 60),  
    'Bone Mineral Content': (1.5, 3.5),  
    'Fat-Free Mass Index (FFMI)': (17, 23),  
    'Body Adiposity Index (BAI)': (8, 21),  # Updated to commonly accepted range
    'Resting Metabolic Rate (RMR)': (1500, 2500)  
}

# Define findings for each result
findings = {
    'BMI': {
        'Underweight': 'Your BMI indicates that you are underweight.',
        'Normal weight': 'Your BMI falls within the normal range.',
        'Overweight': 'Your BMI indicates that you are overweight.',
        'Obesity': 'Your BMI indicates that you are obese.'
    },
    'BMR': {
        'Low': 'Your BMR is lower than normal, which may indicate a slower metabolism.',
        'Normal': 'Your BMR falls within the normal range.',
        'High': 'Your BMR is higher than normal, which may indicate a faster metabolism.'
    },
    'Lean Body Mass': {
        'Low': 'Your lean body mass is lower than normal.',
        'Normal': 'Your lean body mass falls within the normal range.',
        'High': 'Your lean body mass is higher than normal.'
    },
    # Define findings for other parameters similarly
    'Body Fat Mass': {
        'Low': 'Your body fat mass is lower than normal.',
        'Normal': 'Your body fat mass falls within the normal range.',
        'High': 'Your body fat mass is higher than normal.'
    },
    'Waist-to-Hip Ratio': {
        'Normal': 'Your waist-to-hip ratio falls within the normal range.'
    },
    'Muscle Mass': {
        'Low': 'Your muscle mass is lower than normal.',
        'Normal': 'Your muscle mass falls within the normal range.',
        'High': 'Your muscle mass is higher than normal.'
    },
    'Visceral Fat Level': {
        'Low': 'Your visceral fat level is lower than normal.',
        'Normal': 'Your visceral fat level falls within the normal range.',
        'High': 'Your visceral fat level is higher than normal.'
    },
    'Body Water Percentage': {
        'Low': 'Your body water percentage is lower than normal.',
        'Normal': 'Your body water percentage falls within the normal range.',
        'High': 'Your body water percentage is higher than normal.'
    },
    'Bone Mineral Content': {
        'Low': 'Your bone mineral content is lower than normal.',
        'Normal': 'Your bone mineral content falls within the normal range.',
        'High': 'Your bone mineral content is higher than normal.'
    },
    'Fat-Free Mass Index (FFMI)': {
        'Low': 'Your FFMI is lower than normal.',
        'Normal': 'Your FFMI falls within the normal range.',
        'High': 'Your FFMI is higher than normal.'
    },
    'Body Adiposity Index (BAI)': {
        'Normal': 'Your BAI falls within the normal range.'
    },
    'Resting Metabolic Rate (RMR)': {
        'Low': 'Your RMR is lower than normal.',
        'Normal': 'Your RMR falls within the normal range.',
        'High': 'Your RMR is higher than normal.'
    }
}

# Calculate BMI
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Calculate BMR (Basal Metabolic Rate)
def calculate_bmr(weight, height, age, sex):
    if sex == 'Male':
        bmr = 10 * weight + 6.25 * height * 100 - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height * 100 - 5 * age - 161
    return bmr

# Calculate Lean Body Mass
def calculate_lean_body_mass(weight, body_fat_percentage):
    return weight * (1 - body_fat_percentage / 100)

# Calculate Body Fat Mass
def calculate_body_fat_mass(weight, body_fat_percentage):
    return weight * (body_fat_percentage / 100)

# Calculate Waist-to-Hip Ratio
def calculate_waist_to_hip_ratio(waist_hip_ratio):
    return waist_hip_ratio

# Calculate Muscle Mass
def calculate_muscle_mass(weight, body_fat_percentage):
    lean_body_mass = calculate_lean_body_mass(weight, body_fat_percentage)
    return lean_body_mass * 0.85

# Calculate Visceral Fat Level
def calculate_visceral_fat_level(waist_hip_ratio, sex):
    if sex == 'Male':
        visceral_fat_level = 10 * waist_hip_ratio - 5
    else:
        visceral_fat_level = 10 * waist_hip_ratio - 6
    return visceral_fat_level

# Calculate Body Water Percentage
def calculate_body_water_percentage(weight, body_fat_percentage, sex):
    if sex == 'Male':
        lean_body_mass = weight * (1 - body_fat_percentage / 100)
        body_water_percentage = 60 + 0.1 * (lean_body_mass - 50)
    else:
        lean_body_mass = weight * (1 - body_fat_percentage / 100)
        body_water_percentage = 50 + 0.1 * (lean_body_mass - 45)
    return body_water_percentage
