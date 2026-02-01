from openai import OpenAI
import json

class QuizAI:
        def __init__(self, api_key, model="tngtech/deepseek-r1t2-chimera:free"):
                self.client = OpenAI(
                        base_url="https://openrouter.ai/api/v1",
                        api_key=api_key
                )
                self.model = model
        def get_quiz_questions(self, amount):
                completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                                {
                                        "role": "system",
                                        "content": "You are a model that poses a general knowledge question",
                                },
                                {
                                        "role": "user",
                                        "content": f"Generate exactly {amount} general knowledge questions, each question should have answers a, b, c, d, only one is correct",
                                },
                        ],
                        response_format={
                                "type": "json_schema",
                                "json_schema": {
                                        "name": "quiz_questions",
                                        "schema": {
                                                "type": "object",
                                                "properties": {
                                                        "questions": {
                                                                "type": "array",
                                                                "items": {
                                                                        "type": "object",
                                                                        "properties": {
                                                                                "question": {"type": "string"},
                                                                                "answers": {
                                                                                        "type": "object",
                                                                                        "properties": {
                                                                                                "a": {"type": "string"},
                                                                                                "b": {"type": "string"},
                                                                                                "c": {"type": "string"},
                                                                                                "d": {"type": "string"}
                                                                                        },
                                                                                        "required": ["a", "b", "c", "d"]
                                                                                },
                                                                                "correct_answer": {
                                                                                        "type": "string",
                                                                                        "enum": ["a", "b", "c", "d"]
                                                                                }
                                                                        },
                                                                        "required": ["question", "answers", "correct_answer"]
                                                                }
                                                        }
                                                },
                                                "required": ["questions"]
                                        }
                                }
                        },
                )
                content = completion.choices[0].message.content
                try:
                        return json.loads(content)
                except json.JSONDecodeError:
                        import re
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                                return json.loads(json_match.group())
                        return content