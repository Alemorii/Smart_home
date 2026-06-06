import ply.lex as lex
import sys

tokens = (
    'WHEN', 'EVERY', 'DO', 'END',
    'IF', 'THEN', 'ELSE',
    'AND', 'OR', 'NOT',
    'IGUAL', 'NOIGUAL', 'MAYORIGUAL', 'MAYOR', 'MENOR', 'MENORIGUAL',
    'ASIGNACION', 'PUNTO',
    # actuadores
    'FOCO', 'AIRE', 'PERSIANA', 'CERRADURA',
    'RELOJ', 'ALTAVOZ', 'ALARMA',
    # sensores
    'SENSOR_TEMP', 'SENSOR_HUMEDAD', 'SENSOR_LUZ',
    'SENSOR_MOVIMIENTO', 'SENSOR_HUMO',
    # atributos
    'ESTADO', 'BRILLO', 'COLOR', 'MODO',
    'TEMP_OBJ', 'TEMP_ACT', 'POSICION',
    'VOLUMEN', 'MUTE', 'MENSAJE', 'EMAIL_NOTIF',
    'ACTIVADA', 'HORA',
    # valores
    'BOOL', 'DISCRETO', 'NOMBRE',
    'PERCENT', 'TEMP', 'LUX', 'TIME',
    'EMAIL', 'TEXTO', 'TIEMPO',
)

# expresiones regulares de simbolos
t_IGUAL = r'=='
t_NOIGUAL = r'!='
t_MAYORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MAYOR = r'>'
t_MENOR = r'<'
t_ASIGNACION = r'='
t_PUNTO = r'\.'

t_ignore = ' \t'

# Expresiones regulares simples

def t_COMENTARIO(t):
    r'//[^\n]*'
    pass    # no revuelve nada

def t_WHEN(t):
    r'when\b|WHEN\b'  # el \b lo que hace es pararlo ahi y que si viene un whens, no tome como token when token s y lo tome como un nombre
    return t

def t_EVERY(t):
    r'every\b|EVERY\b'
    return t

def t_DO(t):
    r'do\b|DO\b'
    return t

def t_END(t):
    r'end\b|END\b'
    return t

def t_IF(t):
    r'if\b|IF\b'
    return t

def t_THEN(t):
    r'then\b|THEN\b'
    return t

def t_ELSE(t):
    r'else\b|ELSE\b'
    return t

def t_AND(t):
    r'AND\b'
    return t

def t_OR(t):
    r'OR\b'
    return t

def t_NOT(t):
    r'NOT\b'
    return t

# SENSORES
def t_SENSOR_TEMP(t):
    r'sensor_temp\b'
    return t

def t_SENSOR_HUMEDAD(t):
    r'sensor_humedad\b'
    return t

def t_SENSOR_LUZ(t):
    r'sensor_luz\b'
    return t

def t_SENSOR_MOVIMIENTO(t):
    r'sensor_movimiento\b'
    return t

def t_SENSOR_HUMO(t):
    r'sensor_humo\b'
    return t

# ACTUADORES
def t_FOCO(t):
    r'foco_[a-zA-Z0-9]+'
    return t

def t_AIRE(t):
    r'aire_[a-zA-Z0-9]+'
    return t

def t_PERSIANA(t):
    r'persiana_[a-zA-Z0-9]+'
    return t

def t_CERRADURA(t):
    r'cerradura_[a-zA-Z0-9]+'
    return t

def t_RELOJ(t):
    r'reloj_[a-zA-Z0-9]+'
    return t

def t_ALTAVOZ(t):
    r'altavoz_[a-zA-Z0-9]+'
    return t

def t_ALARMA(t):
    r'alarma_[a-zA-Z0-9]+'
    return t

# ATRIBUTOS
def t_TEMP_OBJ(t):
    r'temp_obj\b'
    return t

def t_TEMP_ACT(t):
    r'temp_act\b'
    return t

def t_EMAIL_NOTIF(t):
    r'email_notif\b'
    return t

def t_ESTADO(t):
    r'estado\b'
    return t

def t_BRILLO(t):
    r'brillo\b'
    return t

def t_COLOR(t):
    r'color\b'
    return t

def t_MODO(t):
    r'modo\b'
    return t

def t_POSICION(t):
    r'posicion\b'
    return t

def t_VOLUMEN(t):
    r'volumen\b'
    return t

def t_MUTE(t):
    r'mute\b'
    return t

def t_MENSAJE(t):
    r'mensaje\b'
    return t

def t_ACTIVADA(t):
    r'activada\b'
    return t

def t_HORA(t):
    r'hora\b'
    return t

# expresiones regulares compuestas

def t_BOOL(t):
    r'true\b|false\b|on\b|off\b|TRUE\b|FALSE\b|ON\b|OFF\b'
    return t

def t_DISCRETO(t):
    r'frio\b|calor\b|ventilacion\b'
    return t

def t_EMAIL(t):
    r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9._+-]+\.[a-zA-Z]{2,4}'  # sacás las comillas
    return t

def t_TEMP(t):
    r'-?[0-9]+(\.[0-9]+)?°[CF]'
    return t

def t_TIEMPO(t):
    r'[0-9]+(seg|min|hs)'
    return t

def t_TIME(t):
    r'[0-2][0-9]:[0-5][0-9]'
    return t

def t_LUX(t):
    r'[0-9]+(\.[0-9]+)?lux'
    return t

def t_PERCENT(t):
    r'[0-9]{1,3}%'
    t.value = int(t.value[:-1])
    return t

def t_TEXTO(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_NOMBRE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# logica de usuario

def procesar_archivo(file_name):  # lee archivo y muestra tokens
    try:
        with open(file_name, 'r', encoding='utf-8')as f:
            data = f.read()

        lexer.input(data)

        print(f"\n--- Analizando archivo: {file_name} ---")
        for tok in lexer:
            print(tok)
        print("Análisis léxico completo.")
    except FileNotFoundError:
        print("error, archivo no encontrado")


program = True
if __name__ == "__main__":
    while program == True:
        print("\n -- Bienvenidx al analizador lexico--")
        print("1. Procesar archivo en la carpeta actual")
        print("2. procesar tokens de texto")
        print("3. Salir")
        print('-' * 40)

        choice = input("Elige una opcion (1,2,3) :")

        match choice:
            case "1":
                file_name = input("introduzca el nombre del archivo :")
                procesar_archivo(file_name)
            case "2":
                data = input("ingrese texto a tokenizar :\n ")
                lexer.input(data)
                for tok in lexer:
                    print(tok)
                print("analisis lexico completo")
            case "3":
                sys.exit()
