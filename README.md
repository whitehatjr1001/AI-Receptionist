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

ist/blob/main/assets/DEMO%20-%20Made%20with%20Clipchamp.mp4


## Project Structure

- `utils.py`: Contains utility functions for API interactions, embedding, and LLM operations.
- `database_setup.ipynb`: Jupyter notebook for setting up and populating the Pinecone vector database.
- `emergencies.json`: JSON file containing emergency scenarios and corresponding instructions.
- `app.py`: Main Streamlit application file.

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/whitehatjr1001/emergency-response-ai.git
   cd emergency-response-ai
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   MAPS_API_KEY=your_maps_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_API_ENV=your_pinecone_environment
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Open the Streamlit app in your web browser.
2. Type in your emergency situation or question.
3. The AI will analyze your input and provide appropriate guidance.
4. For emergencies, it will also estimate the arrival time of medical assistance based on your location.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
