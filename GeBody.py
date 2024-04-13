import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objs as go
from plotly.subplots import make_subplots


# Create a connection to the SQLite database
conn = sqlite3.connect('new_patient_data.db')
c = conn.cursor()

# Create a table to store patient data
c.execute('''CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                sex TEXT,
                weight REAL,
                height REAL,
                waist_hip_ratio REAL,
                body_fat_percentage REAL,
                bmi REAL,
                bmr REAL,
                lean_body_mass REAL,
                body_fat_mass REAL,
                muscle_mass REAL,
                visceral_fat_level REAL,
                body_water_percentage REAL,
                bone_mineral_content REAL,
                resting_metabolic_rate REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')

# Commit changes and close the connection
conn.commit()
conn.close()



# Function to insert patient data into the database
def insert_patient_data(name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage, bmi, bmr, lean_body_mass, body_fat_mass, muscle_mass, visceral_fat_level, body_water_percentage, bone_mineral_content, resting_metabolic_rate):
    conn = sqlite3.connect('new_patient_data.db')  # Connect to the new database
    c = conn.cursor()
    c.execute('''INSERT INTO patients (
                    name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage,
                    bmi, bmr, lean_body_mass, body_fat_mass, muscle_mass, visceral_fat_level,
                    body_water_percentage, bone_mineral_content, resting_metabolic_rate)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage,
               bmi, bmr, lean_body_mass, body_fat_mass, muscle_mass, visceral_fat_level,
               body_water_percentage, bone_mineral_content, resting_metabolic_rate))
    conn.commit()
    conn.close()

# Function to fetch patient data for the current user
def fetch_patient_data(name):
    conn = sqlite3.connect('new_patient_data.db')  # Connect to the new database
    c = conn.cursor()
    c.execute('''SELECT * FROM patients WHERE name = ?''', (name,))
    data = c.fetchall()
    conn.close()
    return data


# Define normal ranges for each parameter
normal_ranges = {
    'BMI': (18.5, 24.9),
    'BMR': (1200, 2500),  # Updated range based on Harris-Benedict equation
    'Lean Body Mass': (50, 90),
    'Body Fat Mass': (10, 30),
    'Waist-to-Hip Ratio': (0.8, 0.85),  # Updated to commonly accepted range
    'Muscle Mass': (40, 60),
    'Visceral Fat Level': (1, 12),  # Updated to commonly accepted range
    'Body Water Percentage': (45, 60),
    'Bone Mineral Content': (1.5, 3.5),
    'Resting Metabolic Rate (RMR)': (1200, 2500)  # Updated range based on Harris-Benedict equation
}

