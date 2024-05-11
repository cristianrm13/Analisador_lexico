from flask import Flask, request, render_template
import ply.lex as lex

reserved = {
    'for': 'FOR',
    'do': 'DO',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
}

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'ID',
]+ list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
        t.description = f'Palabra reservada {t.type.lower()}'
    else:
        t.type = 'ID'
        t.description = 'Identificador'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.txt'):
                code = file.read().decode('utf-8')
            else:
                return "File type not supported"
        else:
            code = request.form['code']
        lexer.input(code)
        line_counter = 1
        tokens = []
        for token in lexer:
            tokens.append({'type': token.type, 'value': token.value, 'line': line_counter, 'description': token.description})
            if token.value in ['(', ')']:
                line_counter += 1
            else:
                words = token.value.split()
                line_counter += len(words)
        return render_template('index.html', tokens=tokens)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)