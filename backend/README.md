## Getting Started

Make sure you're using a Python virtual environment in the x-ecute/backend folder. 

If you haven't created an virtual environment in the x-ecute/backend folder, navigate to the x-ecute/backend folder and type:

```bash
python -m venv venv #if your keyword is python
```

or 

```bash
python3 -m venv venv #if your keyword is python3
```

To activate the Python virtual environment in the x-ecute/backend folder, navigate to the x-ecute/backend folder and type:

```bash
. venv/bin/activate # if you are using Mac
. venv/Scripts/activate #if you are using Windows
```

You should see a (venv) to the left of your terminal.

To install dependencies from requirements.txt, navigate to the x-ecute/backend and run:

```bash
pip install -r requirements.txt
```

## Running the server

To run the API server locally, navigate to the x-ecute/backend folder and run: 

```bash
python app.py
```

or 

```bash
python3 app.py
```

## Adding dependencies

If you want to add any dependncies / libraries / tools, follow these steps:
1. Ask the chat and have it approved
2. run `pip install <dependency>`
3. run `pip freeze > requirements.txt`