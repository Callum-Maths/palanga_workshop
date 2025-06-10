def response(row_number):
    import pandas as pd
    import requests

    row_number = int(row_number)  # Ensure row_number is an integer
    csv_file = "assets.csv"

    if row_number == 0:
        df = pd.read_csv(csv_file, nrows=1)
    else:
        df = pd.read_csv(csv_file, skiprows=range(1, row_number + 1), nrows=1)

    if df.empty:
        return "Error: Row not found", "Unknown"

    name = df.iloc[0]['name']
    description = df.iloc[0].get('description', '')

    if pd.isna(description) or str(description).strip() == "":
        return "No Description, Unknown, Unknown", name

    prompt = f"What are 3 genres for this TV show/film? Warning: There are multiple different languages.\n\nShow: {name}\nDescription: {description[:500]}\n\nGenres:\n"

    data = {
    "model": "gemma:2b",  # Change this line
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.3,  # Lower for more consistent categorization
        "num_predict": 40,   # Reduced tokens
        "top_p": 0.8
    }
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=data, timeout=90)
        result = response.json()
        return result.get("response", "Error, Error, Error").strip(), name
    except requests.exceptions.ReadTimeout:
        return "Timeout: Model took too long to respond", name
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama service", name
    except Exception as e:
        return f"Error: {str(e)}", name