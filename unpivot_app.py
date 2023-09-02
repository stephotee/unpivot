import streamlit as st
import pandas as pd

def transform_data(input_df):
    # Unpivot the data
    melted_data = pd.melt(input_df, id_vars=["response_id"], 
                          value_vars=input_df.columns[1:],
                          var_name="Response Option",
                          value_name="Selected")
    
    # Map the values
    value_mapping = {
        "Yes": "Selected",
        "1": "Selected",
        "Selected": "Selected",
        "True": "Selected",
        "No": "Not selected",
        "0": "Not selected",
        "Not selected": "Not selected",
        "False": "Not selected",
        "": "Not selected",  # for blank strings
        None: "Not selected"  # for NaN values
    }
    
    melted_data['Selected'] = melted_data['Selected'].astype(str).map(value_mapping).fillna("Not selected")
    
    return melted_data

st.title('Unpivot Multi-Select Survey Data')

st.write('This is a simple web app that can help you convert multi-select data from a survey into into a format that you can pivot. In other words, it will help you unpivot your data.')

st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    transformed_data = transform_data(input_df)
    
    st.write("Transformed Data:")
    st.write(transformed_data)
    
    st.download_button(label="Download Transformed Data", data=transformed_data.to_csv(index=False), file_name='transformed_data.csv', mime='text/csv')
