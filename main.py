from flask import Flask,request,send_file
from openai import OpenAI
from dotenv import load_dotenv
import os
from gtts import gTTS

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/ping")
def ping():
    return "pong!"


@app.route("/hit-me",methods=["POST"])
def didIAskQuestion():
    temp_file_name = "temp.wav"
    modelWp = "whisper-1"
    modelGpt = "gpt-3.5-turbo"
    lang = 'en'
    save_path = os.path.join(temp_file_name)
    request.files["file"].save(save_path)
    af = open(save_path, "rb")
    transcription = client.audio.transcriptions.create(
        model=modelWp, 
        file=af,
        response_format="text" 
    )
    print(transcription)
    response = client.chat.completions.create(
        model=modelGpt,
        messages=[
            {
            "role": "user",
            "content": transcription
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    res = response.choices[0].message.content
    print(res,"response")
    obj = gTTS(text=res, lang=lang, slow=False)
    obj.save("res.mp3")
    try:
	    return send_file("res.mp3")
    except Exception as e:
         return str(e)
         
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)