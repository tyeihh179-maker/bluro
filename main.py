import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_prompt = data.get('prompt', '')
    
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    structured_prompt = f"""
    Analyze the following query and provide the response in a clear format:
    1. Direct Answer: (Provide a clear, concise answer)
    2. Evidence: (Provide supporting data, facts, or context)
    3. Sources: (Mention potential reliable reference domains)
    4. Confidence: (State confidence level as High, Medium, or Low)

    Query: {user_prompt}
    """

    try:
        response = model.generate_content(structured_prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
