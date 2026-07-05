from datetime import datetime

class HtmlBuilder:

    def __init__(self):
        self.reset()

    def reset(self):
        self.sensores = []
        self.actuadores = {}
        self.emails = []

    # SENSORES

    def sensor(self, nombre, unidad):
        self.sensores.append({
            "nombre": nombre,
            "unidad": unidad
        })

    # ACTUADORES

    def actuador(self, nombre):
        if nombre not in self.actuadores:
            self.actuadores[nombre] = {}

    def atributo(self, actuador, nombre, valor):

        if actuador not in self.actuadores:
            self.actuadores[actuador] = {}

        self.actuadores[actuador][nombre] = valor

    # EMAIL

    def email(self, correo):
        self.emails.append(correo)

    # ERRORES (reservado)

    def error(self, error):
        pass

    def tiene_contenido(self):
        """True si el builder acumuló algo (sirve para saber si hay estado parcial)."""
        return bool(self.sensores or self.actuadores or self.emails)

    # ==========================
    # CONTENIDO (sin <html>/<head>/<body>)
    # ==========================

    def render_content(self):
        """
        Devuelve únicamente los bloques de sensores/actuadores/emails,
        sin el esqueleto del documento. Se puede llamar en cualquier
        momento (incluso con parseo incompleto) para obtener el estado
        parcial acumulado hasta ese punto.
        """

        html = []

        # Sensores

        for sensor in self.sensores:

            html.append(
                '<div style="border:1px solid green; padding:20px;">'
            )

            html.append(
                f"<h2>{sensor['nombre']}</h2>"
            )

            html.append(
                f"<p>{sensor['unidad']}</p>"
            )

            html.append("</div>")

        # Actuadores

        for nombre, atributos in self.actuadores.items():

            html.append(
                '<div style="border:1px solid gray; padding:20px;">'
            )

            html.append(
                f"<h1>{nombre}</h1>"
            )

            html.append("<ul>")

            for atributo, valor in atributos.items():

                if atributo == "email":

                    usuario = valor.split("@")[0]

                    html.append(
                        f'<li><a href="mailto:{valor}">Contactar a {usuario}</a></li>'
                    )

                else:

                    html.append(
                        f"<li>{atributo}: {valor}</li>"
                    )

            html.append("</ul>")
            html.append("</div>")

        # Emails independientes

        for correo in self.emails:

            usuario = correo.split("@")[0]

            html.append(
                f'<a href="mailto:{correo}">Contactar a {usuario}</a><br>'
            )

        return html

    # GENERACIÓN HTML (documento completo, caso éxito)

    def finish(self):

        html = []

        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append('<meta charset="UTF-8">')
        html.append("<title>Smart Home</title>")
        html.append("</head>")
        html.append("<body>")

        html.extend(self.render_content())

        html.append("</body>")
        html.append("</html>")

        return html


def generate_error_html(errors, output_file, partial_builder=None):
    """
    Genera un único HTML que muestra:
    1. El estado parcial reconocido por el parser antes de fallar
        si se pasa un `partial_builder` con contenido).
    2. La tabla de errores encontrados.

    Parameters
    ----------
    errors : list
        Lista de diccionarios con los errores.

    output_file : str
        Nombre del archivo HTML de salida.

    partial_builder : HtmlBuilder, optional
        Builder que contiene lo que el parser ya había reconocido
        (sensores/actuadores/emails) hasta el punto del error.
    """

    html = []

    html.append("<!DOCTYPE html>")
    html.append("<html lang='es'>")
    html.append("<head>")
    html.append('    <meta charset="UTF-8">')
    html.append("    <title>Errores encontrados</title>")
    html.append("    <style>")
    html.append("        body { font-family: Arial, sans-serif; margin:40px; }")
    html.append("        table { border-collapse: collapse; width:100%; }")
    html.append("        th, td { border:1px solid #ccc; padding:8px; }")
    html.append("        th { background:#f44336; color:white; }")
    html.append("        tr:nth-child(even) { background:#f2f2f2; }")
    html.append("        h1 { color:#d32f2f; }")
    html.append("        h1.parcial { color:#2e7d32; }")
    html.append("        hr { margin:30px 0; }")
    html.append("    </style>")
    html.append("</head>")
    html.append("<body>")

    # Estado parcial (lo que sí se pudo reconocer)

    if partial_builder is not None and partial_builder.tiene_contenido():

        html.append("<h1 class='parcial'>Estado parcial reconocido antes del error</h1>")
        html.extend(partial_builder.render_content())
        html.append("<hr>")

    # Errores

    html.append("<h1>Errores encontrados</h1>")

    html.append(f"<p>Total de errores: <b>{len(errors)}</b></p>")
    html.append(f"<p>Generado: {datetime.now()}</p>")

    html.append("<table>")
    html.append("<tr>")
    html.append("<th>#</th>")
    html.append("<th>Tipo</th>")
    html.append("<th>Línea</th>")
    html.append("<th>Columna</th>")
    html.append("<th>Lexema</th>")
    html.append("<th>Descripción</th>")
    html.append("</tr>")

    for i, error in enumerate(errors, start=1):

        html.append("<tr>")

        html.append(f"<td>{i}</td>")
        html.append(f"<td>{error.get('tipo','')}</td>")
        html.append(f"<td>{error.get('linea','')}</td>")
        html.append(f"<td>{error.get('columna','')}</td>")
        html.append(f"<td>{error.get('lexema','')}</td>")
        html.append(f"<td>{error.get('mensaje','')}</td>")

        html.append("</tr>")

        # Fila extra con el contexto de la línea y un puntero '^'
        # señalando la columna exacta del error (si el error trae esa info).
        contexto = error.get('contexto')
        puntero = error.get('puntero')

        if contexto:
            html.append("<tr>")
            html.append(
                f'<td colspan="6" style="background:#fff3f3;">'
                f'<pre style="margin:0; font-family:monospace;">'
                f'{contexto}\n{puntero}'
                f'</pre></td>'
            )
            html.append("</tr>")

    html.append("</table>")

    html.append("</body>")
    html.append("</html>")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(html))
