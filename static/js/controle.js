// CONEXÃO COM O SOCKET
const socket = io();

const SCROLL_SHIFT = 8;

// socket.on


if (window.location.pathname === "/historia.html") {
  socket.volatile.emit("scroll_mode_on");
} else {
  socket.volatile.emit("scroll_mode_off");
}

// RECEBE OS GESTOS DO PYTHON
socket.volatile.on("gesto", function (comando) {
  console.log("Gesto recebido:", comando);

  if (window.location.pathname === "/historia.html") {
    switch (comando) {
      case "inicio": {
        window.location.href = "/";
      } break;
    }

    return;
  }

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

    // VOLTAR AO INÍCIO
    case "inicio":
      window.location.href = "/";
      break;
  }
});


let scrollDir = 0;
let scrolling = false;


socket.volatile.on("scroll_start", direction => {
  if (direction === "up") {
    scrollDir = -1;
  }

  if (direction === "down") {
    scrollDir = 1;
  }

  if (!scrolling) {
    scrolling = true;
    scrollLoop();
  }
});


socket.volatile.on("scroll_stop", () => {
  scrollDir = 0;
  scrolling = false;
});


function scrollLoop() {
  if (!scrolling || scrollDir === 0)
    return;

  window.scrollBy({
    left: 0,
    top: scrollDir * SCROLL_SHIFT,
    behavior: "smooth", // May "instant"
  });

  requestAnimationFrame(scrollLoop);
}
