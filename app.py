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
        st.text_input("Ask a question to find engineers", value='', key="user_question")    

    # Process query
    if st.session_state['query']:
        process_query(st.session_state['query'])

def process_query(query):
    # Fetch candidates from MongoDB and add embeddings to the documents
    candidates = fetch_and_embed_candidates(query)

    # Check if any candidates were fetched
    if candidates:
        # Display fetched candidates
        for i, candidate in enumerate(candidates, 1):
            st.markdown(f"""
            **Candidate {i}**
            - **Name:** {candidate['name']}
            - **Skills:** {candidate['skillName']}
            - **Brief:** {candidate['description']}
            - **StartDate:** {candidate['startDate']}
            - **EndDate:** {candidate['endDate']}
            - **FTE Salary:** {candidate['fullTimeSalary']}
            - **FTE Currency:** {candidate['fullTimeSalaryCurrency']}
            - **Part Time Salary:** {candidate['partTimeSalary']}
            - **Part Time Salary Currency:** {candidate['partTimeSalaryCurrency']}
            """)
    else:
        st.write("No candidates meet the criteria.")

if __name__ == "__main__":
    main()