from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.callbacks import get_openai_callback
import os
from dotenv import load_dotenv
from src.mcqGenerator.logger import logging
from src.mcqGenerator import utils


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

template = """
Text: {text}
You are an expert MCQ maker, Given the above text, it is your job to create a quiz
of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and all the questions are confirming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs.
###RESPONSE_JSON
{response_json}
"""

quiz_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template,
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt, output_key="quiz", verbose=True)

eval_template = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students, you need to 
evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
If the quiz is not at par with the cognitive and analytical abilities of the students, update the quiz questions  
which needs to be changed and change the tone such that it perfectly fits the student abilities.
Quiz_MCQs:
{quiz}

Analysis from an expert English Writer of the above quiz:
"""

eval_prompt = PromptTemplate(
    input_variables=["quiz", "subject"], template=eval_template
)

eval_chain = LLMChain(llm=llm, prompt=eval_prompt, output_key="review", verbose=True)

chain = SequentialChain(
    chains=[quiz_chain, eval_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True,
)
