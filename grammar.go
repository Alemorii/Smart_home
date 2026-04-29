/* un programa podria ser 
if sensor_himo == on then 
	altavoz_comedor.mensaje = "PELIGRO"
comentarios no contemplados en gramatica
*/

//producciones nt 
<programa> -> <lista_instrucciones>

<lista_instrucciones> -> <instruccion> | <instruccion> <lista_instrucciones>

<instruccion> ->  <bloque_when> 
	|<bloque_every>
	|<bloque_if>
	|<asignacion> 

<bloque_when> -> <when> <condicion> <do> <lista_acciones> <end> 

<lista_acciones> -> <accion> | <accion> <lista_acciones>

<accion> -> <asignacion> | <bloque_if> 

<asignacion> -> <dispositivo> . <atributo>  = <valor> 
	|<dispositivo> . <atributo>  = <rango>

<bloque_every> -> <every> <tiempo> <do> <lista_acciones> <end> 

<bloque_if> -> <if> <condicion> <then> <lista_acciones> <else> <lista_acciones> <end>
	|<if> <condicion> <then> <lista_acciones> <end>

//producciones directas 
<dispositivo> -> foco_ 
	|aire_
	|persiana_
	|cerradura_
	|reloj_
	|altavoz_ 
	|alarma_

<atributo> -> estado
	|brillo 
	|color 
	|modo 
	|temp_obj
	|temp_act
	|posicion 
	|hora 
	|fecha 
	|volumen 
	|mute 
	|mensaje 
	|email_notif 
	|activada


<do>-> DO | do 
<when> -> WHEN| when 
<end> -> END | end 
<if> -> IF | if 
<then> -> THEN | then 
<else> -> ELSE | else 
<every> -> EVERY| every

