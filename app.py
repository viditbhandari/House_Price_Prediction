import pandas as pd
import pickle as pk
import streamlit as st

model = pk.load(open('House_prediction_model.pkl','rb'))

st.header('Banglore House Price Predictor')

st.divider()

data = pd.read_csv('Cleaned_data.csv')

loc = st.selectbox('Choose the loaction',data['location'].unique())

sqft = st.number_input('Enter Total Sqft')

beds = st.number_input("Enter No. of Bedrooms")
bath = st.number_input("Enter No. of bathrooms")
balc = st.number_input("Enter No. of Balconies")
st.divider()

input = pd.DataFrame([[loc,sqft,beds,bath,balc]],columns=['location','total_sqft','bath','balcony','bedroom'])

if st.button("Predict Price"):
    st.balloons()
    output = model.predict(input)
    st.write(f"The predicted house price is : Rs {output[0]*100000:,.2f}")

    
