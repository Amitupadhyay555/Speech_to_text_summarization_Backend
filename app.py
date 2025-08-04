# # Backend: app.py

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from transformers import pipeline

# app = Flask(__name__)
# CORS(app)

# @app.route("/summarize", methods=["POST"])
# def summarize():
#     if request.method == "POST":
#         data = request.get_json()
#         transcribed_text = data.get("transcribedText", "")

#         # If the number of words is less than 10, return the input text itself as the summary
#         if len(transcribed_text.split()) < 10:
#             return jsonify({"summary": transcribed_text})

#         # Adjust max_length based on the length of the input text
#         max_length = min(2 * len(transcribed_text), 500)  # Adjust the multiplier and maximum limit as needed

#         # Initialize the summarization pipeline with adjusted max_length
#         summarizer = pipeline("summarization", model="facebook/bart-large-cnn", max_length=max_length, min_length=20, length_penalty=2.0)

#         # Use the summarizer with adjusted parameters
#         summary = summarizer(transcribed_text)

#         return jsonify({"summary": summary[0]['summary_text']})
#     else:
#         return jsonify({"error": "Method Not Allowed"}), 405

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)







from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

@app.route("/summarize", methods=["POST"])
def summarize():
    if request.method == "POST":
        data = request.get_json()
        transcribed_text = data.get("transcribedText", "")

        if len(transcribed_text.split()) < 10:
            return jsonify({"summary": transcribed_text})

        max_length = min(2 * len(transcribed_text), 500)

        # ✅ Load model inside the route to avoid memory overuse on startup
        summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",  # ⚠️ lighter model for Render free tier
            max_length=max_length,
            min_length=20,
            length_penalty=2.0
        )

        summary = summarizer(transcribed_text)
        return jsonify({"summary": summary[0]['summary_text']})
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ dynamic port for Render
    app.run(host="0.0.0.0", port=port, debug=False)

