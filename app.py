from flask import Flask, jsonify, render_template, request
from quizai import QuizAI

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/questions/<int:amount>")
def get_questions(amount):
	try:
		api_key = request.args.get('api_key')
		model = request.args.get('model', 'tngtech/deepseek-r1t2-chimera:free')
		
		quiz = QuizAI(api_key, model)
		questions = quiz.get_quiz_questions(amount)
		return jsonify(questions)
	except Exception as e:
		print(f"Error: {str(e)}")
		return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
	app.run(debug=True)