import os

from lexer import lexer, lexer_errors
from parser import parser, parser_errors, builder
from html_generator import generate_error_html

import sys


def elegir_archivo():
    """
    Abre un selector de archivos nativo (tkinter) filtrado por smart
    """
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()          # no queremos la ventana principal, solo el diálogo
        root.attributes('-topmost', True)

        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo .smart",
            initialdir=os.getcwd(),
            filetypes=[("Archivos Smart Home", "*.smart"), ("Todos los archivos", "*.*")]
        )

        root.destroy()

        return file_path if file_path else None

    except Exception as e:
        print(f"No se pudo abrir el selector gráfico ({e}).")
        return None


# lee archivo
def procesar_archivo(file_name):

    # Reseteamos estado por cada corrida (antes esto solo pasaba
    # una vez a nivel de módulo, y arrastraba datos entre archivos).
    builder.reset()
    lexer_errors.clear()
    parser_errors.clear()
    lexer.lineno = 1

    try:
        with open(file_name, 'r', encoding='utf-8')as f:
            data = f.read()

        lexer.input(data)

        print(f"\n--- Analizando archivo: {file_name} ---")
        for tok in lexer:
            #print(tok)
            print(tok.type, tok.value, tok.lineno)

        # controlamos si tenemos error en el proceso
        if lexer_errors:

            print("\nErrores léxicos encontrados:\n")

            for err in lexer_errors:
                print(
                    f"Línea {err['linea']}: "
                    f"{err['mensaje']}"
                    f"('{err['lexema']}')"
                )
            return {
                "success": False,
                "errors": lexer_errors,
                "data": None
            }

        # reseteamos la linea del lexer
        lexer.lineno = 1

        result = parser.parse(data, lexer=lexer,)

        if parser_errors:

            print("\nErrores sintácticos encontrados:\n")

            for err in parser_errors:

                print(
                    f"Línea {err['linea']}: "
                    f"{err['mensaje']} "
                    f"('{err['lexema']}')"
                )

            return {
                "success": False,
                "errors": parser_errors,
                "data": None
            }

        print("\nPrograma correcto.")

        return {
            "success": True,
            "errors": [],
            "data": result
        }

    except FileNotFoundError:
        errors = [{
            "tipo": "Ejecución",
            "linea": "-",
            "lexema": file_name,
            "mensaje": "El archivo no existe."
        }]

        output = file_name.replace(".smart", "_error.html")

        generate_error_html(errors, output)

        return None

def procesar_texto(data):
    builder.reset()
    lexer_errors.clear()
    parser_errors.clear()

    lexer.lineno = 1

    # Verificamos que el usuario haya ingresado texto
    if not data.strip():

        return {
            "success": False,
            "errors": [{
                "tipo": "Ejecución",
                "linea": "-",
                "lexema": "",
                "mensaje": "No se ingresó ningún texto."
            }],
            "data": None
        }

    lexer.input(data)

    print("\n--- Analizando entrada interactiva ---")

    for tok in lexer:
        # print(tok)
        print(tok.type, tok.value, tok.lineno)

    if lexer_errors:

        print("\nErrores léxicos encontrados:\n")

        for err in lexer_errors:
            print(
                f"Línea {err['linea']}: "
                f"{err['mensaje']}"
            )

        return {
            "success": False,
            "errors": lexer_errors,
            "data": None
        }

    lexer.lineno = 1

    result = parser.parse(data, lexer=lexer)

    if parser_errors:

        print("\nErrores sintácticos encontrados:\n")

        for err in parser_errors:

            print(
                f"Línea {err['linea']}: "
                f"{err['mensaje']} "
            )

        return {
            "success": False,
            "errors": parser_errors,
            "data": None
        }

    print("\nPrograma correcto.")

    return {
        "success": True,
        "errors": [],
        "data": result
    }

# EJECUCION DEL PROGRAMA

program = True

if __name__ == "__main__":

    while program == True:
        print("\n -- Bienvenido al analizador lexico--")
        print("1. Selecionar archivo a parsear")
        print("2. procesar tokens de texto")
        print("3. Salir")
        print("recuerde que el archivo de texto debe estar en la carpeta actual")
        print('-' * 40)

        choice = input("Elige una opcion (1,2,3) :")

        match choice:
            case "1":
                print("Abriendo selector de archivos...")
                file_name = elegir_archivo()

                if not file_name:
                    # tkinter no disponible, o el usuario cerró el diálogo
                    # sin elegir nada: dejamos la vía manual como respaldo.
                    file_name = input(
                        "No se seleccionó ningún archivo. "
                        "Introduzca el nombre manualmente (o Enter para cancelar): "
                    )

                if not file_name:

                    errors = [{
                        "tipo": "Ejecución",
                        "linea": "-",
                        "lexema": "",
                        "mensaje": "No se especificó ningún archivo."
                    }]

                    generate_error_html(errors, "error.html")
                    continue

                if not file_name.lower().endswith(".smart"):

                    errors = [{
                        "tipo": "Ejecución",
                        "linea": "-",
                        "lexema": file_name,
                        "mensaje": "La extensión del archivo debe ser .smart."
                    }]

                    output = file_name.rsplit(".", 1)[0] + "_error.html"
                    generate_error_html(errors, output)

                    continue

                result = procesar_archivo(file_name)

                if result is None:
                    # FileNotFoundError ya generó su propio HTML de error
                    continue

                if result["success"]:

                    output = file_name.replace(".smart", ".html")

                    with open(output, "w", encoding="utf-8") as f:
                        f.write("\n".join(result["data"]["html"]))

                    print("HTML generado correctamente.")

                else:

                    output = file_name.replace(".smart", "_error.html")

                    # Pasamos el builder para que se incluya todo lo que
                    # el parser ya había reconocido antes del error.
                    generate_error_html(
                        result["errors"],
                        output,
                        builder
                    )

                    print("Se generó el HTML con el estado parcial y los errores encontrados.")

                print ("Resultado del parser:", result)

            case "2":
                data = input("ingrese texto a tokenizar :\n ")

                result = procesar_texto(data)

                if result["success"]:

                    output = "interactive.html"

                    with open(output, "w", encoding="utf-8") as f:
                        f.write("\n".join(result["data"]["html"]))

                    print(f"HTML generado correctamente: {output}")

                else:

                    print("Se encontraron errores.")

                    output = "interactive_error.html"

                    generate_error_html(
                        result["errors"],
                        output,
                        builder
                    )

                    print(f"Se encontraron {len(result['errors'])} errores.")
                    print(f"HTML de errores generado (con estado parcial): {output}")

            case "3":
                sys.exit()
