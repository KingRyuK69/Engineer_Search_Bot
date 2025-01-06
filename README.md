# Engineer Search Bot

A Streamlit-based application for searching engineering candidates based on skills, experience, and budget using MongoDB for data storage and Hugging Face for generating embeddings.

---

## Features
- **Interactive UI**: Built using Streamlit for ease of use.
- **Skill Matching**: Matches user queries with candidate skills using semantic search.
- **Flexible Filters**: Supports filtering by skills, years of experience, and budget constraints.
- **Real-time Embedding Generation**: Generates embeddings for candidates' skills using Hugging Face models.
- **MongoDB Integration**: Stores and retrieves candidate data efficiently.

---

## Architecture Overview
1. **Streamlit Frontend**: Provides an interactive user interface for querying candidates.
2. **MongoDB Backend**: Stores candidate data and retrieves relevant candidates based on queries.
3. **Hugging Face Embeddings**: Utilizes Hugging Face's API for semantic matching of skills.

---

## Setup Instructions

### Prerequisites
- Python 3.7+
- MongoDB instance (local or cloud-based)
- Hugging Face API Token
- Environment variables configured in a `.env` file:
  ```env
  MONGO_URI=<your_mongo_uri>
  HUGGINGFACE_TOKEN=<your_huggingface_api_token>
  HUGGINGFACE_URL=<your_huggingface_api_url>
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Application Workflow

1. **Input Query**: Users can type queries like "Find me a Python Developer with 3 years of experience."
2. **Processing**: 
   - The query is parsed to extract key filters (e.g., skills, budget, experience).
   - A semantic embedding is generated for the query using Hugging Face.
3. **Database Search**:
   - MongoDB is queried for matching candidates.
   - Candidates are ranked based on cosine similarity of embeddings and other filters.
4. **Output**:
   - Top candidates are displayed with details such as name, skills, salary, and experience.

---

## Code Overview

### Main Application (`app.py`)
- Initializes the Streamlit interface.
- Handles user input and displays results.

### Candidate Matching (`database.py`)
- Fetches candidate data from MongoDB.
- Uses Hugging Face API to generate embeddings for skills and queries.
- Ranks candidates based on cosine similarity and filters.

### Utilities (`utils.py`)
- Handles embedding generation and retries for Hugging Face API.

---

## Example Queries
- "Find me someone with an experience in C#"
- "Find me someone with 3 years of experience in Java"
- "Find me someone with 4 years of Python experience within a budget of 150000 USD"
- "Find me someone with 4+ years of Python experience within a budget of 90000 EUR"

---

## Key Files
- `app.py`: Main application logic.
- `database.py`: MongoDB integration and candidate filtering.
- `utils.py`: Embedding generation utilities.
- `.env`: Environment variables (not included in the repository).

---

## Future Enhancements
- Add support for more advanced filters (e.g., location, availability).
- Optimize database queries for faster results.
- Enhance the UI with additional visualization options.
- Add support for batch candidate uploads.

---

## Link to access the bot - https://mercorengineerbot.streamlit.app/

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
