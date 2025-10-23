from mistralai import Mistral
from dotenv import load_dotenv
import random
import os

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model="mistral-medium-latest"

spin_the_wheel = [
    "as a cooking recipe",
    "as a breakup text",
    "as a conspiracy theory",
    "as a haiku",
    "as if you are an 8-year-old explaining",
    "as a Shakespearean monologue",
    "as a love letter"]

def spin_wheel():
    input("\n\nPress Enter to spin the wheel...")
    return random.choice(spin_the_wheel)

def ask_user():
    topic = input("\nEnter a topic you want to learn about: ")
    return topic

def response_to_user(topic,model_response):
    client = Mistral(api_key=api_key)

    prompt = f"""
        You are a fun and engaging AI assistant.
        Your task:
        1. Define the topic **{topic}** briefly in one sentence (about 15% of the total).
        2. Then explain it creatively, humorously, and conversationally (about 75% of the total).
        3. Present the explanation {model_response}.

        Format:
        - Use short paragraphs or playful tone when suitable.
        - Avoid sounding robotic or overly academic.
        - End with a suitable {model_response} closing line.

        Now, define and explain the topic: **{topic}**.
        """

    response = client.chat.complete(
        model=model,
        messages=[
            {"role": "system", "content": "You are a creative and humorous teacher who makes explanations enjoyable and accessible. Keep it under 300 tokens."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    topic = ask_user()
    model_response = spin_wheel()
    print(f"\nModel Response Style: {model_response}")
    print(response_to_user(topic,model_response))