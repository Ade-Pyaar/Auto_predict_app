from pkg_resources import VersionConflict
import streamlit as st
from utils import get_suggestions



st.sidebar.subheader('About the App')
st.sidebar.write('Auto-predict App with Streamlit using N-grams')
st.sidebar.write("The app tries to predict the next word of an incomplete sentence based on the previous words in the sentence.")
st.sidebar.write("The model is not perfect...")



#start the user interface
st.title("Auto-predict App")
st.write("Type in your incomplete sentence below and click/press the 'Predict' button to get the next possible words")

my_text = st.text_input("Enter the incomplete sentence", "", max_chars=100, key='to_classify')
verbose = st.checkbox("Do you want verbose output?", value=False, key="verbose")

if st.button('Predict', key='classify_button'):
    suggestion = get_suggestions(my_text)
    
    for item in suggestion.keys():
        if verbose:
            st.write(f"{my_text}: {item}\t\tProbability: {suggestion[item]}")
        else:
            st.write(f"{my_text}: {item}")
