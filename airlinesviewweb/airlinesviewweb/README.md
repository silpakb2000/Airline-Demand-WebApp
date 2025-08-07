# Airline Demand WebApp

A data-driven web application that visualizes real-time flight data using the AviationStack API. It includes charts, statistics, and an AI-powered chatbot for summarizing and answering questions about global flight activity.

## Features

- Real-time flight data fetched from [AviationStack API](https://aviationstack.com/)
- Clean, responsive UI with charts, tables, and stats
- AI chatbot powered by Groq's LLaMA-3 model for:
  - Demand summary
  - User query responses
- Flask backend and Bootstrap frontend
- Docker and Render deployment support

## Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, Chart.js
- **Backend:** Python (Flask)
- **AI APIs:** OpenAI / Groq
- **Deployment:** Docker, Render

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` for package management
- AviationStack, OpenAI, and/or Groq API keys

### Clone the Repository

```bash
git clone https://github.com/your-username/airline-demand-webapp.git
cd airline-demand-webapp 

```
### Setup Environment
- Create a .env file:

- `touch` .env
  
### Add the following to .env:
- OPENAI_API_KEY=your_openai_key
- GROQ_API_KEY=your_groq_key

### Install Dependencies
- `pip` install -r requirements.txt


### Run the App
- python app.py
- Visit http://localhost:5000 in your browser.

### Docker Setup
- To build and run locally with Docker:

- docker build -t airline-demand-webapp .
- docker run -p 5000:5000 airline-demand-webapp
