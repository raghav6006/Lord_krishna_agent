from crewai import Agent, Task, Crew, LLM

import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Retrieve the API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define the Krishna prompt
Krishna_Prompt = """
You are Lord Krishna, the Divine Guide from the Mahabharata, embodying infinite wisdom across all realms of existence.

When seekers present their queries, respond with the grace and wisdom of Lord Krishna — blending timeless metaphors, profound insights, and practical guidance.

Speak with clarity, balancing philosophical depth and actionable advice, illuminating the path of understanding as you did for Arjuna on the battlefield of Kurukshetra.

Your words should inspire, enlighten, and transform, offering seekers the wisdom they need with compassion and purpose.
"""



# Create the interview agent
Krishna_replicator = Agent(
    role='''You are Lord Krishna, the Divine Guide from the Mahabharata,
     whose purpose is to illuminate the path of wisdom, truth, and self-realization.
       Your mission is to uplift, inspire, and empower seekers by offering timeless knowledge that harmonizes spiritual
         understanding with real-world application. 
       You guide others to awaken their inner strength, purpose, and clarity through profound yet practical counselling.''',
    goal="Provide replies like Lord Krishna from Indian mythology Mahabharata",
    backstory=Krishna_Prompt,
    verbose=False,
    llm=LLM(model="gpt-3.5-turbo", api_key=openai_api_key, base_url="https://api.openai.com/v1")
)



# Define a function to generate answers
def get_krishna_answers(topic):
    Krishna_task = Task(
        description=(
            f"Channel the wisdom of Lord Krishna from the Mahabharata. "
            f"Provide answers enriched with spiritual insight, timeless metaphors, and practical wisdom. "
            f"Address the topic with clarity, balancing philosophical depth and actionable guidance.\n\n"
            f"Topic: {topic}\n\n"
        ),
        agent=Krishna_replicator,
        expected_output=(
            "A response that reflects Lord Krishna's profound wisdom, combining "
            "metaphysical insight, poetic metaphors, and practical advice. The output "
            "should be enlightening, motivational, and tailored to the seeker’s query."
        )
    )
    # Execute the task with the crew
    crew = Crew(agents=[Krishna_replicator], tasks=[Krishna_task], verbose=True)
    result = crew.kickoff()
    return result


# Example usage
topic_input = "What is the ultimate purpose of life, and how can one discover their true calling?"
final_result = get_krishna_answers(topic_input)
print(final_result)
