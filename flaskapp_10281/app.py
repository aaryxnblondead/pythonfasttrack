from flask import Flask, render_template, abort
from typing import Union

# Initialize Flask application
app = Flask(__name__)

# Route definitions
@app.route('/')
def index() -> Union[str, None]:
    """
    Render the main page of the application.
    Returns:
        str: Rendered HTML template
    """
    try:
        return render_template('index.html')
    except Exception as e:
        abort(500)

@app.route('/about')
def about() -> Union[str, None]:
    """
    Render the about page.
    Returns:
        str: Rendered HTML template
    """
    try:
        return render_template('about.html')
    except Exception as e:
        abort(500)

@app.route('/contact')
def contact() -> Union[str, None]:
    """
    Render the contact page.
    Returns:
        str: Rendered HTML template
    """
    try:
        return render_template('contact.html')
    except Exception as e:
        abort(500)

# Error handlers
@app.errorhandler(404)
def not_found_error(error) -> tuple[str, int]:
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error) -> tuple[str, int]:
    return render_template('500.html'), 500

# Application entry point
if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
