// CONEXÃO COM O SOCKET
const socket = io();

// socket.on

// RECEBE OS GESTOS DO PYTHON
socket.volatile.on("gesto", function (comando) {
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

        // VOLTAR AO INÍCIO
        case "inicio":
            window.location.href = "/";
            break;
    }
});
