# Evaluacion2

## Descripción

Programa en Python que consume la API REST de GraphHopper para calcular rutas entre un origen y un destino, como parte de una aplicación de apoyo a los visitantes de la Biblioteca Nacional.

El programa original fue modificado con las siguientes mejoras:

- Todos los textos de interacción con el usuario (solicitudes y respuestas) están en español.
- Las distancias se muestran con exactamente dos decimales.
- El usuario puede salir del programa ingresando `s` o `salir`.
- La narrativa del viaje (instrucciones paso a paso) se imprime en español.

Proyecto desarrollado para la Evaluación Parcial N° 2 de CUY6142 (Telepresencia y Entornos Innovadores de Colaboración Humana).

## Requisitos

- Python 3.10 o superior
- Librería `requests`:
```bash
  pip install requests
```
- Key del servicio de rutas GraphHopper, asignada en la variable `key` dentro de `rutas_graphhopper.py`

## Ejecución

```bash
python rutas_graphhopper.py
```

Ejemplo de uso: ingresar como origen `Melipilla` y como destino `Biblioteca Nacional`. Para terminar el programa, escribir `s` o `salir`.