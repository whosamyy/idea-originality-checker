"""Local Flask interface for the existing idea analysis and runtime insertion."""

from flask import Flask, abort, redirect, render_template, request, url_for

from analysis import analyze_idea
from app import add_user_idea
from vector_store import get_user_record

# Vercel serves public/static via its CDN; Flask serves the same URL locally.
app = Flask(__name__, static_folder='public/static', static_url_path='/static')


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
        app.logger.error('Idea analysis failed')
        return render_template('index.html', description=description,
                               error='We couldn’t build your report right now. Please try again. If this continues, check that the selected database is available.'), 503
    return render_template('results.html', report=report)


@app.route('/add-idea', methods=['GET', 'POST'])
def add_idea():
    name = ''
    description = ''
    errors = {}
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if not name:
            errors['name'] = 'Give your idea a name before saving it.'
        if not description:
            errors['description'] = 'Describe what your idea does before saving it.'
        if not errors:
            try:
                idea_id = add_user_idea(name, description)
            except Exception:
                app.logger.error('Adding a user idea failed')
                return render_template('add_idea.html', name=name, description=description,
                                       errors={}, error='We couldn’t save your idea right now. Please try again.'), 503
            # Refreshing the confirmation page must not insert another item.
            return redirect(url_for('idea_added', idea_id=idea_id), code=303)
    return render_template('add_idea.html', name=name, description=description,
                           errors=errors), (400 if errors else 200)


@app.get('/ideas/<idea_id>')
def idea_added(idea_id):
    if not idea_id.startswith('user:'):
        abort(404)
    try:
        item = get_user_record(idea_id)
    except Exception:
        app.logger.error('Reading a user idea failed')
        return render_template('add_idea.html', name='', description='', errors={},
                               error='We couldn’t open the confirmation right now. Please try again.'), 503
    if item is None:
        abort(404)
    return render_template('idea_added.html', idea_id=idea_id,
                           name=item['metadata'].get('company_name', 'Your idea'),
                           description=item['document'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
