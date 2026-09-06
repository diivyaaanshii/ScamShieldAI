
import os
import json

import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Get API key from local .env or Streamlit Cloud Secrets
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=api_key)


def analyze_scam(message):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": """
You are ScamShield AI, a cybersecurity scam detection assistant.

Analyze the user's message for scam or fraud indicators.

Classify the message using:
- LOW
- MEDIUM
- HIGH
- CRITICAL

Identify the scam category, important red flags, explain the reasoning,
and provide a safe recommended action.

Return the result according to the provided JSON schema.
"""
            },
            {
                "role": "user",
                "content": f"Analyze this suspicious message:\n\n{message}"
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "scam_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "risk_level": {
                            "type": "string",
                            "enum": [
                                "LOW",
                                "MEDIUM",
                                "HIGH",
                                "CRITICAL"
                            ]
                        },
                        "risk_score": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 100
                        },
                        "category": {
                            "type": "string"
                        },
                        "red_flags": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "explanation": {
                            "type": "string"
                        },
                        "recommended_action": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "risk_level",
                        "risk_score",
                        "category",
                        "red_flags",
                        "explanation",
                        "recommended_action"
                    ],
                    "additionalProperties": False
                }
            }
        },

        temperature=0
    )

    result = response.choices[0].message.content

    print("RAW AI RESPONSE:", repr(result))

    if not result:
        raise ValueError("AI returned an empty response.")

    return json.loads(result)
