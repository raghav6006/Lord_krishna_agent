from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Retrieve the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define Krishna's role and replicator as before
Krishna_Prompt = """
You are Lord Krishna, the Divine Guide from the Mahabharata, providing clear and practical wisdom.
When seekers present their questions, respond with straightforward advice that is easy to understand.
Use simple language, relatable examples, and practical guidance to help them navigate their challenges.
"""

Krishna_replicator = Agent(
    role='''You are Lord Krishna, the Divine Guide from the Mahabharata,
     whose purpose is to offer clear and practical wisdom.
     You inspire and empower seekers by providing straightforward knowledge that blends spiritual understanding with everyday life.
     Your guidance is compassionate, using simple stories and relatable examples.
     Your words provide both emotional support and actionable advice.''',
    goal="Provide replies like Lord Krishna from Indian mythology Mahabharata, offering compassionate and easy-to-understand counseling for life's challenges.",
    backstory=Krishna_Prompt,
    verbose=False,
    llm=LLM(model="gpt-3.5-turbo", api_key=openai_api_key, base_url="https://api.openai.com/v1")
)

@app.route('/')
def home():
    # Clear the conversation history on each page reload
    session['history'] = []
    return render_template('index.html')

@app.route('/get_krishna_answers', methods=['POST'])
def get_krishna_answers():
    data = request.json
    user_message = data.get('topic')

    # Append user message to history
    session['history'].append({"role": "user", "content": user_message})

    # Prepare conversation history for context
    conversation = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in session['history']])

    Krishna_task = Task(
        description=(
            f"Channel the wisdom of Lord Krishna from the Mahabharata. "
            f"Provide clear and empathetic answers with practical insights and easy-to-understand language. "
            f"Offer compassionate counseling that addresses emotional, psychological, and everyday challenges. "
            f"Deliver relatable and supportive guidance with actionable steps and spiritual clarity.\n\n"
            f"Conversation:\n{conversation}\n\n"
        ),
        agent=Krishna_replicator,
        expected_output=(
            "A response that reflects Lord Krishna's profound wisdom, using simple language and relatable examples. "
            "The response should be comforting, motivational, and easy for the seeker to understand and apply."
        )
    )

    # Execute the task with the crew
    crew = Crew(agents=[Krishna_replicator], tasks=[Krishna_task], verbose=True)
    result = crew.kickoff()

    # Extract Krishna's response and append to history
    krishna_response = result.raw
    krishna_response = krishna_response.replace("\n", "<br>")
    session['history'].append({"role": "krishna", "content": krishna_response})

    return jsonify({"Krishna_answer": krishna_response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
