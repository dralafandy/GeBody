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
def calculate_waist_to_hip_ratio(waist_to_hip_ratio):
    return waist_to_hip_ratio

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

# Calculate Bone Mineral Content
def calculate_bone_mineral_content(weight):
    return weight * 0.03

# Calculate Fat-Free Mass Index (FFMI) using the corrected height
def calculate_ffmi(weight, height, body_fat_percentage):
    # Calculate lean body mass
    lean_body_mass = calculate_lean_body_mass(weight, body_fat_percentage)
    
    # Calculate FFMI using the lean body mass and height
    ffmi = lean_body_mass / ((height) ** 2) + 6.1 * (1.8 - height)
    
    return ffmi

# Calculate Resting Metabolic Rate (RMR)
def calculate_rmr(weight, height, age, sex):
    if sex == 'Male':
        rmr = 9.99 * weight + 6.25 * height * 100 - 4.92 * age + 5
    else:
        rmr = 9.99 * weight + 6.25 * height * 100 - 4.92 * age - 161
    return rmr

def calculate_ideal_weight(height, sex):
    ideal_weight_male = 22 * (height ** 2)
    ideal_weight_female = 21 * (height ** 2)
    return ideal_weight_male if sex == 'Male' else ideal_weight_female


def calculate_weight_difference(weight, ideal_weight):
    difference = weight - ideal_weight
    if difference < -0.5:
        return "Gain weight", abs(difference)
    elif difference > 0.5:
        return "Lose weight", abs(difference)
    else:
        return "Maintain weight", abs(difference)

