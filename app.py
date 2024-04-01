import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqGenerator.utils import readFile, formatData
from src.mcqGenerator.mcqgenerator import chain
from src.mcqGenerator.logger import logging

with open("response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator")

with st.form("User Input"):
    uploadedFile = st.file_uploader("Upload data file (pdf or txt)")

    mcq_count = st.number_input(
        "Number of MCQs", min_value=3, max_value=50, placeholder=5
    )

    subject = st.text_input("what is the Subject?", max_chars=20)
    tone = st.text_input(
        "what is the complexity of the questions?", max_chars=20, placeholder="Simple"
    )

    button = st.form_submit_button("Generate MCQs")

    if button and uploadedFile is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = readFile(uploadedFile)

                with get_openai_callback() as cb:
                    response = chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON),
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        df = formatData(quiz)
                        df.index = df.index + 1
                        st.table(df)
                        st.text_area(label="Review", value=response["review"])
                    else:
                        st.error("Error in the quiz format")

                else:
                    st.write(response)