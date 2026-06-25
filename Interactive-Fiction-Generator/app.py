import os
import json
import yaml
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your-secret-key"
app.config['UPLOAD_FOLDER'] = 'stories'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

ALLOWED_EXTENSIONS = {'json', 'yaml', 'yml'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_story(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as f:
        if ext == 'json':
            return json.load(f)
        elif ext in ('yaml', 'yml'):
            return yaml.safe_load(f)
    return None


@app.route('/')
def index():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    return render_template('index.html', stories=files)


@app.route('/play/<story_name>')
def play(story_name):
    story = load_story(story_name)
    if not story:
        flash("Story file not found or corrupted.", "error")
        return redirect(url_for('index'))
    session['current_story'] = story_name
    session['state'] = story.get('initial_state', {})
    session['node'] = story['start']
    return redirect(url_for('story_node'))


@app.route('/story', methods=['GET', 'POST'])
def story_node():
    story_name = session.get('current_story')
    node_key = session.get('node')
    state = session.get('state', {})
    if not story_name or not node_key:
        return redirect(url_for('index'))

    story = load_story(story_name)
    if not story:
        flash("Story file not found or corrupted.", "error")
        return redirect(url_for('index'))

    node = story['nodes'].get(node_key)
    if not node:
        flash("Story node not found.", "error")
        return redirect(url_for('index'))

    # Handle choice submission
    if request.method == 'POST':
        choice_index = int(request.form['choice'])
        choice = node['choices'][choice_index]
        # Handle state updates, if any
        effects = choice.get('set_state', {})
        state.update(effects)
        session['state'] = state
        session['node'] = choice['target']
        return redirect(url_for('story_node'))

    # Evaluate conditions for choices
    choices = []
    for choice in node.get('choices', []):
        show = True
        conds = choice.get('condition', {})
        for key, val in conds.items():
            if state.get(key) != val:
                show = False
                break
        if show:
            choices.append(choice)
    is_end = len(choices) == 0
    return render_template('story.html', node=node, choices=choices, is_end=is_end, story_name=story_name)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Validate file
            try:
                ext = filename.rsplit('.', 1)[1].lower()
                if ext == 'json':
                    json.load(f)
                elif ext in ('yaml', 'yml'):
                    yaml.safe_load(f)
                f.seek(0)
            except Exception as e:
                flash("Invalid story file: {}".format(str(e)), "error")
                return redirect(request.url)
            f.save(filepath)
            flash("Story uploaded successfully.", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid file type.", "error")
    return render_template('upload.html')


@app.route('/download/<story_name>')
def download(story_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], story_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)