import ply.yacc as yacc
from lexer import tokens, lexer
from html_generator import HtmlBuilder

builder = HtmlBuilder()

start = 'programa'

def p_programa(p):
    'programa : lista_instrucciones'

    p[0] = {
        "programa": p[1],
        "html": builder.finish()
    } 

def p_lista_instrucciones_una(p):
    'lista_instrucciones : instruccion'
    p[0] = [p[1]]

def p_lista_instrucciones_varias(p):
    'lista_instrucciones : instruccion lista_instrucciones'
    p[0] = [p[1]] + p[2]

def p_instruccion(p):
    '''instruccion : bloque_when 
                   | bloque_every 
                   | bloque_if 
                   | asignacion'''
    p[0] = p[1]

def p_bloque_when(p):
    'bloque_when : WHEN condicion DO lista_acciones END'
    p[0] = ('when', p[2], p[4])

def p_bloque_if(p):
    '''bloque_if : IF condicion THEN lista_acciones ELSE lista_acciones END 
                 | IF condicion THEN lista_acciones END
    '''
    if len(p) == 8:   # con ELSE
        p[0] = ('if', p[2], p[4], p[6])
    else:             # sin ELSE 
        p[0] = ('if', p[2], p[4])

def p_bloque_every(p):
    '''bloque_every : EVERY TIEMPO  DO  lista_acciones END'''
    p[0] = ('every', p[2], p[4])

def p_lista_acciones_una(p):
    'lista_acciones : accion'
    p[0] = [p[1]]

def p_lista_acciones_varias(p):
    'lista_acciones : accion lista_acciones'
    p[0] = [p[1]] + p[2]

def p_accion(p):
    '''accion : asignacion
               | bloque_if
    '''
    p[0] = p[1]

def p_asignacion_foco_estado(p):
    'asignacion : FOCO PUNTO ESTADO ASIGNACION BOOL'

    builder.actuador(p[1])
    builder.atributo(p[1], 'estado', p[5])

    p[0] = ('asign', p[1], 'estado', p[5])
    

def p_asignacion_foco_brillo(p):
    'asignacion : FOCO PUNTO BRILLO ASIGNACION PERCENT'

    builder.actuador(p[1])
    builder.atributo(p[1], 'brillo', p[5])

    p[0] = ('asign', p[1], 'brillo', p[5])

def p_asignacion_foco_color(p):
    'asignacion : FOCO PUNTO COLOR ASIGNACION NOMBRE'

    builder.actuador(p[1])
    builder.atributo(p[1], 'color', p[5])

    p[0] = ('asign', p[1], 'color', p[5])

def p_asignacion_aire_estado(p):
    'asignacion : AIRE PUNTO ESTADO ASIGNACION BOOL'

    builder.actuador(p[1])
    builder.atributo(p[1], 'estado', p[5])

    p[0] = ('asign', p[1], 'estado', p[5])

def p_asignacion_aire_modo(p):
    'asignacion : AIRE PUNTO MODO ASIGNACION DISCRETO'

    builder.actuador(p[1])
    builder.atributo(p[1], 'modo', p[5])

    p[0] = ('asign', p[1], 'modo', p[5])

def p_asignacion_aire_temp_obj(p):
    'asignacion : AIRE PUNTO TEMP_OBJ ASIGNACION TEMP'

    builder.actuador(p[1])
    builder.atributo(p[1], 'temp_obj', p[5])

    p[0] = ('asign', p[1], 'temp_obj', p[5])

def p_asignacion_persiana_posicion(p):
    'asignacion : PERSIANA PUNTO POSICION ASIGNACION PERCENT'

    builder.actuador(p[1])
    builder.atributo(p[1], 'posicion', p[5])

    p[0] = ('asign', p[1], 'posicion', p[5])

def p_asignacion_cerradura_estado(p):
    'asignacion : CERRADURA PUNTO ESTADO ASIGNACION BOOL'

    builder.actuador(p[1])
    builder.atributo(p[1], 'estado', p[5])

    p[0] = ('asign', p[1], 'estado', p[5])

def p_asignacion_altavoz_volumen(p):
    'asignacion : ALTAVOZ PUNTO VOLUMEN ASIGNACION PERCENT'

    builder.actuador(p[1])
    builder.atributo(p[1], 'volumen', p[5])

    p[0] = ('asign', p[1], 'volumen', p[5])

def p_asignacion_altavoz_mute(p):
    'asignacion : ALTAVOZ PUNTO MUTE ASIGNACION BOOL'

    builder.actuador(p[1])
    builder.atributo(p[1], 'mute', p[5])

    p[0] = ('asign', p[1], 'mute', p[5])

def p_asignacion_altavoz_mensaje(p):
    'asignacion : ALTAVOZ PUNTO MENSAJE ASIGNACION TEXTO'

    builder.actuador(p[1])
    builder.atributo(p[1], 'mensaje', p[5])

    p[0] = ('asign', p[1], 'mensaje', p[5])

