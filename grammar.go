//producciones nt 
<programa> -> <lista_instrucciones>

<lista_instrucciones> -> <instruccion> | <instruccion> <lista_instrucciones>

<instruccion> ->  
	<bloque_when> 
	|<bloque_every>
	|<bloque_if>
	|<asignacion> 

<bloque_when> -> <when> <condicion> <do> <lista_acciones> <end> 

<bloque_every> -> <every> <tiempo> <do> <lista_acciones> <end> 

<bloque_if> ->	<if> <condicion> <then> <lista_acciones> <else> <lista_acciones> <end>
    |<if> <condicion> <then> <lista_acciones> <end>

<lista_acciones> -> <accion> | <accion> <lista_acciones> // condicionales a anidar

<accion> -> <asignacion> | <bloque_if> 

 // <actuador> . <atributo>  = <valor> //bindear cada actuador 
<asignacion> ->  
	<foco>.estado = TK_BOOL | <foco>.brillo = TK_PERCENT  | <foco>.color = TK_NOMBRE
	|<aire>.estado = TK_BOOL | <aire>.modo = TK_DISCRETO 	
	|<aire>.temp_obj = TK_TEMP 
	|<persiana>.posicion = TK_PERCENT
	|<cerradura>.estado = TK_BOOL 
	|<altavoz>.volumen = TK_PERCENT | <altavoz>.mute = TK_BOOL 
	|<altavoz>.mesaje = TK_TEXTO | <altavoz>.email_notif = TK_EMAIL 
	|<alarma>.estado = TK_BOOL | <alarma>.activada = TK_BOOL


// este seria el bloque if, condicion de sensores
//<sensor> <evaluacion> <valor> 

<condicion> -> <comp_sensor>
    | <comp_actuador>
    | <condicion> <logico> <condicion>
    | NOT <condicion>

<comp_sensor> -> sensor_temp <comparacion> TK_TEMP
    | sensor_humedad <comparacion> TK_PERCENT
    | sensor_luz <comparacion> TK_LUX
    | sensor_movimiento <comparacion> TK_BOOL
    | sensor_humo <comparacion> TK_BOOL

<comp_actuador> -> <reloj> . hora <comparacion> TK_TIME
    | <alarma> . estado <comparacion> TK_BOOL
    | <aire> . estado <comparacion> TK_BOOL
    | <aire> . temp_act <comparacion> TK_TEMP

//producciones directas 
//consideramos las palabras reservadas como parte de la gramatica
<do>-> DO | do 
<when> -> WHEN| when 
<end> -> END | end 
<if> -> IF | if 
<then> -> THEN | then 
<else> -> ELSE | else 
<every> -> EVERY| every

<comparacion> -> == |  != | < | > | >= | <= 
<logico> -> AND | OR 

<foco> -> foco_ TK_NOMBRE
<aire> -> aire_ TK_NOMBRE
<persiana> -> persiana_ TK_NOMBRE
<cerradura> -> cerradura_ TK_NOMBRE
<reloj> -> reloj_ TK_NOMBRE
<altavoz> -> altavoz_ TK_NOMBRE
<alarma> -> alarma_ TK_NOMBRE



