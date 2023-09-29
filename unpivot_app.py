import streamlit as st
import pandas as pd

def transform_data(input_df):
    # Unpivot the data
    melted_data = pd.melt(input_df, id_vars=["response_id"], 
                          value_vars=input_df.columns[1:],
                          var_name="Response Option",
                          value_name="Selected")
    
    # Convert to lowercase for case-insensitive matching
    melted_data['Selected'] = melted_data['Selected'].astype(str).str.lower()

    # Map the values
    value_mapping = {
        "yes": "Selected",
        "1": "Selected",
        "selected": "Selected",
        "true": "Selected",
        "no": "Not selected",
        "0": "Not selected",
        "not selected": "Not selected",
        "false": "Not selected",
        "": "Not selected",  # for blank strings
        "nan": "Not selected"  # for NaN values
    }
    
    melted_data['Selected'] = melted_data['Selected'].map(value_mapping).fillna("Not selected")
    
    return melted_data


st.title('Unpivot Multi-Select Survey Data')

st.write('This is a simple web app that can help you convert multi-select data from a survey into into a format that you can pivot. In other words, it will help you unpivot your data.')
st.write('For example, say you have a survey question that looks like this:')
st.write('**Which of the following terms, if any, would you use to describe <brand name>? Choose all that apply.**')
st.markdown('- Affordable')
st.markdown('- Durable')
st.markdown('- High quality')
st.markdown('- Stylish')
st.markdown('- None of the above')

st.write('A raw data export for a question like this would typically look like this:')

st.write(pd.DataFrame({
    'response_id': [1, 2, 3, 4, 5],
    'q1r1 Affordable': [1, 1, 1, 0, 0],
    'q1r2 Durable': [0, 1, 1, 0, 0],
    'q1r3 High quality': [0, 0, 0, 1, 0],
    'q1r4 Stylish': [1, 0, 1, 0, 0],
    'q1r5 None of the above': [0, 0, 0, 0, 1],
}))

st.write('Unfortunately, this format can not easily be pivoted in Excel, so this script will convert it to a multi-row, single-column format that looks like this:')
st.write(pd.DataFrame({
    'response_id': [1, 2, 3, 4, 5],
    'Response Option': ["Affordable", "Affordable", "Affordable", "Affordable", "Affordable"],
    'Selected': ["Selected", "Selected", "Selected", "Not selected", "Not selected"],
}))

st.write('For more information on how to prepare your file check out the link below')
url = "https://analythical.com/blog/unpivot-multi-select-data-tool"
st.write("[Read the walkthrough for how to prepare your data](%s)" % url)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    transformed_data = transform_data(input_df)
    
    st.write("Transformed Data:")
    st.write(transformed_data)
    
    st.download_button(label="Download Transformed Data", data=transformed_data.to_csv(index=False), file_name='transformed_data.csv', mime='text/csv')