def p_asignacion_altavoz_email(p):
    'asignacion : ALTAVOZ PUNTO EMAIL ASIGNACION CORREO'

    builder.email(p[5])

    p[0] = ('asign', p[1], 'email', p[5])

def p_asignacion_alarma_estado(p):
    'asignacion : ALARMA PUNTO ESTADO ASIGNACION BOOL'

    builder.actuador(p[1])
    builder.atributo(p[1], 'estado', p[5])

    p[0] = ('asign', p[1], 'estado', p[5])

def p_asignacion_alarma_activada(p):
    'asignacion : ALARMA PUNTO ACTIVADA ASIGNACION BOOL'

    builder.actuador(p[1])
    builder.atributo(p[1], 'activada', p[5])

    p[0] = ('asign', p[1], 'activada', p[5])

def p_condicion(p):
    'condicion : condicion_or'
    p[0] = p[1]

def p_condicion_or(p):
    '''condicion_or : condicion_or OR condicion_and
                    | condicion_and'''
def p_condicion_and(p): 
    '''condicion_and : condicion_and AND condicion_not
                    | condicion_not
    '''

def p_condicion_not(p):
    '''condicion_not : NOT condicion_not
                    | condicion_simple 
    '''

def p_condicion_simple(p):
    '''condicion_simple : comp_sensor
                        | comp_actuador'''

def p_comp_sensor(p):
    '''comp_sensor : SENSOR_TEMP comparacion TEMP
                   | SENSOR_HUMEDAD comparacion PERCENT
                   | SENSOR_LUZ comparacion LUX
                   | SENSOR_MOVIMIENTO comp_bool BOOL
                   | SENSOR_HUMO comp_bool BOOL'''
    
    builder.sensor(p[1], p[3])

    p[0] = (p[1], p[2], p[3])

def p_comp_actuador(p):
    '''comp_actuador : RELOJ PUNTO HORA comparacion TIME
                    | RELOJ PUNTO FECHA comparacion DATE
                    | ALARMA PUNTO ESTADO comp_bool BOOL
                    | AIRE PUNTO ESTADO comp_bool BOOL
                    | AIRE PUNTO TEMP_ACT comparacion TEMP
    '''
    builder.actuador(p[1])
    builder.atributo(p[1], p[3], p[5])

    p[0] = (p[1], p[3], p[4], p[5])

def p_comp_bool(p):
    '''comp_bool : IGUAL
                    | NOIGUAL
    '''
    p[0] = p[1]

def p_comparacion(p):
    '''comparacion : IGUAL
                   | NOIGUAL
                   | MAYOR
                   | MENOR
                   | MAYORIGUAL
                   | MENORIGUAL'''
    p[0] = p[1]

parser_errors = []

def _tokens_esperados():
    """
    Consulta la tabla LALR del parser en su estado actual para saber
    qué tokens hubiesen sido válidos en ese punto. Devuelve una lista
    de nombres de token (puede venir vacía si no se puede determinar).
    """
    try:
        estado_actual = parser.statestack[-1]
        acciones = parser.action.get(estado_actual, {})
        return sorted(t for t in acciones.keys() if t != 'error')
    except Exception:
        return []


def _contexto_linea(p):
    """
    Reconstruye la línea de texto donde ocurrió el error junto con
    un puntero '^' señalando la columna exacta del token conflictivo.
    """
    lexdata = p.lexer.lexdata
    inicio = lexdata.rfind('\n', 0, p.lexpos) + 1
    fin = lexdata.find('\n', p.lexpos)
    if fin == -1:
        fin = len(lexdata)

    linea_texto = lexdata[inicio:fin]
    columna = p.lexpos - inicio

    puntero = ' ' * columna + '^'

    return linea_texto, columna + 1, puntero


def p_error(p):

    if parser_errors:      # ya hay un error real registrado, ignoramos la cascada
        return

    if p:
        linea_texto, columna, puntero = _contexto_linea(p)
        esperados = _tokens_esperados()

        mensaje = f"Token inesperado '{p.value}' (tipo {p.type})"
        if esperados:
            mensaje += f". Se esperaba: {', '.join(esperados)}"

        parser_errors.append({
            "tipo": "Sintáctico",
            "linea": p.lineno,
            "columna": columna,
            "lexema": p.value,
            "contexto": linea_texto,
            "puntero": puntero,
            "esperados": esperados,
            "mensaje": mensaje
        })
    else:
        parser_errors.append({
            "tipo": "Sintáctico",
            "linea": None,
            "columna": None,
            "lexema": "EOF",
            "contexto": "",
            "puntero": "",
            "esperados": [],
            "mensaje": "Fin de archivo inesperado (¿falta cerrar un bloque con 'END'?)"
        })
parser = yacc.yacc()