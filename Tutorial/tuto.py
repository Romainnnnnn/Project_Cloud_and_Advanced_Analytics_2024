import streamlit as st
import os

# Function to save inputs to .env file
def save_to_env(var_names, var_values):
    with open('.env', 'w') as f:
        for name, value in zip(var_names, var_values):
            f.write(f"{name}={value}\n")

# Streamlit app layout
def main():
    st.title('Backend Environement Setup')

    st.write("##### API Key")
    st.write("Please enter your OpenWeatherMap API key. This is required for authentication with external services.")
    st.write("You can get an API key by signing up [here](https://home.openweathermap.org/users/sign_up)")
    api_key = st.text_input("Enter API Key", key='API_KEY')

    st.write("##### Project Name")
    st.write("The project name of your Google Cloud project. This is required for authentication with Google Cloud services.")
    project_name = st.text_input("Enter Project Name", key='PROJECT_NAME')

    st.write("##### Key Path")
    st.write("This key is your Google Cloud service account key. This is required for authentication with Google Cloud services")
    key_path = st.text_input("Enter Key Path", key='KEY_PATH')

    st.write("##### Location Setting (format: Lausanne,CH)")
    st.write("Please specify the deployment location. This will help configure regional settings.")
    location = st.text_input("Enter Location", key='LOCATION')

    st.write("##### Variable 5")
    st.write("Additional configuration settings can be specified here.")
    var5 = st.text_input("Enter Variable 5", key='VAR5')

    var_names = ['API_KEY', 'PROJECT_NAME', 'KEY_PATH', 'LOCATION', 'VAR5']
    var_values = [api_key, project_name, key_path, location, var5]

    # Save button
    if st.button('Save to .env'):
        save_to_env(var_names, var_values)
        st.success('Environment variables saved successfully!')
        st.write('##### Copy the .env file to the backend folder to use the updated configuration.')

    if st.button('Next Page'):
        st.switch_page('pages/uiflow.py')

if __name__ == "__main__":
    main()
