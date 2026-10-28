import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Initialize the Gemini client using Environment Variable for security
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_prompt = data.get('prompt', '')
    
    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Prompt engineering to get the 4 structured sections
    structured_prompt = f"""
    Analyze the following query and provide the response strictly in these 4 sections:
    1. Direct Answer: (Provide a clear, concise direct answer)
    2. Evidence: (Provide supporting data, facts, or reasoning)
    3. Sources: (Mention potential reliable references or general knowledge base)
    4. Confidence: (State confidence level as High, Medium, or Low with brief justification)

    Query: {user_prompt}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=structured_prompt
        )
        
        return jsonify({
            "status": "success",
            "response": response.text
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
