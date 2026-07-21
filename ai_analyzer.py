import os
import json
import re

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_scam(message):

    prompt = f"""
Analyze this suspicious message for scam or fraud risk:

{message}

Return ONLY a valid JSON object. Do not add any text before or after it.

The JSON must have exactly these fields:

{{
    "risk_level": "HIGH",
    "risk_score": 90,
    "category": "Digital Arrest Scam",
    "red_flags": [
        "Threat of arrest",
        "Urgent demand for money",
        "Impersonation of authorities"
    ],
    "explanation": "This message contains multiple signs of a scam.",
    "recommended_action": "Do not send money or share personal information. Report the message."
}}

Use a risk_level of LOW, MEDIUM, HIGH, or CRITICAL.
The risk_score must be between 0 and 100.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    # Print the actual AI response in the terminal for debugging
    print("RAW AI RESPONSE:", repr(result))

    if not result:
        raise ValueError("AI returned an empty response.")

    result = result.strip()

    # Remove Markdown code blocks if the AI adds them
    result = re.sub(r"```json", "", result, flags=re.IGNORECASE)
    result = re.sub(r"```", "", result)

    # Find the JSON object
    start = result.find("{")
    end = result.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"AI did not return valid JSON. Raw response: {result}"
        )

    json_text = result[start:end + 1]

    return json.loads(json_text)