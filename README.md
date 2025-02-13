# Personalized Video
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
