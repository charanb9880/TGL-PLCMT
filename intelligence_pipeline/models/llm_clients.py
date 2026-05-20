from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config.settings import GEMINI_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY

def get_openai_client():
    # Using Groq (Llama 3.3 70B) for the OpenAI branch
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.1,
        max_tokens=1000
    )

def get_gemini_client():
    # Switching to Groq Llama to bypass Gemini Quota issues (Mixtral was deprecated)
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0.1,
        max_tokens=1000
    )

def get_openrouter_client():
    # Using Cerebras (Llama 3.1 8B) for the OpenRouter branch
    return ChatOpenAI(
        base_url="https://api.cerebras.ai/v1",
        api_key=CEREBRAS_API_KEY,
        model="llama3.1-8b",
        temperature=0.1,
        max_tokens=1000
    )
