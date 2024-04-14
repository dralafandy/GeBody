def main():
    st.title('GeBody - Body Composition Analyzer')

    name = st.text_input('Enter patient name:')
    age = st.number_input('Enter age:', min_value=0, max_value=150, value=30)
    sex = st.radio('Select sex:', ('Male', 'Female'))
    weight = st.number_input('Enter weight (kg):', min_value=0.0, value=70.0)
    height = st.number_input('Enter height (cm):', min_value=0.0, value=170.0)
    waist_hip_ratio = st.number_input('Enter waist/hip ratio:', min_value=0.0, value=0.9)
    body_fat_percentage = st.number_input('Enter body fat percentage:', min_value=0.0, max_value=100.0, value=20.0)
    goal_weight = st.number_input(f'Enter goal weight (kg):', min_value=0.0, value=70.0)

    # Determine goal action based on goal weight and current weight
    if goal_weight > weight:
        action = "Gain weight"
    elif goal_weight < weight:
        action = "Lose weight"
    else:
        action = "Maintain weight"

    rate_of_change = st.number_input('Enter desired weekly rate of weight change (in kg/week):', min_value=-1.0, max_value=1.0, value=0.5)
    
    activity_options = ['Sedentary', 'Lightly active', 'Moderately active', 'Very active']
    activity = st.selectbox('Select activity level:', activity_options)

    # Automatically determine the goal action based on the selected action
    if action == "Gain weight":
        goal_action = "Gain weight"
    elif action == "Lose weight":
        goal_action = "Lose weight"
    else:
        goal_action = "Maintain weight"

    # Calculate calorie intake based on the goal action
    min_calorie_intake, max_calorie_intake = calculate_calorie_intake(weight, height, age, sex, activity, goal_weight, rate_of_change)


    action = st.selectbox('Choose an action:', ['Calculate', 'Show Data'])

    if action == "Calculate":
        if st.button('Calculate'):
            # Perform calculations
            bmi = calculate_bmi(weight, height / 100)  # Convert height to meters
            ideal_weight = calculate_ideal_weight(height, sex)
            weight_status, weight_difference = calculate_weight_difference(weight, ideal_weight)
            bmr = calculate_bmr(weight, height, age, sex)
            lean_body_mass = calculate_lean_body_mass(weight, body_fat_percentage)
            body_fat_mass = calculate_body_fat_mass(weight, body_fat_percentage)
            waist_to_hip_ratio = calculate_waist_to_hip_ratio(waist_hip_ratio)
            muscle_mass = calculate_muscle_mass(weight, body_fat_percentage)
            visceral_fat_level = calculate_visceral_fat_level(waist_to_hip_ratio, sex)
            body_water_percentage = calculate_body_water_percentage(weight, body_fat_percentage, sex)
            bone_mineral_content = calculate_bone_mineral_content(weight)
            rmr = calculate_rmr(weight, height, age, sex)
            total_body_water = calculate_total_body_water(weight, height, age, sex)

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
                'Total Body Water': total_body_water,
                'Min Calorie Intake': min_calorie_intake,
                'Max Calorie Intake': max_calorie_intake,
                'Dietary Recommendations': []  # Placeholder for dietary recommendations
            }

            # Generate recommendations based on other parameters
            if body_fat_percentage:
                if body_fat_percentage < 10:
                    body_composition_results['Dietary Recommendations'].append("Your body fat percentage is extremely low. It's important to maintain a healthy level of body fat to support bodily functions. Consider consulting a healthcare professional for personalized advice.")
                elif body_fat_percentage > 30:
                    body_composition_results['Dietary Recommendations'].append("Your body fat percentage is higher than normal. Consider incorporating more physical activity and dietary changes to reduce body fat levels.")
                else:
                    body_composition_results['Dietary Recommendations'].append("Your body fat percentage falls within the normal range. Keep up the good work with your diet and exercise routine.")

            if waist_hip_ratio:
                if sex == 'Male':
                    if waist_hip_ratio > 0.9:
                        body_composition_results['Dietary Recommendations'].append("Your waist-to-hip ratio indicates higher abdominal fat. Consider incorporating more cardiovascular exercises and reducing calorie intake to target abdominal fat.")
                    else:
                        body_composition_results['Dietary Recommendations'].append("Your waist-to-hip ratio falls within the normal range. Keep up the good work with your fitness routine.")
                else:
                    if waist_hip_ratio > 0.85:
                        body_composition_results['Dietary Recommendations'].append("Your waist-to-hip ratio indicates higher abdominal fat. Consider incorporating more cardiovascular exercises and reducing calorie intake to target abdominal fat.")
                    else:
                        body_composition_results['Dietary Recommendations'].append("Your waist-to-hip ratio falls within the normal range. Keep up the good work with your fitness routine.")

            # Displaying results in a collapsible box
            with st.expander("Results", expanded=True):
                for result, value in body_composition_results.items():
                    unit = ""
                    if result in ["BMI", "Lean Body Mass", "Body Fat Mass", "Muscle Mass", "Bone Mineral Content", "Ideal Weight", "Weight Difference", "Total Body Water", "Min Calorie Intake", "Max Calorie Intake"]:
                        unit = "kg"
                    elif result in ["BMR", "RMR"]:
                        unit = "kcal/day"
                    elif result == "Body Water Percentage":
                        unit = "%"
                    elif result == "Waist-to-Hip Ratio":
                        unit = ""
                    elif result == "Dietary Recommendations":
                        continue  # Skip displaying dietary recommendations here
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
                        st.progress(progress_value)
                        st.markdown("---")

            # Display dietary recommendations separately
            st.write('## Dietary Recommendations')
            for recommendation in body_composition_results['Dietary Recommendations']:
                st.write(recommendation)
            # Display calorie intake for weight management
            st.write('### Calorie Intake for Weight Management')
            st.markdown(f'Minimum Calorie Intake: {min_calorie_intake} kcal/day')
            st.markdown(f'Maximum Calorie Intake: {max_calorie_intake} kcal/day')

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
