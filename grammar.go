/* un programa podria ser 
if sensor_humo == on then 
	altavoz_comedor.mensaje = "PELIGRO"
comentarios no contemplados en gramatica
*/

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
	foco_.estado = Tk_bool | foco_.brillo = Tk_percent  | foco_.color = Tk_nombre
	|aire_.estado = TK_bool | aire_.modo = Tk_discreto 	
	|aire_.temp_obj = Tk_temp | aire.temp_act = Tk_temp //temp actual no deberia poder asignarse
	|persiana_.posicion = Tk_percent
	|cerradura_.estado = Tk_bool 
	|reloj_.hora = Tk_time | reloj_.hora = Tk_fecha // reloj es de solo lectura asi que no deberia ser asignado
	|altavoz_.volumen = Tk_percent | altavoz_.mute = Tk_Bool 
	|altavoz_.mesaje = Tk_texto | altavoz_.email_notif = Tk_email 
	|alarma_.estado = Tk_Bool | alarma.activada = Tk_Bool

// este seria el bloque if, condicion de sensores
//<sensor> <evaluacion> <valor> 

// duda clave : ya que el actuador reloj y temp_act son solo lectura los tratamos como sensores?
<condicion> -> 
	sensor_temp <comparacion> Tk_temp | sensor_humedad <comparacion> tk_temp <logico> <condicion>
	|sensor_humedad <comparacion> Tk_lux |sensor_humedad <comparacion> Tk_lux <logico> <condicion>
	|sensor_movimiento <comparacion> Tk_Bool | sensor_humedad <comparacion> Tk_lux <condicion>
	|sensor_humo <comparacion> Tk_Bool | sensor_humedad <comparacion> Tk_lux <condicion>

//producciones directas 
<do>-> DO | do 
<when> -> WHEN| when 
<end> -> END | end 
<if> -> IF | if 
<then> -> THEN | then 
<else> -> ELSE | else 
<every> -> EVERY| every

<comparacion> -> == |  != | < | > | >= | <= 
<condicion> -> AND | OR | NOT 


