import streamlit as st
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from prompt import get_interview_system_prompt
from prompt import get_validation_prompt
from prompt import get_report_prompt
from gtts import gTTS
from ui import render_css, render_header, render_question

load_dotenv()
client=OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def speech_to_text(audio):
    transcript=client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )
    return transcript.text

def speak_text(text):
    tts=gTTS(text)
    tts.save("question.mp3")
    audio_file=open("question.mp3","rb")
    st.audio(audio_file,autoplay=True)

def generate_report():
    report_prompt=get_report_prompt()
    validation=client.chat.completions.create(
        model="gpt-5.4-mini",
        max_completion_tokens=300,
        messages=st.session_state.conversation_history+[{"role":"user","content":report_prompt}]
    )
    validation=validation.choices[0].message.content
    return validation

def validate_input(job_role,experience):
    validation_prompt=get_validation_prompt(job_role,experience)
    validation=client.chat.completions.create(
        model="gpt-5.4-mini",
        max_completion_tokens=10,
        messages=[{"role":"user","content":validation_prompt}]
    )
    validation_text=validation.choices[0].message.content
    if "VALID" in validation_text and "INVALID" not in validation_text:
        return True
    else:
        return False


def get_ai_response(user_message,system_prompt):
    st.session_state.conversation_history.append(
        {"role":"user","content": user_message}
    )
    response=client.chat.completions.create(
        model="gpt-5.4-mini",
        max_completion_tokens=300,
        messages=[{"role":"system","content":system_prompt}]+st.session_state.conversation_history
    )
    ai_text=response.choices[0].message.content
    st.session_state.conversation_history.append(
        {"role":"assistant","content":ai_text}
    )
    return ai_text
    

st.title("AI INTERVIEW")
render_css() 
# start hone se pahale 
if "job_role" not in st.session_state:
    st.session_state.job_role=""
if "experience" not in st.session_state:
    st.session_state.experience=""
if "interview_started" not in st.session_state:
    st.session_state.interview_started=False
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history=[]
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt=""
if "first_question_asked" not in st.session_state:
    st.session_state.first_question_asked=False
if "current_question" not in st.session_state:
    st.session_state.current_question=""
if "interview_ended" not in st.session_state:
    st.session_state.interview_ended=False
if "speak_question" not in st.session_state:
    st.session_state.speak_question=False

#stage 1 when it's not start
if not st.session_state.interview_started:
    st.session_state.job_role=st.text_input("enter the job role")
    st.session_state.experience=st.text_input("enter the experience")
    if st.button("submit"):
        if st.session_state.job_role=="":
            st.write("enter the job role")
        if st.session_state.experience=="":
            st.write("enter the experience")
        if st.session_state.job_role and st.session_state.experience:
            is_valid=validate_input(st.session_state.job_role, st.session_state.experience)
            if is_valid:
                st.session_state.system_prompt=get_interview_system_prompt(
                st.session_state.job_role,
                st.session_state.experience
                )
                st.session_state.interview_started=True
                st.rerun()    
            else:
                st.write("Invalid job role or experience!")
#stage 2 when it's  start
elif st.session_state.interview_started and not st.session_state.interview_ended:
   render_header()
   if not st.session_state.first_question_asked:
       ai_question=get_ai_response("Start the interview and ask me the first question.",st.session_state.system_prompt)
       st.session_state.current_question=ai_question
       st.session_state.first_question_asked=True
       st.session_state.speak_question=True
    
   render_question(st.session_state.current_question)
   if st.session_state.speak_question: 
        speak_text(st.session_state.current_question)
        st.session_state.speak_question=False

   audio=st.audio_input("speak your answer",
                        key=f"audio_{len(st.session_state.conversation_history)}"
                        )
   if audio and not st.session_state.get("processing", False):
       st.session_state.processing=True
       user_answer=speech_to_text(audio)
       ai_question=get_ai_response(user_answer,st.session_state.system_prompt)
       st.session_state.current_question=ai_question
       st.session_state.speak_question=True
       st.session_state.processing=False
       st.rerun()
   if st.button("Interview end"):
       st.session_state.interview_ended=True
       st.rerun()
elif st.session_state.interview_ended:
    st.write("Interview has been ended")

    report=generate_report()
    st.write(report)