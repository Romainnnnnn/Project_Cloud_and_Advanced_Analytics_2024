import streamlit as st



st.title('M5 Stack Setup')
st.write("##### Copy paste the code in the m5stack folder to the M5 Stack IDE")
st.write('##### Change the M5 Stack wifi settings and add your local or deployed backend URL')
image = st.image('data/setup.png', caption='https://flow.m5stack.com/', width=500)

st.write('##### Connect your sensors')
image = st.image('data/sensors.png', caption='https://flow.m5stack.com/', width=500)
st.write('###### ENV III : port red : 32/33')
st.write('###### TVOC : port blue : 14/13')
st.write('###### PIR : port black : 36/26')

st.write('##### Download the firmware onto the M5 Stack')

st.write('###### Click on the download button and wait for the firmware to be downloaded')
image = st.image('data/dl.png', caption='https://flow.m5stack.com/', width=500)

if st.button('Next Page'):
    st.switch_page('tuto.py')
