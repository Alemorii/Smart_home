import ply.yacc as yacc
from lexer import tokens, lexer

start = 'programa'

def p_programa(p):
    'programa : lista_instrucciones'
    p[0] = p[1]

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
    '''accion : asignacion'''
    p[0] = p[1]

def p_asignacion_foco_estado(p):
    'asignacion : FOCO PUNTO ESTADO ASIGNACION BOOL'
    p[0] = ('asign', p[1], 'estado', p[5])

def p_asignacion_foco_brillo(p):
    'asignacion : FOCO PUNTO BRILLO ASIGNACION PERCENT'
    p[0] = ('asign', p[1], 'brillo', p[5])

def p_asignacion_foco_color(p):
    'asignacion : FOCO PUNTO COLOR ASIGNACION NOMBRE'
    p[0] = ('asign', p[1], 'color', p[5])

def p_condicion(p):
    '''condicion : comp_sensor'''
    p[0] = p[1]

def p_comp_sensor(p):
    '''comp_sensor : SENSOR_TEMP comparacion TEMP
                   | SENSOR_HUMEDAD comparacion PERCENT
                   | SENSOR_LUZ comparacion LUX
                   | SENSOR_MOVIMIENTO comparacion BOOL
                   | SENSOR_HUMO comparacion BOOL'''
    p[0] = (p[1], p[2], p[3])

def p_comparacion(p):
    '''comparacion : IGUAL
                   | NOIGUAL
                   | MAYOR
                   | MENOR
                   | MAYORIGUAL
                   | MENORIGUAL'''
    p[0] = p[1]

 
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis: fin de archivo inesperado")


parser = yacc.yacc()

if __name__ == "__main__":
    data = input(" ")
    lexer.lineno = 1
    resultado = parser.parse(data, lexer=lexer)
    print("Parseo:", resultado)
