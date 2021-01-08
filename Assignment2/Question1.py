from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/<name>")
def generateResponse(name=""):
    if len(name) > 0:
        if has_symbol(name):
            name = remove_symbols(name)
        else:
            name = upper_lower(name)
    return "Welcome " + name + " to my CSCB20 website!"

def has_symbol(string):
    result = False
    for char in string:
        if not char.isalpha():
            result = True
    return result

def remove_symbols(string):
    result = ""
    for char in string:
        if char.isalpha():
            result += char
    return result

def upper_lower(string):
    result = ""
    if string[0].isupper():
        result = string.lower()
    else:
        result = string.upper()
    return result

if __name__ == "__main__":
    app.run(debug=True)