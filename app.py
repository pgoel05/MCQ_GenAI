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

