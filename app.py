import streamlit as st

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def calculate_ideal_weight(height, gender):
    if gender == "Male":
        return 50 + 0.91 * (height - 152.4)
    elif gender == "Female":
        return 45.5 + 0.91 * (height - 152.4)
    else:
        return None

def calculate_ideal_body_weight(height, gender):
    if gender == "Male":
        return 50 + 0.91 * (height - 152.4)
    elif gender == "Female":
        return 45.5 + 0.91 * (height - 152.4)
    else:
        return None

def calculate_body_fat_percentage(weight, body_fat_mass):
    return (body_fat_mass / weight) * 100

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "Female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return None

def calculate_tdee(bmr, activity_level):
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Extra active": 1.9
    }
    return bmr * activity_factors[activity_level]

def calculate_calorie_intake(tdee, goals, weight, ideal_weight):
    if "Fitness" in goals:
        if weight < ideal_weight:
            goals.append("Weight gain")
        elif weight > ideal_weight:
            goals.append("Weight loss")
    if "Weight loss" in goals:
        if "Rapid Weight Loss" in goals:
            return tdee - 1000  # Subtract 1000 kcal/day for rapid weight loss
        else:
            return tdee - 500
    elif "Weight gain" in goals:
        return tdee + 500
    elif "Fitness" in goals:
        return tdee  # No calorie adjustment for fitness goal, treat it as Ideal Weight
    else:
        return tdee

def calculate_tbw(weight, height, age, gender):
    if gender == "Male":
        k = 2.447 - 0.09516 * age + 0.1074 * height + 0.3362 * weight
    elif gender == "Female":
        k = -2.097 + 0.1069 * height + 0.2466 * weight
    else:
        return None
    
    return 0.3669 * k - 0.0906 * weight + 0.1074 * height + 0.2466 * weight

def user_input_page():
    st.title("Ai Calorie Calculator")

    # Sidebar for additional options
    st.sidebar.title("Options")

    # Age input
    age = st.sidebar.number_input("Enter your age", min_value=1, max_value=150, step=1)

    # Gender selection
    gender = st.sidebar.selectbox("Select your gender", options=["Male", "Female", "Other"])

    # Weight and height input
    st.sidebar.subheader("Weight and Height:")
    weight = st.sidebar.number_input("Enter your weight (kg)", min_value=0.0, step=0.1)
    height = st.sidebar.number_input("Enter your height (cm)", min_value=0.0, step=0.1)

    # Body composition input
    st.sidebar.subheader("Body Composition:")
    body_fat_percentage = st.sidebar.number_input("Enter your body fat percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
    waist_to_hip_ratio = st.sidebar.number_input("Enter your waist-to-hip ratio", min_value=0.0, step=0.01)
    lean_body_mass = st.sidebar.number_input("Enter your lean body mass (kg)", min_value=0.0, step=0.1)

    # Calculate BMI
    bmi = calculate_bmi(weight, height)

    # Calculate total body water (TBW)
    tbw = calculate_tbw(weight, height, age, gender)

    # Calculate ideal weight
    ideal_weight = calculate_ideal_weight(height, gender)

    # Calculate ideal body weight
    if gender == "Male":
        ideal_body_weight = 50 + 2.3 * ((height * 0.393701) - 60)  # Convert height to inches
    elif gender == "Female":
        ideal_body_weight = 45.5 + 2.3 * ((height * 0.393701) - 60)  # Convert height to inches
    else:
        ideal_body_weight = None

    if ideal_body_weight:
        st.write(f"Ideal Body Weight (Devine formula): {ideal_body_weight:.2f} kg")
    else:
        st.write("Unable to calculate ideal body weight: Gender not specified.")


    # Calculate body fat mass
    body_fat_mass = weight * (body_fat_percentage / 100)

    # Calculate BMR
    bmr = calculate_bmr(weight, height, age, gender)

    # Calculate TDEE
    activity_level = st.selectbox("Select your activity level", options=["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"])
    tdee = calculate_tdee(bmr, activity_level)

    # Dietary goals selection
    st.sidebar.subheader("Select your dietary goals:")
    weight_loss = st.sidebar.checkbox("Weight loss")
    weight_gain = st.sidebar.checkbox("Weight gain")
    maintenance = st.sidebar.checkbox("Maintenance")
    fitness = st.sidebar.checkbox("Fitness")
    rapid_weight_loss = st.sidebar.checkbox("Rapid Weight Loss")
    
    goals = []
    if weight_loss:
        goals.append("Weight loss")
    if weight_gain:
        goals.append("Weight gain")
    if maintenance:
        goals.append("Maintenance")
    if fitness:
        goals.append("Fitness")
    if rapid_weight_loss:
        goals.append("Rapid Weight Loss")

    # Calculate calorie intake
    calorie_intake = calculate_calorie_intake(tdee, goals, weight, ideal_weight)

    # Submit button
if st.button("Submit"):
    st.subheader("Calculated Metrics:")
    # BMI
    if bmi < 18.5:
        bmi_indication = "Underweight"
        bmi_color = "warning"
    elif 18.5 <= bmi < 25:
        bmi_indication = "Normal weight"
        bmi_color = "success"
    elif 25 <= bmi < 30:
        bmi_indication = "Overweight"
        bmi_color = "info"
    else:
        bmi_indication = "Obese"
        bmi_color = "error"
    st.write(f"BMI: {bmi:.2f} ({bmi_indication})", unsafe_allow_html=True)
    st.info("BMI is a measure of body fat based on height and weight.")

    # BMR
    # There are no standard indications for BMR as it is a measure of the body's basal metabolic rate.
    st.write(f"BMR: {bmr:.2f} kcal/day", unsafe_allow_html=True)
    st.info("Basal Metabolic Rate is the amount of energy expended while at rest in a neutrally temperate environment.")

    # TDEE
    # You can provide interpretations based on the activity level chosen by the user.
    # For example, Sedentary, Lightly active, Moderately active, Very active, Extra active.
    st.write(f"TDEE: {tdee:.2f} kcal/day", unsafe_allow_html=True)
    st.info("Total Daily Energy Expenditure is the total number of calories burned each day.")

    # Body Fat Mass
    # There are no standard indications for body fat mass. It's typically interpreted in the context of overall body composition goals.
    st.write(f"Body Fat Mass: {body_fat_mass:.2f} kg", unsafe_allow_html=True)
    st.info("Body Fat Mass is the amount of fat tissue in the body.")

    # Total Body Water (TBW)
    # There are no standard indications for total body water. It's generally interpreted based on hydration status and health conditions.
    st.write(f"Total Body Water (TBW): {tbw:.2f} liters", unsafe_allow_html=True)
    st.info("Total Body Water is the total amount of water present in the body.")