# Define findings for each result
findings = {
    'BMI': {
        'Underweight': 'Your BMI indicates that you are underweight. This may suggest a higher risk of certain health issues such as nutritional deficiencies and osteoporosis.',
        'Normal weight': 'Your BMI falls within the normal range. This indicates a healthy weight for your height.',
        'Overweight': 'Your BMI indicates that you are overweight. This may increase your risk of developing various health problems such as heart disease and type 2 diabetes.',
        'Obesity': 'Your BMI indicates that you are obese. Obesity is associated with an increased risk of several serious health conditions, including heart disease, stroke, type 2 diabetes, and certain cancers.'
    },
    'BMR': {
        'Low': 'Your BMR is lower than normal, which may indicate a slower metabolism. This could be due to various factors such as age, sex, muscle mass, and hormonal imbalances.',
        'Normal': 'Your BMR falls within the normal range. This suggests that your metabolism is functioning adequately to support basic bodily functions.',
        'High': 'Your BMR is higher than normal, which may indicate a faster metabolism. Factors such as genetics, physical activity level, and muscle mass can influence your metabolic rate.'
    },
    'Lean Body Mass': {
        'Low': 'Your lean body mass is lower than normal. Lean body mass includes muscles, bones, organs, and water. Increasing muscle mass through resistance training and consuming adequate protein can help improve lean body mass.',
        'Normal': 'Your lean body mass falls within the normal range. This suggests that you have an appropriate amount of muscle, bone, and other lean tissues for your height and weight.',
        'High': 'Your lean body mass is higher than normal. Having a higher lean body mass can indicate greater strength, endurance, and overall fitness. However, it\'s important to maintain a balance between muscle mass and body fat.'
    },
    'Body Fat Mass': {
        'Low': 'Your body fat mass is lower than normal. While a low body fat percentage may be desirable for some athletes, it can also indicate inadequate energy reserves and potential health risks. Ensure that you are consuming enough calories and nutrients to support your body\'s needs.',
        'Normal': 'Your body fat mass falls within the normal range. This suggests a healthy balance between lean tissues and stored fat.',
        'High': 'Your body fat mass is higher than normal. Excess body fat can increase the risk of various health conditions such as heart disease, diabetes, and certain cancers. Consider adopting a balanced diet and regular exercise routine to reduce body fat.'
    },
    'Waist-to-Hip Ratio': {
        'Normal': 'Your waist-to-hip ratio falls within the normal range. This indicates a healthy distribution of body fat, which may lower the risk of obesity-related health issues such as heart disease and diabetes.'
    },
    'Muscle Mass': {
        'Low': 'Your muscle mass is lower than normal. Adequate muscle mass is essential for strength, mobility, and overall health. Consider incorporating resistance training exercises and consuming sufficient protein to support muscle growth and maintenance.',
        'Normal': 'Your muscle mass falls within the normal range. This suggests good muscle development and overall physical fitness.',
        'High': 'Your muscle mass is higher than normal. Having greater muscle mass can enhance metabolism, strength, and functional capacity. Continue with your current exercise routine to maintain muscle health.'
    },
    'Visceral Fat Level': {
        'Low': 'Your visceral fat level is lower than normal. Visceral fat surrounds organs and can contribute to various health problems when elevated. Maintaining a healthy weight, engaging in regular physical activity, and consuming a balanced diet can help prevent visceral fat accumulation.',
        'Normal': 'Your visceral fat level falls within the normal range. This suggests a healthy distribution of fat within the body, which may lower the risk of metabolic disorders and cardiovascular disease.',
        'High': 'Your visceral fat level is higher than normal. Excess visceral fat is associated with an increased risk of metabolic syndrome, heart disease, and type 2 diabetes. Focus on lifestyle modifications such as dietary changes and increased physical activity to reduce visceral fat levels.'
    },
    'Body Water Percentage': {
        'Low': 'Your body water percentage is lower than normal. Adequate hydration is essential for various bodily functions, including temperature regulation, digestion, and nutrient transport. Increase your water intake and consume hydrating foods to maintain optimal hydration levels.',
        'Normal': 'Your body water percentage falls within the normal range. This suggests adequate hydration, which is crucial for overall health and well-being.',
        'High': 'Your body water percentage is higher than normal. While hydration is important, excessive water retention may indicate underlying health issues such as kidney dysfunction or hormonal imbalances. Consult with a healthcare professional for further evaluation.'
    },
    'Bone Mineral Content': {
        'Low': 'Your bone mineral content is lower than normal. Adequate bone mineral density is essential for skeletal health and reducing the risk of fractures and osteoporosis. Ensure adequate intake of calcium, vitamin D, and engage in weight-bearing exercises to promote bone health.',
        'Normal': 'Your bone mineral content falls within the normal range. This suggests good bone density and overall skeletal health. Maintain a balanced diet and engage in regular physical activity to support bone health.',
        'High': 'Your bone mineral content is higher than normal. While higher bone density is generally beneficial for skeletal strength, excessively high bone mineral content may indicate underlying health conditions such as hyperparathyroidism or certain cancers. Further evaluation may be warranted.'
    },
    'Resting Metabolic Rate (RMR)': {
        'Low': 'Your RMR is lower than normal, which may indicate a slower metabolism. A lower metabolic rate can make it more challenging to maintain or lose weight. Factors such as age, sex, body composition, and medical conditions can influence RMR.',
        'Normal': 'Your RMR falls within the normal range. This suggests that your metabolism is functioning adequately to support basic bodily functions at rest. Regular physical activity and dietary choices can influence metabolic rate.',
        'High': 'Your RMR is higher than normal, which may indicate a faster metabolism. A higher metabolic rate can lead to increased calorie burning and easier weight maintenance. Factors such as genetics, muscle mass, and thyroid function can influence RMR.'
    }
}

