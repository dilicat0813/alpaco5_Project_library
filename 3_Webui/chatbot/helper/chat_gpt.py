import openai
import os

openai.api_key = os.getenv('API_KEY')
openai.organization = "org-hGPtZbB25DAWDQflBn094cUK" # https://platform.openai.com/account/org-settings

# https://platform.openai.com/docs/models/gpt-3-5
model_engine = "text-davinci-003"
# 4,096 tokens or about 3,000 words. As a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text.
max_tokens = 1024

def ask_chat_GPT(text):
    response = openai.Completion.create(model=model_engine, prompt=text, temperature=0.6, max_tokens=max_tokens)
    return response.choices[0].text