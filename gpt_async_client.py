import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

class GPTAClient:
    def __init__(self):
        load_dotenv()
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def send_request_stream(self, system, user_content, temperature=0.3):
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content}
        ]

        completion = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            stream=True,
            temperature=temperature
        )

        
        async for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                

        