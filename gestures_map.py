# Gestos reconhecidos pelo modelo padrão do MediaPipe.
# Ajuste estas associações se quiser trocar os comandos do site.
#
# ALTERAÇÃO: Closed_Fist foi substituído por ILoveYou para voltar ao início.
# Os polegares continuam no mapa porque, fora da página de história,
# eles continuam sendo usados para navegar entre os cards.
GESTURES_MAP = {
    "Thumb_Up": ["proxima"],
    "Thumb_Down": ["anterior"],
    "Pointing_Up": ["abrir_historia"],
    "Victory": ["abrir_video"],
    "ILoveYou": ["inicio"],

    # ALTERAÇÃO: mão aberta ✋ será usada para Play/Pause do vídeo.
    "Open_Palm": ["play_video"],
}