def main():
    st.title('GeBody - Body Composition Analyzer')

    name = st.text_input('Enter patient name:')
    age = st.number_input('Enter age:', min_value=0, max_value=150, value=30)
    sex = st.radio('Select sex:', ('Male', 'Female'))
    weight = st.number_input('Enter weight (kg):', min_value=0.0, value=70.0)
    height = st.number_input('Enter height (m):', min_value=0.0, value=1.7)
    waist_hip_ratio = st.number_input('Enter waist/hip ratio:', min_value=0.0, value=0.9)
    body_fat_percentage = st.number_input('Enter body fat percentage:', min_value=0.0, max_value=100.0, value=20.0)

    if st.button('Calculate'):
        # Perform calculations
        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age, sex)
        lean_body_mass = calculate_lean_body_mass(weight, body_fat_percentage)
        body_fat_mass = calculate_body_fat_mass(weight, body_fat_percentage)
        waist_to_hip_ratio = calculate_waist_to_hip_ratio(waist_hip_ratio)
        muscle_mass = calculate_muscle_mass(weight, body_fat_percentage)
        visceral_fat_level = calculate_visceral_fat_level(waist_to_hip_ratio, sex)
        body_water_percentage = calculate_body_water_percentage(weight, body_fat_percentage, sex)
        bone_mineral_content = calculate_bone_mineral_content(weight)
        ffmi = calculate_ffmi(weight, height, body_fat_percentage)
        rmr = calculate_rmr(weight, height, age, sex)
        ideal_weight = calculate_ideal_weight(height, sex)
        weight_status, weight_difference = calculate_weight_difference(weight, ideal_weight)
        insert_patient_data(name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage)
        st.success('Patient data saved successfully!')

        # Grouping results into categories
        body_composition_results = {
            'BMI': bmi,
            'BMR': bmr,
            'Lean Body Mass': lean_body_mass,
            'Body Fat Mass': body_fat_mass,
            'Waist-to-Hip Ratio': waist_to_hip_ratio,
            'Muscle Mass': muscle_mass,
            'Visceral Fat Level': visceral_fat_level,
            'Body Water Percentage': body_water_percentage,
            'Bone Mineral Content': bone_mineral_content,
            'Fat-Free Mass Index (FFMI)': ffmi,
            'Resting Metabolic Rate (RMR)': rmr,
            'Ideal Weight': ideal_weight, 
            'Weight Status': weight_status,
            'Weight Difference': weight_difference
        }

        # Displaying results in separate collapsible sections with improved formatting
        st.write('## Results')

        for result, value in body_composition_results.items():
            unit = ""
            if result in ["BMI", "Lean Body Mass", "Body Fat Mass", "Muscle Mass", "Bone Mineral Content", "Fat-Free Mass Index (FFMI)", "Ideal Weight", "Weight Difference"]:
                unit = "kg"
            elif result in ["BMR", "RMR"]:
                unit = "kcal/day"
            elif result == "Body Water Percentage":
                unit = "%"
            elif result == "Waist-to-Hip Ratio":
                unit = ""
            normal_range = normal_ranges.get(result)
            if normal_range is not None:
                # Calculate status based on predefined thresholds
                status = ""
                if result in findings:
                    for ind, description in findings[result].items():
                        if normal_range[0] <= value <= normal_range[1]:
                            status = ind
                            break

                progress_value = max(0, min(1, (value - normal_range[0]) / (normal_range[1] - normal_range[0])))
                color = 'green' if status == 'Normal' else 'red'
                st.markdown(f'### {result}')
                st.markdown(f'Result: {value} {unit} (Normal Range: {normal_range[0]} - {normal_range[1]} {unit})')
                st.markdown(f"Status: {status}")
                st.markdown(f"Finding: {findings[result].get(status, 'No finding available')}")
                st.markdown(f'<progress value="{value}" max="{normal_range[1]}" style="width: 100%; background-color: {color};"></progress>', unsafe_allow_html=True)

        if st.button('Show Recommendations'):
            st.write('## Recommendations')

            # Analyze the calculated results and provide personalized recommendations
            if bmi < 18.5:
                st.write("Your BMI indicates that you are underweight. It's important to focus on increasing your calorie intake and incorporating strength training exercises to build muscle mass.")
            elif 18.5 <= bmi <= 24.9:
                st.write("Your BMI falls within the normal range. Keep up the good work with your diet and exercise routine to maintain a healthy weight.")
            elif 25 <= bmi <= 29.9:
                st.write("Your BMI indicates that you are overweight. Consider reducing your calorie intake and increasing physical activity to achieve a healthy weight.")
            else:
                st.write("Your BMI indicates that you are obese. It's crucial to prioritize weight loss through a balanced diet and regular exercise under medical supervision.")

            if bmr < 1500:
                st.write("Your BMR is lower than the normal range. Ensure that you are consuming enough calories to support your body's basic metabolic needs.")
            elif 1500 <= bmr <= 2500:
                st.write("Your BMR falls within the normal range. This is the number of calories your body needs to maintain basic functions at rest.")
            else:
                st.write("Your BMR is higher than normal. Regular physical activity may contribute to a higher metabolic rate, but consult with a healthcare professional if you have concerns.")

            if lean_body_mass < 50:
                st.write("Your lean body mass is lower than normal. Incorporate resistance training exercises and ensure adequate protein intake to help build and maintain muscle mass.")
            elif 50 <= lean_body_mass <= 90:
                st.write("Your lean body mass falls within the normal range. Lean body mass consists of muscles, bones, organs, and tissues that are metabolically active.")
            else:
                st.write("Your lean body mass is higher than normal. This can be advantageous for overall health and metabolism, but maintain a balanced lifestyle.")

            if body_fat_percentage < 10:
                st.write("Your body fat percentage is lower than normal. While having low body fat levels may be desirable for some, ensure that it does not compromise your overall health.")
            elif 10 <= body_fat_percentage <= 30:
                st.write("Your body fat percentage falls within the normal range. This range is considered healthy for most individuals.")
            else:
                st.write("Your body fat percentage is higher than normal. Consider incorporating aerobic exercises and dietary changes to reduce body fat levels.")

            # Add more recommendations based on other parameters as needed

    if st.button('Show Data'):
        data = fetch_patient_data(name)
        if data:
            st.write('## Patient Data')
            headers = ["ID", "Name", "Age", "Sex", "Weight", "Height", "Waist-to-Hip Ratio", "Body Fat Percentage"]
            data_df = pd.DataFrame(data)  # Use only the necessary number of headers
            st.dataframe(data_df)
        else:
            st.warning('No data found for this patient.')

if __name__ == '__main__':
    main()

