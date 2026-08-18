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

from constants import EXPECTED_PORT, CONFIDENCE_THRESHOLD, GESTURE_HOLD_TIME
from gestures_map import GESTURES_MAP


APP = Flask(__name__)


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


# ============================================================
# ALTERAÇÃO:
# Controla se estamos dentro da página de história.
# Quando estiver ativo, os polegares controlam a rolagem.
# ============================================================

in_infinite_scroll_mode = False


@SIO.on("scroll_mode_on")
def handle_scroll_mode_on() -> None:
  global in_infinite_scroll_mode

  in_infinite_scroll_mode = True

  print("Modo de rolagem ATIVADO")


@SIO.on("scroll_mode_off")
def handle_scroll_mode_off() -> None:
  global in_infinite_scroll_mode

  in_infinite_scroll_mode = False

  # ALTERAÇÃO:
  # Se sair da história, garante que qualquer rolagem seja parada.
  SIO.emit("scroll_stop")

  print("Modo de rolagem DESATIVADO")


def worker() -> None:
  base_options = python.BaseOptions(
    model_asset_path="model_tasks/gesture_recognizer.task"
  )


  options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=CONFIDENCE_THRESHOLD,
    min_hand_presence_confidence=CONFIDENCE_THRESHOLD,
    min_tracking_confidence=CONFIDENCE_THRESHOLD
  )


  # ============================================================
  # CÂMERA
  # ============================================================

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

    # Abre o navegador quando a câmera estiver pronta.
    open_webb("http://localhost:%d/" % EXPECTED_PORT, 2)


    while cap.isOpened():
      t0 = time.perf_counter()
      success, frame = cap.read()
      t1 = time.perf_counter()


      if not success:
        print(
          "Ignoring empty camera frame #%d...",
          ignored_frames + 1
        )

        ignored_frames += 1

        continue


      # ============================================================
      # ALTERAÇÃO:
      # A câmera NÃO é mais espelhada.
      #
      # Antes:
      # frame = cv2.flip(frame, 1)
      #
      # Agora:
      # usamos o frame original.
      # ============================================================

      rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
      )

      t2 = time.perf_counter()


      mp_img = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
      )

      t3 = time.perf_counter()


      frame_id += 1


      result = recon.recognize_for_video(
        mp_img,
        frame_id
      )

      t4 = time.perf_counter()


      print(
        "read:", t1 - t0,
        "convert:", t2 - t1,
        "image:", t3 - t2,
        "recognize:", t4 - t3
      )


      # ============================================================
      # GESTO RECONHECIDO
      # ============================================================

      if result.gestures:

        top_gesture = result.gestures[0][0]

        gesture_name = top_gesture.category_name
        confidence = top_gesture.score


        if confidence > CONFIDENCE_THRESHOLD and gesture_name in GESTURES_MAP:

          now = time.monotonic()


          # --------------------------------------------------------
          # Detecta mudança do gesto
          # --------------------------------------------------------

          if gesture_name != candidate_gesture:

            candidate_gesture = gesture_name
            candidate_since = now


          # --------------------------------------------------------
          # Gesto permaneceu tempo suficiente
          # --------------------------------------------------------

          elif now - candidate_since >= GESTURE_HOLD_TIME:


            # ======================================================
            # PRIORIDADE MÁXIMA: SAIR DA HISTÓRIA
            # ======================================================
            #
            # 🤟 ILoveYou sempre tem prioridade.
            #
            # Mesmo se estiver rolando a história, esse gesto
            # NÃO será confundido com rolagem.
            # ======================================================

            if gesture_name == "ILoveYou":

              if last_gesture != "ILoveYou":

                # ALTERAÇÃO:
                # ILoveYou -> voltar para o início.
                SIO.emit("gesto", "inicio")

                print(
                  "Sending `gesture_action=inicio` "
                  "(PRIORIDADE)"
                )

              last_gesture = "ILoveYou"


            # ======================================================
            # MODO HISTÓRIA
            # ======================================================

            elif in_infinite_scroll_mode:


              # ----------------------------------------------------
              # 👍 ROLAR PARA CIMA
              # ----------------------------------------------------

              if gesture_name == "Thumb_Up":

                if last_gesture != "Thumb_Up":

                  # ALTERAÇÃO:
                  # inicia rolagem para cima.
                  SIO.emit(
                    "scroll_start",
                    "up"
                  )

                  print(
                    "Scroll START -> UP"
                  )

                  last_gesture = "Thumb_Up"


              # ----------------------------------------------------
              # 👎 ROLAR PARA BAIXO
              # ----------------------------------------------------

              elif gesture_name == "Thumb_Down":

                if last_gesture != "Thumb_Down":

                  # ALTERAÇÃO:
                  # inicia rolagem para baixo.
                  SIO.emit(
                    "scroll_start",
                    "down"
                  )

                  print(
                    "Scroll START -> DOWN"
                  )

                  last_gesture = "Thumb_Down"


              # ----------------------------------------------------
              # Outro gesto dentro da história
              # ----------------------------------------------------

              else:

                # ALTERAÇÃO:
                # se estava rolando e mudou para outro gesto,
                # manda parar.
                if last_gesture in (
                  "Thumb_Up",
                  "Thumb_Down"
                ):

                  SIO.emit("scroll_stop")

                  print(
                    "Scroll STOP"
                  )


                last_gesture = None


            # ======================================================
            # FORA DA HISTÓRIA
            # ======================================================

            else:

              if gesture_name != last_gesture:
                for gesture in GESTURES_MAP[gesture_name]:
                  SIO.emit(
                    "gesto",
                    gesture
                  )

                  print("Sending `gesture_action=%s`" % gesture)


              last_gesture = gesture_name


        else:

          # ========================================================
          # ALTERAÇÃO:
          # Gesto perdeu confiança.
          #
          # Se estava usando o polegar para rolar,
          # interrompe imediatamente.
          # ========================================================

          if in_infinite_scroll_mode and last_gesture in ("Thumb_Up", "Thumb_Down") :
            SIO.emit("scroll_stop")
            print("Scroll STOP -> gesto perdido")


          candidate_since = 0
          candidate_gesture = None
          last_gesture = None


        # ==========================================================
        # MOSTRA O GESTO NA JANELA DA CÂMERA
        # ==========================================================

        text = (
          f"Gesture "
          f"{gesture_name} "
          f"({confidence:.2f})"
        )


        cv2.putText(
          frame,
          text,
          (20, 50),
          cv2.FONT_HERSHEY_SIMPLEX,
          1,
          (0, 255, 0),
          2,
          cv2.LINE_AA
        )


      # ==========================================================
      # NENHUM GESTO DETECTADO
      # ==========================================================

      else:

        # ALTERAÇÃO:
        # Sem gesto = parar a rolagem.
        if ( in_infinite_scroll_mode and last_gesture in ("Thumb_Up", "Thumb_Down") ):
          SIO.emit("scroll_stop")
          print("Scroll STOP -> nenhuma mão detectada")


        candidate_since = 0
        candidate_gesture = None
        last_gesture = None

      cv2.imshow("MediaPipe Gesture Recognition", frame)


      # ESC fecha o programa.
      if cv2.waitKey(5) & 0xFF == 27:
        break


  cap.release()

  cv2.destroyAllWindows()


# ============================================================
# INICIA SERVIDOR
# ============================================================

SIO.start_background_task(worker)

SIO.run(
  APP,
  port=EXPECTED_PORT
)