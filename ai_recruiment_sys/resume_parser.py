import os
import re
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_nvidia_ai_endpoints import ChatNVIDIA

os.environ['NVIDIA_API_KEY'] = "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"

llm = ChatNVIDIA(model="meta/llama3-70b-instruct")

skills = ["""Required Skills:
- Python, PyTorch/Tensorflow
- Machine Learning algorithms and frameworks
- Deep learning and Neural Networks
- Data preprocessing and analysis
- MLOps and Model Deployment
- RAG, LLM, Finetuning and Prompt Engineering""",
          """Required Skills:
- React/Vue.js/Angular
- HTML5, CSS3, JavaScript/TypeScript
- Responsive Design
- State Management
- Frontend testing""",
          """Required Skills:
- Python/Java/Node.js
- REST APIs
- Database design and management
- System architecture
- Cloud services (AWS/GCP/Azure)
- Kubernetes, Docker, CI/CD"""]

# Document loader and text extraction
def document_loader(filepath):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
    temp_file.write(filepath.read())  # Write the contents of the uploaded file
    temp_path = temp_file.name  
    
  loader = PyPDFLoader(temp_path)
  text = loader.load()
  content = text[0].page_content
  
  return content

def summarizer(text):
  prompt_for_summary = f"""This is the resume content: {text}. Give a summery of this resume, mention name, number(if available), email(if available), skills(structured way) and projects."""
  
  result = llm.invoke(prompt_for_summary)
  result = result.content

  unwanted_symbols = "*&$%"
  pattern = f"[{re.escape(unwanted_symbols)}]"

  # Clean each string in the list
  cleaned_strings = re.sub(pattern,"", result)
  
  return cleaned_strings

def fit_or_not(content,skill,job_role):
  prompt = f"""This is the resume content: {content}. The required skills for the job role are: {skill}.
  Based on this information, determine if the person is suitable for the {job_role} fresher position.
  Only respond with a 'Yes' or 'No'."""
  result = llm.invoke(prompt)
  result = result.content

  unwanted_symbols = "*&$%"
  pattern = f"[{re.escape(unwanted_symbols)}]"

  # Clean each string in the list
  cleaned_strings = re.sub(pattern,"", result)
  
  return cleaned_strings

def name_from_resume(content):
  prompt = f"""This is the resume content: {content}. Strictly only give the Name of the candidate."""
  result = llm.invoke(prompt)
  result = result.content

  unwanted_symbols = "*&$%"
  pattern = f"[{re.escape(unwanted_symbols)}]"

  # Clean each string in the list
  cleaned_strings = re.sub(pattern,"", result)
  
  return cleaned_strings