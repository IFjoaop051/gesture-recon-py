// PEGA O ID DA MULHER PELA URL
const parametros = new URLSearchParams(window.location.search);
const id = parametros.get("id");

// PROCURA A MULHER NO dados.js
const mulher = mulheres[id];

// ELEMENTOS DO VÍDEO
const video = document.getElementById("videoPrincipal");
const source = document.getElementById("videoSource");


// VERIFICA SE A MULHER EXISTE
if (!mulher) {

    document.body.innerHTML = `
        <div style="
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            font-family:Inter,sans-serif;
        ">
            <h1>Vídeo não encontrado</h1>
            <a href="/">Voltar para a galeria</a>
        </div>
    `;

}

// VERIFICA SE EXISTE VÍDEO PARA ESSA MULHER
else if (!mulher.video) {

    document.body.innerHTML = `
        <div style="
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
            flex-direction:column;
            font-family:Inter,sans-serif;
        ">
            <h1>Vídeo ainda não disponível</h1>
            <p>${mulher.nome}</p>
            <a href="/">Voltar para a galeria</a>
        </div>
    `;

}

else {

    document.title = `${mulher.nome} | Galeria de Histórias`;

    source.src = mulher.video;

    video.load();

    video.play()
        .catch((erro) => {
            console.log("Autoplay bloqueado:", erro);
        });

}