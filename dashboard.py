import streamlit as st
import pandas as pd
import plotly.express as px
from modules import Analyse_repo
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models.openai import ChatOpenAI
import warnings

# Suppress warnings using warnings module
warnings.filterwarnings("ignore")

load_dotenv()
DB_FAISS_PATH = 'vectorstore/db_faiss'


# Set the page configuration
st.set_page_config(
    page_title="Developer Performance Dashboard",
    layout="wide"
)

def load_llm():
        """to load llm"""
        llm_openai = ChatOpenAI(
        model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("openai_api_key")
        )

        return llm_openai


def fetch_github_data(repo_url):
    """Function to fetch data and generate CSV from GitHub repository"""
    # obj=Analyse_repo(repo_name="scikit-learn/scikit-learn")
    obj=Analyse_repo(repo_name=repo_url)
    response= obj.Give_analytics(limit_count=5)
    if response:
        st.success("CSV files created successfully!")
    else:
        st.error("Error loading repo")


def conversational_chat(query):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]

# Load data
@st.cache_data
def load_data():
    commits_df = pd.read_csv('commits.csv')
    pr_df = pd.read_csv('pr_data.csv')
    issue_df = pd.read_csv('issue_data.csv')
    performance_df = pd.read_csv('developer_performance.csv')
    return commits_df, pr_df, issue_df, performance_df

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Enter GitHub URLs", "Dashboard", "Chatbot"])

# ===================
# Page 1: Enter GitHub URLs
# ===================
if page == "Enter GitHub URLs":
    st.title("Enter GitHub URLs")
    
    repo_url = st.text_input("Enter the GitHub repository URL:")
    
    if st.button("Fetch Data"):
        if repo_url:
            fetch_github_data(repo_url)
        else:
            st.error("Please enter a valid GitHub URL.")

# ===================
# Page 2: Dashboard
# ===================
if page == "Dashboard":
    st.title("Developer Performance Dashboard")
    commits_df, pr_df, issue_df, performance_df = load_data()
    
    # ===================
    # Overview Page
    # ===================
    st.header("Team Overview")
    
    # Show high-level metrics
    total_commits = commits_df['Commits'].sum()
    total_prs = pr_df['PRs'].sum()
    total_issues_resolved = issue_df['Resolved Issues'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Commits", total_commits)
    col2.metric("Total PRs", total_prs)
    col3.metric("Issues Resolved", total_issues_resolved)

    # Line chart for commits over time
    st.subheader("Commits Over Time")
    fig = px.line(commits_df, x='Date', y='Commits', color='Author', title="Commits per Developer")
    st.plotly_chart(fig)

    # ===================
    # Individual Developer Page
    # ===================
    st.header("Developer Performance")

    # Dropdown to select a developer
    developers = performance_df['Developer'].unique()
    selected_dev = st.selectbox("Select Developer", developers)

    # Filter data for the selected developer
    dev_data = performance_df[performance_df['Developer'] == selected_dev]

    col1, col2, col3 = st.columns(3)
    col1.metric("Commits", int(dev_data['Commits'].values[0]))
    col2.metric("Code Churn (Lines)", int(dev_data['Code Churn (Lines)'].values[0]))
    col3.metric("PRs Opened", int(dev_data['PRs Opened'].values[0]))

    st.subheader(f"{selected_dev}'s Pull Request Metrics")
    st.write(dev_data[['PRs Opened', 'PRs Merged', 'Avg PR Size', 'Avg PR Review Time (Days)']])

    st.subheader(f"{selected_dev}'s Issue Resolution Metrics")
    st.write(dev_data[['Issues Resolved', 'Avg Issue Resolution Time (hours)']])

    # ===================
    # PR Analysis Page
    # ===================
    st.header("Pull Request (PR) Analysis")

    # Plot PR size distribution
    st.subheader("PR Size Distribution")
    fig = px.histogram(pr_df, x='Total PR Size', nbins=30, title="PR Size Distribution")
    st.plotly_chart(fig)

    # PR merge rate
    st.subheader("PR Merge Rate by Developer")
    fig = px.bar(pr_df, x='Author', y='Merged PRs', title="PR Merge Rate")
    st.plotly_chart(fig)

    st.subheader("Average PR Review Time by Developer")
    fig = px.bar(pr_df, x='Author', y='Total Review Time (hours)', title="Average PR Review Time")
    st.plotly_chart(fig)

    # ===================
    # Issue Tracking Page
    # ===================
    st.header("Issue Tracking")

    # Line chart for issue resolution over time
    st.subheader("Issues Resolved Over Time")
    fig = px.line(issue_df, x='Date', y='Resolved Issues', color='Assignee', title="Issues Resolved per Developer")
    st.plotly_chart(fig)

    # Show average issue resolution time
    st.subheader("Average Issue Resolution Time by Developer")
    fig = px.bar(issue_df, x='Assignee', y='Avg Issue Resolution Time (hours)', title="Average Issue Resolution Time")
    st.plotly_chart(fig)

# ===================
# Page 3: Chatbot
# ===================
if page == "Chatbot":
    st.title("Chat with the Data")
    loader = CSVLoader(file_path='developer_performance.csv', encoding="utf-8", csv_args={
                'delimiter': ','})
    
    data = loader.load()
  
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    

    db = FAISS.from_documents(data, embeddings)
    db.save_local(DB_FAISS_PATH)
    llm = load_llm()
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())


    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me anything about Developers performance  🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]


    response_container = st.container()

    #container for the user's text input
    container = st.container()


    with container:
        with st.form(key='my_form', clear_on_submit=True):
            
            user_input = st.text_input("Query:", placeholder="Chat with Performance data here (:", key='input')
            submit_button = st.form_submit_button(label='Send')
            
        if submit_button and user_input:
            output = conversational_chat(user_input)
            
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")


   
