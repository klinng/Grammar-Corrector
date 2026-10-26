import streamlit as st


@st.cache_resource
def get_model():
    from corrector.pipeline import load_model

    return load_model()


st.title("Grammar Corrector")
mode = st.radio(
    "Mode",
    ["Light (T5, on this PC)", "Smart: fix (Ollama)", "Smart: rewrite (Ollama)"],
)
text = st.text_area("Your text", height=200)

if st.button("Correct") and text.strip():
    try:
        with st.spinner("Correcting..."):
            if mode.startswith("Light"):
                from corrector.pipeline import correct_text

                tokenizer, model = get_model()
                result = correct_text(text, tokenizer, model)
            else:
                from corrector.smart import smart_correct

                result = smart_correct(text, "fix" if "fix" in mode else "rewrite")
    except (RuntimeError, FileNotFoundError) as err:
        st.error(str(err))
    else:
        st.subheader("Result")
        st.write(result)
        st.code(result, language=None)