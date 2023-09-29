import streamlit as st
import pandas as pd

transform_data <- function(input_data) {
  melted_data <- input_data %>% 
    gather(key = "Response Option", value = "Selected", -profile_id)  # Adjust "-profile_id" if your column has a different name
  
  melted_data$Selected <- tolower(as.character(melted_data$Selected)) %>% 
    recode(`1` = "Selected",
           `0` = "Not selected",
           "yes" = "Selected",
           "no" = "Not selected",
           "selected" = "Selected",
           "not selected" = "Not selected",
           .default = "Not selected")  # Default value for NA or empty strings

  return(melted_data)
}
    
    melted_data['Selected'] = melted_data['Selected'].astype(str).map(value_mapping).fillna("Not selected")
    
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
