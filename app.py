from flask import Flask, render_template, request, redirect, url_for
from stories import Story

app = Flask(__name__)

# Example story templates
story_templates = {
    "template1": Story(
        ["place", "noun", "verb", "adjective", "plural_noun"],
        """Once upon a time in a long-ago {place}, there lived a
        large {adjective} {noun}. It loved to {verb} {plural_noun}."""
    ),
    "template2": Story(
        ["name", "adjective", "noun", "verb"],
        """{name} was a {adjective} {noun} who loved to {verb}."""
    )
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_template = request.form['template']
        return redirect(url_for('input_form', template=selected_template))
    return render_template('index.html', templates=story_templates.keys())

@app.route('/input/<template>', methods=['GET', 'POST'])
def input_form(template):
    selected_story = story_templates.get(template)
    if selected_story is None:
        return "Invalid template"  # Handle invalid template selection

    if request.method == 'POST':
        prompts = selected_story.prompts
        user_inputs = {prompt: request.form[prompt] for prompt in prompts}
        return redirect(url_for('generate_story', template=template, **user_inputs))
    
    return render_template('input_form.html', prompts=selected_story.prompts)

@app.route('/generate/<template>')
def generate_story(template):
    selected_story = story_templates.get(template)
    if selected_story is None:
        return "Invalid template"  # Handle invalid template selection
    
    user_inputs = {prompt: request.args.get(prompt) for prompt in selected_story.prompts}
    generated_story = selected_story.generate(user_inputs)
    return render_template('story.html', generated_story=generated_story)

if __name__ == '__main__':
    app.run(debug=True)
