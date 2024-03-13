import cv2
import pygame
import SeguimientoManos as sm

# Inicializar pygame
pygame.mixer.init()

# Definir las notas y los sonidos correspondientes
notes = {
    0: ("La", pygame.mixer.Sound("A.mp3")),
    1: ("Do", pygame.mixer.Sound("C.mp3")),
    2: ("Re", pygame.mixer.Sound("D.mp3")),
    3: ("Mi", pygame.mixer.Sound("E.mp3")),
    4: ("Fa", pygame.mixer.Sound("F.mp3")),
    5: ("Sol", pygame.mixer.Sound("G.mp3")),
}

detector = sm.detectormanos(Confdeteccion=0.6)
cap = cv2.VideoCapture(0)
cap.set(3, 480)  # Ancho
cap.set(4, 320)  # Alto

while True:
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame)
    cv2.rectangle(frame, (420,225), (570, 425), (0, 0, 0), cv2.FILLED)

    cv2.putText(frame, "Dedos", (425, 420), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)

    manosInfo, cuadro = detector.encontrarposicion(frame, dibujar=False)

    if len(manosInfo) != 0:
        dedos = detector.dedosarriba()
        contar = dedos.count(1)
        if contar in notes:
            # Obtener la nota y reproducir el sonido correspondiente
            nota, sonido = notes[contar]
            sonido.play(maxtime=3000)  # Reproducir el sonido durante 3 segundos

            # Mostrar la nota en el frame
            cv2.putText(frame, nota, (445, 375), cv2.FONT_HERSHEY_PLAIN, 10, (0, 255, 0), 25)
            print(f'Nota reconocida: {nota}')
    cv2.imshow("Contando dedos", frame)
    t = cv2.waitKey(1)
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()
