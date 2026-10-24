import streamlit as st

from corrector.pipeline import correct_text, load_model


@st.cache_resource
def get_model():
    return load_model()


st.title("Grammar Corrector")
text = st.text_area("Your text", height=200)

if st.button("Correct") and text.strip():
    tokenizer, model = get_model()
    with st.spinner("Correcting..."):
        result = correct_text(text, tokenizer, model)
    st.subheader("Result")
    st.write(result)
    st.code(result, language=None)