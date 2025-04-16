# AI-Powered P&ID Analysis Website

A web platform for a project that uses artificial intelligence to extract and analyze information from Piping & Instrumentation Diagrams (P&IDs).

## Features

- Interactive landing page with animated elements
- Detailed explanation of P&ID analysis challenges and AI solution
- Interactive demo with sample diagrams and results
- Technology stack overview
- Industry use cases
- Team section
- Contact form

## Tech Stack

- Python 3.8+
- Flask 2.2.3
- Flask-WTF for form handling
- Jinja2 templates
- HTML/CSS/JavaScript
- Font Awesome for icons

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Set the Flask application:
   ```
   export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
   ```
2. Run the application:
   ```
   flask run --host=0.0.0.0
   ```
   Or simply:
   ```
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
pid_analysis_website/
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
├── static/                # Static assets
│   ├── css/               # CSS files
│   │   └── main.css       # Main stylesheet
│   ├── js/                # JavaScript files
│   │   └── main.js        # Main JavaScript file
│   └── images/            # Image assets
├── templates/             # Jinja2 templates
│   ├── base.html          # Base template with common elements
│   ├── index.html         # Home page template
│   └── contact.html       # Contact page template
└── README.md              # Project documentation
```
