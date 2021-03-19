import json, os, sys

def cargar_escuelas():
    with open("escuelas.geojson") as f:
        datos = json.load(f)
        return datos["features"]
        
def contiene(nombre, palabra):
    return (nombre is not None) and (palabra in nombre)

def palabra_en_nombre(escuela, palabra):
    nombre_abreviado = escuela["properties"]["nombre_abr"]
    nombre_completo = escuela["properties"]["nombre_est"]
    return contiene(nombre_abreviado, palabra) or contiene(nombre_completo, palabra)
    
def misma_escuela(escuela, palabras):
    es_misma_escuela = True
    for palabra in palabras:
        if not palabra_en_nombre(escuela, palabra):
            es_misma_escuela = False
            
    return es_misma_escuela

def buscar_escuelas(lista_escuelas, palabras_buscadas):
    escuelas_encontradas = []
    for escuela in lista_escuelas:
        es_misma_escuela = True
        if misma_escuela(escuela, palabras_buscadas):
            escuelas_encontradas.append(escuela["properties"])
    return escuelas_encontradas

def main(argv):
    escuelas = cargar_escuelas()
    
    print("Ingresá las palabras por las que querés buscar:")
    palabras_buscadas = input().split(" ")
    print("Vas a buscar por las palabras", palabras_buscadas)
    
    escuelas_buscadas = buscar_escuelas(escuelas, palabras_buscadas)
    for escuela in escuelas_buscadas:
        print(escuela["cui"], "\t|",escuela["de"],"\t|", escuela["nombre_abr"], "\t|", escuela["nombre_est"])

if __name__=='__main__':
    main(sys.argv)
