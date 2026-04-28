/* un programa podria ser 
if sensor_himo == on then 
	altavoz_comedor.mensaje = "PELIGRO"

*/
<programa> -> <lista_instrucciones>

<lista_instrucciones> -> <instruccion> | <instruccion> <lista_instrucciones>

<instruccion> ->  
	<bloque_when> 
	|<bloque_every>
	|<bloque_if>
	|<asignacion> 

<bloque_when> -> <when> <condicion> <do> <lista_acciones> <end> 

<lista_acciones> -> <accion> | <accion> <lista_acciones>
<accion> -> <asignacion> | <condicional> 

<asignacion> -> <dispositivo> . <atributo>  = <valor> | <rango>

<do>-> DO | do 
<when> -> WHEN| when 
<end> -> END | end 
