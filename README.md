# Sci-Bot 🧠💬

Welcome to Sci-Bot, your intelligent companion for computer science-related questions! Sci-Bot is a chatbot developed using Python and Flask that provides answers to basic questions about computer science and can even learn from user interactions.

## Features
- **Question Answering:** Sci-Bot can answer basic questions related to computer science topics.
- **Interactive Learning:** If Sci-Bot encounters an unknown question, it can learn from user-provided answers and improve over time.
- **Accuracy:** The model behind Sci-Bot achieves approximately 82% accuracy in answering questions.
- **User-Friendly Interface:** The chat interface is intuitive and easy to use.

## How it Works
1. **Ask a Question:** Type your question into the chat interface and hit "Send".
2. **Get an Answer:** Sci-Bot will analyze your question and provide the best answer it knows.
3. **Teach Sci-Bot:** If Sci-Bot doesn't know the answer, you can teach it by providing the correct response.

![Sci-Bot Interface](https://github.com/Nkprasath/Sci-bot/assets/64826468/2c83c1c7-18b0-44ab-8fd9-414341ed7fde)


[Demo video Link](https://youtu.be/wZMji8_Bf1U)

## My Thought Process to Create This Bot
- Task was to create a NLP chatbot, so I decided to create one from scratch.
- Since the time limit was less, I could not develop and train a LLM.
- Using OpenAI or Hugging Face models cannot classify as something I made, since I will just use the API and the text document to answer questions.

## Getting Started
To run Sci-Bot locally, follow these steps:
1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Flask application with `python app.py`.
4. Open your web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to start chatting with Sci-Bot.

To run using a shell script, follow these steps:
1. Make sure to have Git Bash on your PC.
2. Navigate to the working directory.
3. Run the app by typing `bash scibot.sh` in the terminal.

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
