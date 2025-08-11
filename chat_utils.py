from langchain_google_genai import ChatGoogleGenerativeAI

# 🔐 Hardcoded Google API Key (Not recommended for production)
GOOGLE_API_KEY = "AIzaSyCitx6KRbk0O0iBWiEv1AOfhLrZJKKd2X4"

# Returns a chat model using Gemini Pro with API key
def get_google_chat_model():
    return ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
        convert_system_message_to_human=True,  # Optional
        verbose=True  # Optional
    )

# Send a prompt to the model and return the response
def ask_chat_model(chat_model, prompt: str):
    response = chat_model.invoke(prompt)
    return response.content
