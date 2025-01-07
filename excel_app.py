import os 
import dotenv  
from dotenv import load_dotenv
import streamlit as st 
from langchain_openai import ChatOpenAI  
from langchain_groq import ChatGroq 
import pandasai
from pandasai import SmartDataframe  
import pandas as pd 
from pandasai.responses.streamlit_response import StreamlitResponse  
import seaborn as sns 
import sklearn  
import glob 
import random  
import tensorflow
import tensorflow.keras.models

pwd= os.getcwd()
load_dotenv('api.env') 
os.environ["OPENAI_API_KEY"]= os.getenv("OPENAI_API_KEY")
groq_api_key= os.getenv("GROQ_API_KEY")     
os.environ['PANDASAI_API_KEY'] = "$2a$10$bkTOL4aI1gpOGYtLOkhJ.e9CWd9zL7ckGXiFkXnU.wJtsV9NzkyUa" 

st.set_page_config(page_title="Excel ChatBot") 
st.title("Excel Interpreter") 
st.subheader("An Excel Based Interpretation Assistant")  

with st.settings: 
    openai_api_key= st.text_input("Enter your OpenAI API Key:", type="password") 
    pandas_api_key= st.text_input("Enter your Pandas API Key:", type="password")  


if openai_api_key: 
    llm= ChatOpenAI(openai_api_key= openai_api_key, model_name="gpt-4o")

if pandas_api_key:
    file= st.file_uploader("Upload your file", type=["xlsx"])
    if file:  
        df= pd.read_excel(file) 
        sdf= SmartDataframe( 
            df=df, 
            config={
                "llm":llm, 
                "response_parser":StreamlitResponse, 
                "save_charts":True, 
                "save_charts_path":pwd, 
                "custom_whitelisted_dependencies": ["sklearn","random","tensorflow","langchain","huggingface","itertools"]
            }
        )   
        options= ["Chat","Plot"]
        task= st.selectbox("What task do you wish to perform",options) 
        query= st.text_area("Ask me anything", height=100)   
        button= st.button("Submit")
        
        if button and query!="" and task:    
            if task=="Chat":
                response= sdf.chat(query)  
                st.write(response)  
            elif task=="Plot":  
                file= glob.glob(pwd + "/*.png")   
                if file: 
                    os.remove(file[0])
                response= sdf.chat(query) 
                file= glob.glob(pwd + "/*.png")  
                st.image(file[0]) 





        