def plot_progressions(data):
    # Extracting data for plotting
    weight_data = [entry[4] for entry in data]  # Extracting weight from data
    body_fat_percentage_data = [entry[7] for entry in data]  # Extracting body fat percentage from data
    muscle_mass_data = [calculate_muscle_mass(entry[4], entry[7]) for entry in data]  # Calculating muscle mass from weight and body fat percentage

    # Creating Plotly subplot with two columns
    fig = make_subplots(rows=1, cols=3, subplot_titles=("Weight", "Body Fat Percentage", "Muscle Mass"))

    # Adding traces for weight, body fat percentage, and muscle mass
    fig.add_trace(go.Scatter(x=list(range(len(weight_data))), y=weight_data, mode='lines+markers', name='Weight', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=list(range(len(body_fat_percentage_data))), y=body_fat_percentage_data, mode='lines+markers', name='Body Fat Percentage', line=dict(color='green')), row=1, col=2)
    fig.add_trace(go.Scatter(x=list(range(len(muscle_mass_data))), y=muscle_mass_data, mode='lines+markers', name='Muscle Mass', line=dict(color='red')), row=1, col=3)

    # Updating layout
    fig.update_layout(title='Progressions Over Time')

    # Show plot
    fig.show()


# Calculate BMI
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Calculate Ideal Weight
def calculate_ideal_weight(height, sex):
    if sex == 'Male':
        return 50 + 0.91 * (height - 152.4)
    else:
        return 45.5 + 0.91 * (height - 152.4)

# Calculate Weight Difference
def calculate_weight_difference(current_weight, ideal_weight):
    difference = current_weight - ideal_weight
    status = "Normal" if difference == 0 else "Underweight" if difference < 0 else "Overweight"
    return status, abs(difference)

# Calculate Total Body Water (TBW)
def calculate_total_body_water(weight, height, age, sex):
    if sex == 'Male':
        tbw = 2.447 - 0.09156 * age + 0.1074 * height + 0.3362 * weight
    else:
        tbw = -2.097 + 0.1069 * height + 0.2466 * weight
    return tbw


# Calculate BMR (Basal Metabolic Rate) using Harris-Benedict equation
def calculate_bmr(weight, height, age, sex):
    if sex == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
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

# Calculate Resting Metabolic Rate (RMR)
def calculate_rmr(weight, height, age, sex):
    return calculate_bmr(weight, height, age, sex)

# Calculate Ideal Weight
def calculate_ideal_weight(height, sex):
    if sex == 'Male':
        return 50 + 0.91 * (height - 152.4)
    else:
        return 45.5 + 0.91 * (height - 152.4)



