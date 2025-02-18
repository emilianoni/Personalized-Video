# Personalized Video

````
Video Personalized is a project that enables automatic video generation based on financial transactions. Simply input your Groq API key, upload a video, and provide a data frame in Excel format containing transaction details. The AI-powered system will then generate personalized text overlays that reflect the transaction data, seamlessly embedding contextual messages into the video.

Features:
AI-Generated Text: Automatically creates personalized captions based on financial transactions.
Excel Data Input: Upload an Excel file containing transaction data for seamless processing.
Easy Integration: Just input your API key, upload a video, and provide the data frame.
Dynamic Customization: Generates tailored messages that enhance user engagement.
Ideal for financial institutions, marketing campaigns, and personalized content creation.
````

## Setup Guide

### Follow these steps to set up and run the project:

#### 1. Clone the repository

````
git clone https://github.com/muthiaap/Personalized-Video.git

cd Personalized-Video
````

#### 2. Create a virtual environment

````
python -m venv venv  

source venv/bin/activate  # On macOS/Linux  

venv\Scripts\activate  # On Windows
````

#### 3. Install dependencies

````
pip install -r requirements.txt  
````

#### 4. Add the model

Place the model files in the following directory:
````
./model_NER/model/NER_merchant  
````

#### 5. Add Groq API Key

Add your Groq API key to config.json:
````
{

  "api_key": "your_api_key_here"

}
````
#### 6. Run the application

````
streamlit run video_personalized.py 
````
