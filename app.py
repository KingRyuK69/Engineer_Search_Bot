import streamlit as st
from dotenv import load_dotenv
from database import fetch_and_embed_candidates

load_dotenv()

def main():
    st.set_page_config("Engineer Search")
    st.header("Engineer Search Bot 😁")

    # Initialize session state
    if 'query' not in st.session_state:
        st.session_state['query'] = None

    # Display example queries
    st.write("Example queries:")
    example_queries = [
        # "Find me a Python Developer",
        # "Find me a React Developer",
        "Find me someone with an experience in C#",
        "Find me someone with a 3 years of experience in Java",
        "Find me someone with a 4 year experience in Python within a budget of 150000USD",
        "Find me someone with a 4 or more years of experience in python within a budget of 90000EUR"
    ]
    for query in example_queries:
        if st.button(query):
            st.session_state['query'] = query

    # Get user input
    user_question = st.text_input("Ask a question to find engineers", key="user_question")

    # Send button
    if st.button("Search"):
        if user_question:
            st.session_state['query'] = user_question
            
    # Clear button
    if st.button("Clear"):
        st.session_state['query'] = None
        st.session_state['candidates'] = None        

    # Process query
    if st.session_state['query']:
        process_query(st.session_state['query'])

def process_query(query):
    # Fetch candidates from MongoDB and add embeddings to the documents
    candidates = fetch_and_embed_candidates(query)

    # Check if any candidates were fetched
    if candidates:
        # Display fetched candidates
        st.write("Fetched Candidates")
        for candidate in candidates:
            st.write(f"Name: {candidate['name']}")
            st.write(f"Name: {candidate['skillName']}")
            st.write(f"Name: {candidate['description']}")
            st.write(f"Name: {candidate['startDate']}")
            st.write(f"Name: {candidate['endDate']}")
            st.write(f"Name: {candidate['fullTimeSalary']}")
            st.write(f"Name: {candidate['fullTimeSalaryCurrency']}")
            st.write(f"Name: {candidate['partTimeSalary']}")
            st.write(f"Name: {candidate['partTimeSalaryCurrency']}")
    else:
        st.write("No candidates meet the criteria.")

if __name__ == "__main__":
    main()