# Main function
def main():
    st.title('GeBody - Body Composition Analyzer')

    name = st.text_input('Enter patient name:')
    age = st.number_input('Enter age:', min_value=0, max_value=150, value=30)
    sex = st.radio('Select sex:', ('Male', 'Female'))
    weight = st.number_input('Enter weight (kg):', min_value=0.0, value=70.0)
    height = st.number_input('Enter height (cm):', min_value=0.0, value=170.0)
    waist_hip_ratio = st.number_input('Enter waist/hip ratio:', min_value=0.0, value=0.9)
    body_fat_percentage = st.number_input('Enter body fat percentage:', min_value=0.0, max_value=100.0, value=20.0)

    action = st.selectbox('Choose an action:', ['Calculate', 'Show Recommendations', 'Show Data'])

    if action == "Calculate":
        if st.button('Calculate'):
            # Perform calculations
            bmi = calculate_bmi(weight, height / 100)  # Convert height to meters
            bmr = calculate_bmr(weight, height, age, sex)
            lean_body_mass = calculate_lean_body_mass(weight, body_fat_percentage)
            body_fat_mass = calculate_body_fat_mass(weight, body_fat_percentage)
            waist_to_hip_ratio = calculate_waist_to_hip_ratio(waist_hip_ratio)
            muscle_mass = calculate_muscle_mass(weight, body_fat_percentage)
            visceral_fat_level = calculate_visceral_fat_level(waist_to_hip_ratio, sex)
            body_water_percentage = calculate_body_water_percentage(weight, body_fat_percentage, sex)
            bone_mineral_content = calculate_bone_mineral_content(weight)
            rmr = calculate_rmr(weight, height, age, sex)
            ideal_weight = calculate_ideal_weight(height, sex)
            weight_status, weight_difference = calculate_weight_difference(weight, ideal_weight)
            total_body_water = calculate_total_body_water(weight, height, age, sex)  # Calculate total body water
            insert_patient_data(name, age, sex, weight, height, waist_hip_ratio, body_fat_percentage,
                                 bmi, bmr, lean_body_mass, body_fat_mass, muscle_mass,
                                 visceral_fat_level, body_water_percentage, bone_mineral_content, rmr)
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
                'Resting Metabolic Rate (RMR)': rmr,
                'Ideal Weight': ideal_weight,
                'Weight Status': weight_status,
                'Weight Difference': weight_difference,
                'Total Body Water': total_body_water  # Add total body water to results
            }

            # Displaying results in separate collapsible sections with improved formatting
            st.write('## Results')

            for result, value in body_composition_results.items():
                unit = ""
                if result in ["BMI", "Lean Body Mass", "Body Fat Mass", "Muscle Mass", "Bone Mineral Content", "Ideal Weight", "Weight Difference", "Total Body Water"]:
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

    elif action == "Show Recommendations":
        recommendations = []

        # Generate diet-related recommendations based on BMI
        bmi = calculate_bmi(weight, height / 100)  # Convert height to meters
        if bmi:
            if 18.5 <= bmi <= 24.9:
                recommendations.append("Your BMI falls within the normal range. Keep up the good work with your diet and exercise routine to maintain a healthy weight.")
            elif bmi < 18.5:
                recommendations.append("Your BMI indicates that you are underweight. Consider increasing your calorie intake with nutrient-dense foods like nuts, avocados, and lean proteins.")
            else:
                recommendations.append("Your BMI indicates that you are overweight or obese. Focus on a balanced diet rich in fruits, vegetables, whole grains, and lean proteins. Consider consulting a nutritionist for personalized dietary recommendations.")

        # Generate recommendations based on other parameters
        if body_fat_percentage:
            if body_fat_percentage < 10:
                recommendations.append("Your body fat percentage is extremely low. It's important to maintain a healthy level of body fat to support bodily functions. Consider consulting a healthcare professional for personalized advice.")
            elif body_fat_percentage > 30:
                recommendations.append("Your body fat percentage is higher than normal. Consider incorporating more physical activity and dietary changes to reduce body fat levels.")
            else:
                recommendations.append("Your body fat percentage falls within the normal range. Keep up the good work with your diet and exercise routine.")

        if waist_hip_ratio:
            if sex == 'Male':
                if waist_hip_ratio > 0.9:
                    recommendations.append("Your waist-to-hip ratio indicates higher abdominal fat. Consider incorporating more cardiovascular exercises and reducing calorie intake to target abdominal fat.")
                else:
                    recommendations.append("Your waist-to-hip ratio falls within the normal range. Keep up the good work with your fitness routine.")
            else:
                if waist_hip_ratio > 0.85:
                    recommendations.append("Your waist-to-hip ratio indicates higher abdominal fat. Consider incorporating more cardiovascular exercises and reducing calorie intake to target abdominal fat.")
                else:
                    recommendations.append("Your waist-to-hip ratio falls within the normal range. Keep up the good work with your fitness routine.")

        # Display recommendations
        if recommendations:
            st.write('## Recommendations')
            for recommendation in recommendations:
                st.write(recommendation)
        else:
            st.write("No specific recommendations available based on the provided data.")

    elif action == "Show Data":
        data = fetch_patient_data(name)
        if data:
            st.write('## Patient Data')
            headers = ["ID", "Name", "Age", "Sex", "Weight", "Height", "Waist-to-Hip Ratio", "Body Fat Percentage"]
            data_df = pd.DataFrame(data)
            st.dataframe(data_df)
            # Plot progressions if data is available
            st.write('## Progressions Over Time')
            plot_progressions(data)
        else:
            st.warning('No data found for this patient.')


if __name__ == '__main__':
    main()
