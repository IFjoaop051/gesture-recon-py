// CONEXÃO COM O SOCKET
const socket = io();

// ALTERAÇÃO: velocidade da rolagem contínua da página de história.
const SCROLL_SPEED = 8;

// A página de história entra no modo especial de rolagem.
// Nas outras páginas, os polegares continuam com o comportamento normal
// (próxima/anterior).
// ALTERAÇÃO: não usar "volatile" nesses comandos,
// pois o servidor precisa receber o modo corretamente.
if (window.location.pathname === "/historia.html") {
  socket.emit("scroll_mode_on");
} else {
  socket.emit("scroll_mode_off");
}

// RECEBE OS GESTOS DO PYTHON
socket.on("gesto", function (comando) {
    console.log("Gesto recebido:", comando);

    switch (comando) {

        // PRÓXIMA HISTÓRIA
        case "proxima":
            avancar();
            break;

        // HISTÓRIA ANTERIOR
        case "anterior":
            voltar();
            break;

        // ABRIR HISTÓRIA ESCRITA
        case "abrir_historia":
            abrirHistoria();
            break;

        // ABRIR VÍDEO
        case "abrir_video":
            abrirVideo();
            break;
        
        // ALTERAÇÃO: mão aberta ✋ controla Play/Pause do vídeo.
        case "play_video":
          if (window.location.pathname === "/video.html") {
              const video = document.getElementById("videoPrincipal");
              if (video) {
                  // ALTERAÇÃO:
                  // Mão aberta controla o áudio do vídeo.
                  video.muted = !video.muted;
                  if (!video.muted) {
                      video.volume = 1.0;
                      console.log("🔊 Áudio ligado.");
                  } else {
                      console.log("🔇 Áudio desligado.");
                  }
              }
          }
          break;

        // VOLTAR AO INÍCIO
        // ALTERAÇÃO: agora este comando é enviado pelo gesto ILoveYou (🤟).
        case "inicio":
            window.location.href = "/";
            break;
    }
});


// ============================================================
// ROLAGEM DA PÁGINA DE HISTÓRIA COM OS POLEGARES
// ============================================================

let scrollDir = 0;
let scrolling = false;

// O Python envia "up" para 👍 e "down" para 👎.
// Só funciona na página historia.html.
socket.on("scroll_start", direction => {
  if (window.location.pathname !== "/historia.html") {
    return;
  }

  if (direction === "up") {
    scrollDir = -1;
  } else if (direction === "down") {
    scrollDir = 1;
  } else {
    return;
  }

  if (!scrolling) {
    scrolling = true;
    scrollLoop();
  }
});

// Para a rolagem assim que o polegar deixa de ser reconhecido.
socket.on("scroll_stop", () => {
  scrollDir = 0;
  scrolling = false;
});

function scrollLoop() {
  if (!scrolling || scrollDir === 0) {
    return;
  }

  window.scrollBy({
    top: scrollDir * SCROLL_SPEED,
    left: 0,
    behavior: "auto"
  });

  requestAnimationFrame(scrollLoop);
}
