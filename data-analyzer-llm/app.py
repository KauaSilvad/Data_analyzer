import os
import openai
import pandas as pd
from flask import Flask, render_template, request
from dotenv import load_dotenv
from analysis.analyzer import generate_basic_insights

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = ""
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)
            insights = generate_basic_insights(df)

            prompt = f"""
            Aqui estão algumas informações extraídas de um conjunto de dados:\n\n{insights}\n
            Gere um resumo em linguagem natural com explicações e observações úteis para um gestor de negócios.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            analysis_result = response['choices'][0]['message']['content']

    return render_template('index.html', result=analysis_result)

if __name__ == '__main__':
    app.run(debug=True)
