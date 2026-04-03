from pathlib import Path
import os
class Security:
    def __init__(self, workspace):
        self.workspace = workspace
        self.herramientas = {
            "edit_file": "y",
            "list_files_in_dir": "n",
            "read_file": "n"
        }
    
    def authorization(self, herramienta, path):
        if path != None:
            route = Path(os.path.join(self.workspace ,path)).is_relative_to(self.workspace)
        else: 
            route = True
        if route:
            if self.herramientas.get(herramienta, "no existe") == "y":
                danger = self.herramientas.get(herramienta, "no existe")
                permission = input("La herramienta es peligrosa precione Y para continuar con la ejecucion: ").strip().lower()
                if permission == "y":
                    danger = "peligroso"
                    return "authorized"
                elif permission == "n":
                    return "unauthorized"
                else:
                    return "No seleccionaste nada"
            elif self.herramientas.get(herramienta, "no existe") == "n":
                return "authorized"
            else:
                return "No hay herramientas selecionadas"
        else: 
            return "No podemos trabajar en esta carpeta no tengo autorizacion"