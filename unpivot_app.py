import streamlit as st
import pandas as pd

def transform_data(input_df):
    melted_data = pd.melt(input_df, id_vars=["respondent_id"], 
                          value_vars=input_df.columns[1:],
                          var_name="Response Option",
                          value_name="Selected")
    return melted_data

st.title('Unpivot Multi-Select Survey Data')

st.write("This web app will help you convert multi-select question data into a pivotal format.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    transformed_data = transform_data(input_df)
    
    st.write("Transformed Data:")
    st.write(transformed_data)
    
    st.download_button(label="Download Transformed Data", data=transformed_data.to_csv(index=False), file_name='transformed_data.csv', mime='text/csv')
