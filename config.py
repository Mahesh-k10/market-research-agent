import os
import streamlit as st
from openai import OpenAI

api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama3-70b-8192"