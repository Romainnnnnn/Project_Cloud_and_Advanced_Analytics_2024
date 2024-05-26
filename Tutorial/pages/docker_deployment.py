import streamlit as st

st.title("Deployment with Docker and Google Cloud")

st.markdown("""
Below are instruction to deploy the Streamlit app and the backend using Docker:
            
1. Go on the google cloud console and run the following commands:
""")
code1 = """
git clone https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024
cd Project_Cloud_and_Advanced_Analytics_2024
cd backend
docker build -t eu.gcr.io/YOUR_PROJECT_ID/backend:latest .
docker push eu.gcr.io/YOUR_PROJECT_ID/backend:latest
"""



st.code(code1, language='python')

st.markdown("""            
2. You can now go to the Google Cloud Services and deploy the backend using the image you just pushed.
3. Once the backend is deployed, you can copy the URL of the backend and paste it in the Streamlit app and in the m5 stack code.
4. You can now deploy the Streamlit app using the following commands in the google cloud console:
""")

code2 = """ 
cd
cd Project_Cloud_and_Advanced_Analytics_2024
cd UI
docker build -t eu.gcr.io/YOUR_PROJECT_ID/home:latest .
docker push eu.gcr.io/YOUR_PROJECT_ID/home:latest
"""
st.code(code2, language='python')

st.markdown("""
5. You can now go to the Google Cloud Services and deploy the Streamlit app using the image you just pushed.     
""")

if st.button('Next Page'):
    st.switch_page('pages/uiflow.py')