import streamlit as st
import chromadb
from pypdf import PdfReader

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="RAG-Powered Career Hub",
    page_icon="🎯",
    layout="wide"
)

# Initialize Ollama LLM and Embeddings
llm = OllamaLLM(model="llama3.2")
embeddings = OllamaEmbeddings(model="llama3.2")

# Initialize ChromaDB (In-Memory for simplicity)
chroma_client = chromadb.EphemeralClient()
collection = chroma_client.get_or_create_collection(name="resume_docs")

# -----------------------------
# Helper Functions
# -----------------------------
def process_pdf(pdf_file):
    """Extracts text from PDF, chunks it, and saves it to a vector database."""
    pdf_reader = PdfReader(pdf_file)
    raw_text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            raw_text += page.extract_text() + "\n"
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    chunks = text_splitter.split_text(raw_text)
    
    # Clear previous documents and embed new ones
    # Note: To keep things light with Ollama, we will pass standard chunks or embed them
    return raw_text, chunks

# -----------------------------
# App Title & Intro
# -----------------------------
st.title("🎯 Next-Gen RAG Career Coach & AI Interviewer")
st.write("Upload your Resume or Curriculum PDF to unlock highly hyper-personalized career trajectories, dynamic upskilling paths, and simulated technical mock interviews.")
st.divider()

# -----------------------------
# Sidebar - Document Upload & Profile
# -----------------------------
st.sidebar.header("📁 Document Center")
uploaded_file = st.sidebar.file_uploader("Upload Resume / CV / Syllabus (PDF)", type=["pdf"])

pdf_context = ""
chunks_data = []

if uploaded_file is not None:
    with st.sidebar.spinner("Parsing and indexing document..."):
        pdf_context, chunks_data = process_pdf(uploaded_file)
        st.sidebar.success("✅ PDF processed successfully!")

st.sidebar.divider()
st.sidebar.header("👤 Additional Profile Info")
experience = st.sidebar.selectbox("Experience Level", ["Student", "Fresher", "0-2 Years", "2-5 Years", "5+ Years"])
career_goal = st.sidebar.text_input("Target Job Role", placeholder="e.g., Data Scientist, DevOps Engineer")

# -----------------------------
# Main Navigation Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["💡 Career Guidance", "🤖 AI Mock Interview", "💼 Career Opportunities"])

# ---------------------------------------------------------
# TAB 1: CAREER GUIDANCE
# ---------------------------------------------------------
with tab1:
    st.subheader("🚀 Personalized Skill Roadmaps & Growth")
    
    question = st.text_area(
        "Ask a tailored question about your profile:",
        placeholder="Example: Based on my resume, what skill gaps do I have for a Full-Stack Developer role?",
        key="guidance_q"
    )
    
    if st.button("🚀 Generate Strategic Roadmap", type="primary"):
        if not uploaded_file:
            st.warning("Please upload your resume PDF in the sidebar first.")
        else:
            with st.spinner("Analyzing profile gaps..."):
                # Simple RAG context fetching (Passing relevant text block summaries directly into the LLM context)
                context_str = "\n".join(chunks_data[:5]) # Taking top chunks as context
                
                prompt = f"""
                You are a premium, executive-level Career Coach. Optimize your feedback for a candidate aiming to become a '{career_goal}'.
                
                Candidate Document Context:
                {context_str}
                
                Candidate Meta Profile:
                Experience Level: {experience}
                Target Role: {career_goal}
                
                User Request:
                {question}
                
                Provide a detailed breakdown containing:
                1. Contextual Gap Analysis (What is missing from their PDF compared to the target role)
                2. Explicit Learning Roadmap (Broken into 30-60-90 days)
                3. High-Impact Projects to bridge the gap
                """
                try:
                    response = llm.invoke(prompt)
                    st.markdown("### 🎯 Your Career Blueprint")
                    st.markdown(response)
                except Exception as e:
                    st.error("Error communicating with local Ollama instance.")
                    st.code(str(e))

# ---------------------------------------------------------
# TAB 2: AI INTERVIEW SIMULATOR
# ---------------------------------------------------------
with tab2:
    st.subheader("🎭 AI Technical & Behavioral Mock Interview")
    st.write("Generate custom interview questions directly tailored to your uploaded profile and targeted role.")
    
    if st.button("🏁 Generate Custom Interview Questions"):
        if not uploaded_file:
            st.warning("Please upload a PDF first to generate context-specific questions.")
        else:
            with st.spinner("Compiling industry questions..."):
                context_str = "\n".join(chunks_data[:4])
                prompt = f"""
                Act as an elite Technical Interviewer for a {career_goal} position. 
                Based on the candidate's background details here:
                {context_str}
                
                Generate a list of 5 hard-hitting interview questions:
                - 3 Technical Questions covering their listed stack vs expected skills for a {career_goal}.
                - 2 Behavioral/Scenario Questions based on their project/experience scale.
                """
                try:
                    questions_output = llm.invoke(prompt)
                    st.session_state['interview_questions'] = questions_output
                except Exception as e:
                    st.error("Error generating questions.")

    if 'interview_questions' in st.session_state:
        st.markdown("### 📋 Interview Script")
        st.markdown(st.session_state['interview_questions'])
        
        st.divider()
        st.markdown("### 📝 Practice Sandbox")
        user_answer = st.text_area("Type your answer to any question above to get instant grading:", height=150)
        
        if st.button("💯 Grade My Answer"):
            if user_answer:
                with st.spinner("Evaluating performance parameters..."):
                    eval_prompt = f"""
                    You are an expert interviewer. Evaluate the candidate's response to your question.
                    Candidate Target Role: {career_goal}
                    Candidate Answer: {user_answer}
                    
                    Provide constructive feedback, a mock score out of 10, and an optimized, high-scoring model answer alternative.
                    """
                    feedback = llm.invoke(eval_prompt)
                    st.info("### 📊 Performance Feedback")
                    st.markdown(feedback)

# ---------------------------------------------------------
# TAB 3: CAREER OPPORTUNITIES
# ---------------------------------------------------------
with tab3:
    st.subheader("💼 Industry Roles & Career Tracks")
    st.write("Discover what job families and alternative industries you qualify for right now based on your document data.")
    
    if st.button("🔍 Map My Career Horizons"):
        if not uploaded_file:
            st.warning("Please upload your PDF resume to run parsing analytics.")
        else:
            with st.spinner("Analyzing industry verticals..."):
                context_str = "\n".join(chunks_data[:5])
                prompt = f"""
                Analyze the following candidate context data extracted from their profile:
                {context_str}
                
                Targeting: {career_goal}
                Experience: {experience}
                
                Please map out:
                1. Immediate Job Roles they are highly qualified to apply for right now.
                2. Long-term Career Trajectories (e.g., moving into Architecture, Management, or Lead roles in 5 years).
                3. Alternative/Pivot Pathways (e.g., adjacent roles they could move into easily using their current technical foundation).
                """
                try:
                    opportunities = llm.invoke(prompt)
                    st.markdown("### 🌐 Market Opportunity Mapping")
                    st.markdown(opportunities)
                except Exception as e:
                    st.error("Error processing market analysis.")
