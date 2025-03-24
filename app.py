import streamlit as st
from ai_recruiment_sys.resume_parser import skills, document_loader, summarizer, fit_or_not, name_from_resume
from ai_recruiment_sys.email_generator import success_email,apology_email
from ai_data_analyzer.data_fetch import read_data, lst_to_strng, data_for_duckdb, output_makeup
from ai_data_analyzer.text_generator import sql_query_chain, final_answer_chain
import duckdb as db
import pandas as pd

# streamlit page configuration
st.set_page_config(
  page_title="HR Insights Pro",
  page_icon="💭",
  layout="centered"
)

def main():
  
  # Sidebar content
  with st.sidebar:
    option = st.selectbox("HR Insights Pro",("Recruiment System", "Data Analyzer"))


  if option == "Recruiment System":
    st.title("AI Recruitment System")
    with st.sidebar:
      st.title("Credential Settings")
      email = st.text_input("Enter the Email", "")
      password = st.text_input("Enter the password", "",type = 'password')
      gmeet_link = st.text_input("Enter Google meet link", "")
      
      st.title('Personal Information')
      hr_name = st.text_input("Enter your Name", "")
      company_name = st.text_input("  Company name", "")
      
      st.title('Candidate Information')
      c_mail = st.text_input("Enter candidate's Email","")
    
    
      
    global decision
    # main content
    job_role = st.selectbox(
      "Select the job role:",
        ['AI/ML Engineer','FrontEnd Developer','BackEnd Developer'])
      
    if job_role == 'AI/ML Engineer':
      skill = skills[0]
      st.write(skills[0])
    elif job_role == 'FrontEnd Developer':
      skill = skills[1]
      st.write(skills[1])
    else:
      skill = skills[2]
      st.write(skills[2])
      
    uploaded_file = st.file_uploader("Upload the Resume:", type=["pdf"])
    if st.button('Analyze'):
      if uploaded_file is not None:
        content = document_loader(uploaded_file)
        summary = summarizer(content)
        name = name_from_resume(content=content)
        st.write(summary)
        decision = fit_or_not(content=content,skill=skill,job_role=job_role)
        
        if decision == 'Yes':
          st.success('Congratulations, This candidate is Shortlisted.')
          with st.spinner("Sending the mail to the Candidate..."):
            status = success_email(name=name,job_role=job_role,company_name=company_name,gmeet_link=gmeet_link,content=content,sender_email=email,reciever_email=c_mail,sender_name=hr_name,password=password)
            if status == 'Success':
              st.success('Email sent to the Candidate successfully.')
            else:
              st.success("Due to some error, Email sending is not successful.")
        if decision == 'No':
          st.success('Unfortunately, This candidate is not Shortlisted.')
          with st.spinner("Sending the mail to the Candidate..."):
            status = apology_email(job_role=job_role,company_name=company_name,sender_email=email,reciever_email=c_mail,sender_name=hr_name,password=password,name=name)
            if status == 'Success':
              st.success('Email sent to the Candidate successfully.')
            else:
              st.success("Due to some error, Email sending is not successful.")
  else:
    st.title('AI Data Analyzer')

    if "chat_history" not in st.session_state:
      st.session_state.chat_history = []
      
    if "df" not in st.session_state:
      st.session_state.df = None

    uploaded_file = st.file_uploader("Upload your file:",type=['csv','xlsx','xls'])

    if uploaded_file:
      st.session_state.df = read_data(uploaded_file)
      
      column_list, column_names = lst_to_strng(st.session_state.df)
      
      temp_file_duckdb = data_for_duckdb(column_list=column_list,df=st.session_state.df)
      
      DATA_BASE = db.read_csv(temp_file_duckdb)
      db_name = "DATA_BASE"
      
      st.write("Data Preview")
      agree = st.checkbox("Show the Whole Data")
      if agree:
        st.dataframe(st.session_state.df)
      else:
        st.dataframe(st.session_state.df.head())
        
    for message in st.session_state.chat_history:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
    user_question = st.chat_input("Ask anything about the Data")

    if user_question:
      st.chat_message("User").markdown(user_question)
      st.session_state.chat_history.append({"role":"User","content":user_question})
      
      sql_chain = sql_query_chain()
      
      result = sql_chain.invoke({"columns":column_names,"db":db_name,"user_question":user_question})
      
      op_strng = output_makeup(result)
      print(op_strng)
      ans = db.sql(op_strng).to_df()
      ans_dict = ans.to_dict(orient='list')
      
      ans_chain = final_answer_chain()
      
      final_result = ans_chain.invoke({"user_question":user_question,"answer":ans_dict})
      
      
      st.session_state.chat_history.append({"role":"assistant","content":(final_result)})
      
      with st.chat_message("assistant"):
        st.markdown(final_result)
        st.text("Use the query to fetch the data from your DataBase:")
        st.code(op_strng, language="sql",line_numbers=False, wrap_lines=True)
          
if __name__ == "__main__":
  main()
  
  
  
  
  
  
  






  
