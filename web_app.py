"""Local Flask interface for the existing, read-only idea analysis."""

from flask import Flask, render_template, request

from analysis import analyze_idea

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html', description='')


@app.post('/analyze')
def analyze():
    description = request.form.get('description', '').strip()
    if not description:
        return render_template('index.html', description=description,
                               error='Tell us a little about your idea before we explore.'), 400
    try:
        report = analyze_idea(description)
    except Exception:
        app.logger.exception('Idea analysis failed')
        return render_template('index.html', description=description,
                               error='We couldn’t build your report right now. Please try again. If this continues, check that the local database is available.'), 503
    return render_template('results.html', report=report)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
