import openai

client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")

response = client.chat.completions.create(
  model="gpt-5.6-luna",
  messages=[{"role": "user", "content": "Write a short poem"}]
)
print(response.choices[0].message.content)
