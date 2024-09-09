# Emergency Response AI Assistant

This project is an AI-powered emergency response system that provides immediate guidance for various medical emergencies. It uses natural language processing to understand user queries and provides appropriate first-aid instructions.

## Features

- Real-time emergency response guidance
- Integration with Google's Generative AI for natural language understanding
- Vector database (Pinecone) for fast and accurate emergency matching
- Estimated time of arrival calculation using Google Maps API
- User-friendly interface built with Streamlit

## Demo

Here's a quick demo of the Emergency Response AI Assistant in action:



https://github.com/user-attachments/assets/b04da550-ce01-4010-a774-cb5f0c16ceb5



## Project Structure

- `utils.py`: Contains utility functions for API interactions, embedding, and LLM operations.
- `database_setup.py`: Script for setting up and populating the Pinecone vector database.
- `emergencies.json`: JSON file containing emergency scenarios and corresponding instructions.
- `app.py`: Main Streamlit application file.
- `Dockerfile`: Instructions for building the Docker container.
- `requirements.txt`: List of Python dependencies.

## Setup and Installation

### Option 1: Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/whitehatjr1001/emergency-response-ai.git
   cd emergency-response-ai
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   MAPS_API_KEY=your_maps_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_API_ENV=your_pinecone_environment
   ```

5. Run the database setup script:
   ```
   python database_setup.py
   ```

6. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

### Option 2: Docker Deployment

1. Clone the repository:
   ```
   git clone https://github.com/whitehatjr1001/emergency-response-ai.git
   cd emergency-response-ai
   ```

2. Create a `.env` file as described in step 4 of the local setup.

3. Build the Docker image:
   ```
   docker build -t emergency-response-ai .
   ```

4. Run the Docker container:
   ```
   docker run -p 8501:8501 --env-file .env emergency-response-ai
   ```

The application will be accessible at `http://localhost:8501`.

## Usage
  
1. Open the Streamlit app in your web browser (http://localhost:8501 if running locally or through Docker).
2. Type in your emergency situation or question.
3. The AI will analyze your input and provide appropriate guidance.
4. For emergencies, it will also estimate the arrival time of medical assistance based on your location.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
