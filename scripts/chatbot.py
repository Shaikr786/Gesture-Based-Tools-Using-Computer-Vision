import google.generativeai as gen_ai
import json

# Replace with your actual Google Gemini API key
GOOGLE_API_KEY = "AIzaSyCxO4iKszCQ9KPFGCbY5Xzj7SBOaM2tHk0"

# Configure the Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-2.0-flash")


def handle_user_message(user_message):
    """
    Process user input and generate a bot response using the Gemini API.

    :param user_message: The message from the user.
    :return: The chatbot's response.
    """

    try:
        # Start or continue a chat session
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_message)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

def chatbot_console():
    """
    Run a console-based chatbot interaction.
    """
    print("ChatBot 🤖 (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        bot_response = handle_user_message(user_input)
        print(f"Bot: {bot_response['response']}")

if __name__ == "__main__":
    chatbot_console()
