import tkinter as tk
from tkinter import PhotoImage
import cv2
import pygame
import SeguimientoManos as sm

def abrir_pagina1():
    ventana.destroy()

    # Código de Piano.py
    pygame.mixer.init()

    notes = {
        0: ("La", pygame.mixer.Sound("A.mp3")),
        1: ("Do", pygame.mixer.Sound("C.mp3")),
        2: ("Re", pygame.mixer.Sound("D.mp3")),
        3: ("Mi", pygame.mixer.Sound("E.mp3")),
        4: ("Fa", pygame.mixer.Sound("F.mp3")),
        5: ("Sol", pygame.mixer.Sound("G.mp3")),
    }

    detector = sm.detectormanos(Confdeteccion=0.75)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = detector.encontrarmanos(frame)


        manosInfo, cuadro = detector.encontrarposicion(frame, dibujar=False)

        if len(manosInfo) != 0:
            dedos = detector.dedosarriba()
            contar = dedos.count(1)
            if contar in notes:
                nota, sonido = notes[contar]
                sonido.play(maxtime=3000)  # Reproducir el sonido durante 3 segundos

                cv2.putText(frame, nota, (445, 375), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 25)

        cv2.imshow("Piano", frame)
        t = cv2.waitKey(1)
        if t == 27 or t == 113:  # Agregar la condición para la tecla "q"
            break

    cap.release()
    cv2.destroyAllWindows()
    crear_ventana_principal()


def abrir_pagina2():
    # Destruir la ventana principal
    ventana.destroy()

    # Código de Mouse.py
    import cv2
    import numpy as np
    import SeguimientoManos as sm
    import autopy

    anchocam, altocam = 640, 480
    cuadro = 100
    anchopanta, altopanta = autopy.screen.size()
    sua = 5
    pubix, pubiy = 0,0
    cubix, cubiy = 0,0

    cap = cv2.VideoCapture(0)
    cap.set(3,anchocam)
    cap.set(4,altocam)

    detector = sm.detectormanos(maxManos=1)

    while True:
        ret, frame = cap.read()
        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)

        if len(lista) != 0:
            x1, y1 = lista[8][1:]
            x2, y2 = lista[12][1:]

            dedos = detector.dedosarriba()
            cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)  # Generamos cuadro
            if dedos[1]== 1 and dedos[2] == 0:
                x3 = np.interp(x1, (cuadro,anchocam-cuadro), (0,anchopanta))
                y3 = np.interp(y1, (cuadro, altocam-cuadro), (0, altopanta))

                cubix = pubix + (x3 - pubix) / sua
                cubiy = pubiy + (y3 - pubiy) / sua

                autopy.mouse.move(anchopanta - cubix,cubiy)
                cv2.circle(frame, (x1,y1), 10, (0,0,0), cv2.FILLED)
                pubix, pubiy = cubix, cubiy

            if dedos[1] == 1 and dedos[2] == 1:
                longitud, frame, linea = detector.distancia(8,12,frame)
                if longitud < 30:
                    cv2.circle(frame, (linea[4],linea[5]), 10, (0,255,0), cv2.FILLED)
                    autopy.mouse.click()

        cv2.imshow("Mouse", frame)
        k = cv2.waitKey(1)
        if k == 27 or k == 113:  # Agregar la condición para la tecla "q"
            break

    cap.release()
    cv2.destroyAllWindows()

    # Recrear y mostrar la ventana principal
    crear_ventana_principal()

def crear_ventana_principal():
    global ventana

    ventana = tk.Tk()
    ventana.title("GesturePiano: Interacción Virtual con Música")
    ventana.geometry("600x400")

    imagen_fondo = PhotoImage(file="fondo.png")
    fondo_label = tk.Label(ventana, image=imagen_fondo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    boton1 = tk.Button(ventana, text="Programa Piano", command=abrir_pagina1, padx=20, pady=10, bg="#AEF3FF", fg="black")
    boton1.place(x=35, y=150)

    boton2 = tk.Button(ventana, text="Programa Mouse", command=abrir_pagina2, padx=20, pady=10, bg="#AEF3FF", fg="black")
    boton2.place(x=35, y=260)

    ventana.mainloop()

# Llamar a la función para crear la ventana principal al inicio del programa
crear_ventana_principal()