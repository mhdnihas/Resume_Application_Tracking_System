from dotenv import load_dotenv

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai


from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
