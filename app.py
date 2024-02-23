import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

load_dotenv()

SLACK_BOT_TOKEN=os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN=os.getenv("SLACK_APP_TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

app = App(token=SLACK_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

#Listen to messages
@app.message("")
def message_hello(message, say):
    user = message["user"]
    completion = client.chat.completions.create(
        model="gpt-4",
         messages=[
            {"role": "system", "content": "You are a test slack bot. You respond in Slack markdown. You respond in brief and to the point."},
            {"role": "user", "content": message["text"]}
        ]
    )
    #Say the response
    response = completion.choices[0].message.content
    tokens_used = completion.usage.total_tokens
    say(f"{response} \n\nTokens used: {tokens_used}")



#Start app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

