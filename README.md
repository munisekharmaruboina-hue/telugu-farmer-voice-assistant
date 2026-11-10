# 🌾 Telugu Farmer Voice Assistant

An AI-powered, Telugu voice-enabled farming assistant designed to help farmers access agricultural information through natural speech.

## 🎯 Project Overview

The Telugu Farmer Voice Assistant helps farmers ask questions in Telugu and receive understandable answers through both text and voice.

It combines speech recognition, AI-powered responses, agricultural knowledge, and speech synthesis to make farming information easier to access.

## ✨ Key Features

- 🎙️ **Telugu Voice Input:** Ask farming questions using voice.
- 🔊 **Telugu Voice Output:** Listen to spoken answers.
- 🌱 **Crop Cultivation Guidance:** Seasonal calendars and general cultivation advice for 10 crops.
- 🐛 **Pest and Disease Assistance:** Preliminary guidance based on reported crop symptoms.
- 🌦️ **Weather Forecasts:** Rain forecasts for supported locations in Andhra Pradesh.
- 📍 **District Farming Information:** Available crop, soil, fruit, and vegetable information.
- 🛡️ **Safety-Oriented Advice:** Avoids inventing pesticide doses, fertilizer quantities, and unavailable market prices.

## 🌾 Supported Crops

1. Paddy (వరి)
2. Groundnut (వేరుశెనగ)
3. Maize (మొక్కజొన్న)
4. Cotton (పత్తి)
5. Chilli (మిరప)
6. Tomato (టమాట)
7. Banana (అరటి)
8. Mango (మామిడి)
9. Sugarcane (చెరకు)
10. Redgram (కందులు)

## 🛠️ Technology Stack

- Python
- Streamlit
- Gnani.ai Prisma – Speech-to-Text
- Gnani.ai Timbre – Text-to-Speech
- Gemini API – AI-powered responses
- Open-Meteo – Weather forecasts

## ⚙️ How It Works

1. The farmer asks a question in Telugu.
2. Gnani.ai Prisma converts speech into text.
3. The application identifies the question category.
4. Relevant agricultural knowledge or weather information is retrieved.
5. Gemini generates a Telugu response using the available context and safety instructions.
6. Gnani.ai Timbre converts the response into speech.
7. The farmer receives the answer in text and audio.## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/munisekharmaruboina-hue/telugu-farmer-voice-assistant
cd telugu-farmer-voice-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Add your required API credentials locally. Never upload `.env` or API keys to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

## 🧪 Testing

Run the automated tests:

```bash
python -m pytest -q
```

## 🔒 Safety and Limitations

- Disease and pest responses are preliminary guidance, not confirmed diagnoses.
- The application does not currently analyze crop images.
- Unsupported market prices are not presented as live information.
- Farmers should consult qualified local agricultural officers for crop-specific treatment decisions.

## 🔮 Future Improvements

- Expand verified agricultural information to more districts.
- Add crop image-based symptom analysis.
- Improve agricultural data coverage.
- Add more regional language support.

## 👨‍💻 Developer

**Muni Sekhar Maruboina**

AI/ML Engineer | Python Developer | Generative AI Enthusiast

## 🙏 Acknowledgements

Developed for The Great Indian Internship Challenge by Gnani.ai.

