# Federal Institute of Education, Science and Technology
# of State of Santa Catarina.
#
# Copyright (c) 2026 Pagani from IFSC Xanxerê. All rights reserved.
#
# This file was published under the AGPL-3.0-only license, 
# You can read it from "LICESE" file in the repository root.
#
# (filename:main.py)
# (project_code:gesture-recon-py)
# (project_name:"Reconhecimento de Gestos com Python")
# (scope:"Projeto Avaliativo Trimestral para a disciplina 'Tópicos Avançados em Informática'")


if __name__ != "__main__":
  # Termina a execução do programa se estiver em
  # uma `thread` de trabalho ao invés da principal
  # com o código POSIX `EPRM` (operação não permitida)

  from sys import exit
  exit(-4048)



import cv2
import mediapipe as mp
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from webbrowser import open as open_webb

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from constants import EXPECTED_PORT, CONFIDENCE, GESTURE_HOLD_TIME
from gestures_map import GESTURES_MAP

APP = Flask(__name__)
APP.config["SECRET"] = "secret!"

SIO = SocketIO(
  APP,
  logger=True,
  engineio_logger=True,
  cors_allowed_origins=[
    "http://localhost:%d" % EXPECTED_PORT,
    "http://127.0.0.1:%d" % EXPECTED_PORT,
  ],
)


@APP.get("/")
def serve_index():
  return render_template("cardsCarrossel.html")

@APP.get("/historia.html")
def serve_history():
  return render_template("historia.html")

@APP.get("/video.html")
def serve_video():
  return render_template("video.html")



in_infinite_scroll_mode = False

@SIO.on("scroll_mode_on")
def handle_scroll_mode_on() -> None:
  global in_infinite_scroll_mode
  in_infinite_scroll_mode = True

@SIO.on("scroll_mode_off")
def handle_scroll_mode_off() -> None:
  global in_infinite_scroll_mode
  in_infinite_scroll_mode = False



def worker() -> None:
  """
  Utiliza um modelo de ML pré-treinado e publicado pelo Google LLC.

  Obs.: O modelo pré-treinado não acompanha este repositório.
  Se precisar baixá-lo, procure no site oficial do Google (link abaixo).

  - Modelo Pré-treinado: https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task
  - Exemplo no Colab: https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/gesture_recognizer/python/gesture_recognizer.ipynb
  - Mais informações no artigo: https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer/python
  """
  base_options = python.BaseOptions(model_asset_path="model_tasks/gesture_recognizer.task")


  # Opções padrão para detecção de gestos de apenas
  # uma mão em vídeo, com nível de confiança 50%.
  options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    # model_complexity=0,
    min_hand_detection_confidence=CONFIDENCE,
    min_hand_presence_confidence=CONFIDENCE,
    min_tracking_confidence=CONFIDENCE
  )

  # Inicia a primeira câmera disponível.
  # Se o computador tiver mais de uma, selecione aqui.
  cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

  cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

  ignored_frames = 0
  frame_id = 0
  last_gesture = None
  candidate_since = 0
  candidate_gesture = None
  global in_infinite_scroll_mode

  with vision.GestureRecognizer.create_from_options(options) as recon:
    # Aqui, a função [vision/create_from_options()] carrega e
    # inicializa o modelo de ML, assim como prepara o ambiente (CPU/GPU)
    # para processar o vídeo e detectar gestos em tempo real.

    # Open browser when camera is ready
    open_webb("http://localhost:%d/" % EXPECTED_PORT, 2)

    while cap.isOpened():
      t0 = time.perf_counter()
      success, frame = cap.read()
      t1 = time.perf_counter()

      if not success: # Ignora frames vazios ao invés que "quebrar" o programa
        print("Ignoring empty camera frame #%d...", ignored_frames + 1)
        ignored_frames = ignored_frames + 1
        
        continue

      frame = cv2.flip(frame, 1)
      rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      t2 = time.perf_counter()

      # Codifica os pixels do frame atual em um formato que
      # a biblioteca 'MediaPipe' consegue entender e processar
      mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
      t3 = time.perf_counter()

      frame_id += 1 # 304

      # Envia o frame para o modelo que irá reconhecer o possível gesto
      result = recon.recognize_for_video(mp_img, frame_id)
      t4 = time.perf_counter()

      print(
        "read:", t1-t0,
        "convert:", t2-t1,
        "image:", t3-t2,
        "recognize:", t4-t3
      )

      if result.gestures:

        # Escolhe o gesto mais provável. O 'MediaPipe' retorna uma lista
        # com possíveis gestos, do mais provável para o menos provável
        top_gesture = result.gestures[0][0]

        gesture_name = top_gesture.category_name
        confidence = top_gesture.score

        if confidence > 0.5 and gesture_name in GESTURES_MAP:
          now = time.monotonic()

          if gesture_name != candidate_gesture:
            candidate_gesture = gesture_name
            candidate_since = now
          elif now - candidate_since >= GESTURE_HOLD_TIME:
            if in_infinite_scroll_mode:

              if gesture_name == "Thumb_Up":
                if last_gesture != "Thumb_Up":
                  SIO.emit("scroll_start", "up")
                  last_gesture = "Thumb_Up"
              elif gesture_name == "Thumb_Down":
                if last_gesture != "Thumb_Down":
                  SIO.emit("scroll_start", "start")
                  last_gesture = "Thumb_Down"
              else:
                if last_gesture in ("Thumb_Up", "Thumb_Down"):
                  SIO.emit("scroll_stop")

                last_gesture = None

            else:
              if gesture_name != last_gesture:
                for gesture in GESTURES_MAP[gesture_name]:
                  SIO.emit("gesto", gesture)
                  print("Sending `gesture_action=%s`" % gesture)

              last_gesture = gesture_name
        else:
          candidate_since = 0
          candidate_gesture = None
          last_gesture = None

        text = f"Gesture {gesture_name} ({confidence:.2f})"
        
        cv2.putText(
          frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
          1, (0, 255, 0), 2, cv2.LINE_AA
        )
        
        cv2.imshow("MediaPipe Gesture Recognition", frame)

        # Fecha a câmera e sai do loop ao pressionar a tecla "ESC"
        if cv2.waitKey(5) & 0xFF == 27:
          break


  cap.release()
  cv2.destroyAllWindows()


SIO.start_background_task(worker)
SIO.run(APP, port=EXPECTED_PORT)