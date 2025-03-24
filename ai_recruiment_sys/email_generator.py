import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ai_recruiment_sys.resume_parser import llm


def extract_email_parts(email_text):
    # Regular expression to match the subject line
    subject_match = re.search(r"Subject:\s*(.+)", email_text)

    if subject_match:
        subject = subject_match.group(1).strip()
        
        # Splitting the email text into lines and finding the body starting point
        body_start_index = email_text.index("Dear")  # Finding the start of the body by the word "Dear"
        body = email_text[body_start_index:].strip()

        return [subject, body]
    else:
        return ["Subject not found", "Body not found"]

def mail_sender(sender_email,receiver_email,subject,body,password):
  # Create the email
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject
  msg.attach(MIMEText(body, 'plain'))

  # Send the email
  try:
      with smtplib.SMTP('smtp.gmail.com', 587) as server:
          server.starttls()
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, msg.as_string())
          return "Success"
  except Exception as e:
      return "Email sending unsuccessful"

def success_email(name,job_role,company_name,gmeet_link,content,sender_email,reciever_email,sender_name,password):
  prompt = f"""Write a email to {name} whose resume is best fit for the role {job_role}.The sender's organization name: {company_name}. send the person the google meet link: {gmeet_link} to join for the personal interview process.
  The content of the resume: {content}. make it simple, professional and to the point. tell if you have any query, reach out on the email: {sender_email}. sender name is: {sender_name} and no need to mention date and time in the email.
  Don't write any fancy things at the beginning of your answer, strictly start with the email subject. """
  
  email = llm.invoke(prompt)
  email = email.content

  unwanted_symbols = "*&$%"
  pattern = f"[{re.escape(unwanted_symbols)}]"

  # Clean each string in the list
  cleaned_strings = re.sub(pattern,"", email)
  list_of_element = extract_email_parts(cleaned_strings)
  
  status = mail_sender(sender_email=sender_email,receiver_email=reciever_email,subject=list_of_element[0],body=list_of_element[1],password=password)
  return status
  

def apology_email(job_role,company_name,sender_email,reciever_email,sender_name,password,name):
  prompt = f"""Write a professional and empathetic apology email to inform a candidate that they have not been shortlisted for the {job_role} position at {company_name}. The email should express gratitude for the candidate's application, provide a brief reason for not proceeding, offer encouragement for future applications, and wish the candidate success in their career.
  Don't write any fancy things at the beginning of your answer, strictly start with the email subject. Sender name is: {sender_name}, reciever name is: {name} and no need to mention date and time in the email."""
  
  email = llm.invoke(prompt)
  email = email.content

  unwanted_symbols = "*&$%"
  pattern = f"[{re.escape(unwanted_symbols)}]"

  # Clean each string in the list
  cleaned_strings = re.sub(pattern,"", email)
  list_of_element = extract_email_parts(cleaned_strings)
  
  status = mail_sender(sender_email=sender_email,receiver_email=reciever_email,subject=list_of_element[0],body=list_of_element[1],password=password)
  return status

