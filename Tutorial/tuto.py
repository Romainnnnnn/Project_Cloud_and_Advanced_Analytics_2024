import streamlit as st
import os

# Function to save inputs to .env file
def save_to_env(var_names, var_values):
    with open('.env', 'w') as f:
        for name, value in zip(var_names, var_values):
            f.write(f"{name}={value}\n")

# Streamlit app layout
def main():
    st.title('Environment Variables Setup')

    # Create five text input boxes
    var_names = ['API_KEY', 'PROJECT_NAME', 'KEY_PASS', 'LOCATION', 'VAR5']
    var_values = []
    for var in var_names:
        var_value = st.text_input(f"Enter value for {var}", key=var)
        var_values.append(var_value)

    # Save button
    if st.button('Save to .env'):
        save_to_env(var_names, var_values)
        st.success('Environment variables saved successfully! COPY .env FILE TO MIDDLEWARE FOLDER')

if __name__ == "__main__":
    main()
