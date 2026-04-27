<programa> -> <instruccion> // un programa puede ser una sola instruccion
/* un programa podria ser 
if sensor_himo == on then 
	altavoz_comedor.mensaje = "PELIGRO"

*/

<instruccion> ->  
	<when> 
	|<every>
	|<condicional>
	|<asignacion> 

<WHEN> -> <when> <statement> <DO> 

<statement> -> <sensor> <literal> 
<when> -> when | WHEN