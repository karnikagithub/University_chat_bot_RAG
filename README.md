############## 🤖 University Info ChatBot ################

Introduction
Welcome to the University Info ChatBot! This is a Retrieval-Augmented Generation (RAG) based chatbot designed to help students easily search for and get summarized information from official university websites. Using advanced technologies like LangChain, Google Gemini for embeddings and language models, and FAISS for efficient vector storage, this chatbot allows students to ask queries and get precise, real-time responses.

The chatbot interacts with the following universities' official websites:

University of Chicago

University of Washington

Stanford University

University of North Dakota

Key Features:
🧠 Powered by Google Gemini for embedding and LLM

🔍 Retrieves data from university websites and answers students' queries

🧩 Uses FAISS for local vector store indexing

💬 Streamlit frontend with chat history and a clean UI

🔗 Automatically summarizes content and cites the source URLs

🎨 Chatbot interface with friendly emoji branding (🤖)

"Thanks for asking!! Let me know if anything else is needed 😊"

##########################################################################################

⚙️ Setup Instructions
Follow the steps below to set up and run the chatbot.

1. Clone the Repository
Start by cloning the project repository:
git clone https://github.com/karnikagithub/University_chat_bot_RAG.git
cd university-chatbot

2. Install Dependencies
Make sure you have Python 3.9 or higher installed. Then, install all the dependencies required for the application by running:
pip install -r requirements.txt


3. Set Up Environment Variables
Create a .env file in the root directory of the project to store your Google Gemini API key.
GOOGLE_API_KEY=your_gemini_api_key
You can get your Gemini API key from Google's MakerSuite.

4. Ingest Website Data into FAISS
Before running the application, you need to ingest the data from the universities' websites into a FAISS vector store. This step splits and embeds the documents into chunks for efficient retrieval during chat.
python ingest.py
This script will:

Load data from the universities' websites

Split it into smaller chunks

Embed the chunks using Google Gemini's embeddings model

Save the indexed data to a local FAISS store (in faiss_index/ folder)

5. Run the Application
Now that your data is ingested and indexed, you can run the Streamlit frontend for the chatbot.
streamlit run app.py
Once the app starts, open your browser and visit http://localhost:8501 to interact with the chatbot.

🚀 Using the Application
Input Prompt: Type any question related to the universities in the input box.

Submit: Press the Submit button to ask the chatbot your question.

Response: The chatbot will search for the relevant information from the university websites, summarize it, and present the answer to you.

Source Documents: At the end of each response, the chatbot provides the source URL(s) where the information was retrieved from.

Chat History: Your past conversations will be saved, and you can refer to them during your session.

💡 Tech Stack
    Tool	                   Role
LangChain	    Framework for building RAG (Retrieval-Augmented Generation) systems
Google Gemini	Language model & embedding model for LLM and embeddings
FAISS	        Vector storage for fast similarity search and indexing
Streamlit	    Web-based frontend UI for easy interaction
dotenv	        Manage environment variables securely


🔄 Future Improvements
User Login & Memory Persistence: Implement login and user-specific memory to save and load personalized chat histories.

Add More Universities: Expand the scope by adding data from more university websites.

Dashboard: Add a dashboard to show analytics like most frequent queries, response times, etc.

Save Conversations: Provide an option to download or save the conversation history as a PDF or text file.

📬 Credits
This project was built with ❤️ using LangChain, Google Gemini, FAISS, and Streamlit.

