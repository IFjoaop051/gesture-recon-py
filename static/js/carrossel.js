// CARROSSEL DE HISTÓRIAS
const track = document.querySelector(".track");
let cards = document.querySelectorAll(".card");


// CLONA PRIMEIRO E ÚLTIMO CARD
const primeiro = cards[0].cloneNode(true);
const ultimo = cards[cards.length - 1].cloneNode(true);

track.appendChild(primeiro);
track.insertBefore(ultimo, track.firstChild);

// Atualiza lista dos cards
cards = document.querySelectorAll(".card");

// CONTROLE DA POSIÇÃO

// começa no primeiro card real
let posicao = 1;

// largura do card + espaço entre eles
const larguraCard =
    cards[0].offsetWidth + 20;

// posiciona inicialmente
track.style.transform = `translateX(-${posicao * larguraCard}px)`;

// MOVIMENTAÇÃO
function mover() {
    track.style.transition = "transform 0.4s ease";

    track.style.transform = `translateX(-${posicao * larguraCard}px)`;
}

// PRÓXIMA HISTÓRIA
function avancar() {
    posicao++;
    mover();

    // chegou no clone do primeiro card
    if (posicao === cards.length - 1) {
        setTimeout(() => {

            track.style.transition = "none";

            posicao = 1;

            track.style.transform = `translateX(-${posicao * larguraCard}px)`;

        }, 400);
    }
}

// HISTÓRIA ANTERIOR
function voltar() {
    posicao--;
    mover();

    // chegou no clone do último card
    if (posicao === 0) {
        setTimeout(() => {

            track.style.transition = "none";

            posicao = cards.length - 2;

            track.style.transform = `translateX(-${posicao * larguraCard}px)`;

        }, 400);
    }
}

// ABRIR HISTÓRIA ESCRITA
function abrirHistoria() {
    /* Como existem clones no carrossel: posição real começa em 1. Então subtraímos 1 para pegar o índice correto dos dados.*/

    const historiaAtual = posicao - 1;

    const link = cards[posicao].querySelector("a");

    if (link == null) {
        console.error("Failed to get referenced card at index #%d", posicao);
        return;
    }

    window.location.href = link.href;
}

// ABRIR VÍDEO DA HISTÓRIA
function abrirVideo() {

    // PEGA O CARD ATUAL
    const cardAtual = cards[posicao];

    // PEGA O LINK DA HISTÓRIA
    const linkHistoria = cardAtual.querySelector("a");

    if (!linkHistoria) {
        return;
    }

    // TRANSFORMA O LINK EM UMA URL
    const url = new URL(linkHistoria.href);

    // PEGA O ID DA MULHER
    const id = url.searchParams.get("id");

    if (!id) {
        return;
    }

    // ABRE A PÁGINA DO VÍDEO
    window.location.href = `/video.html?id=${id}`;
}


// DISPONIBILIZA PARA OUTROS JS
window.avancar = avancar;
window.voltar = voltar;
window.abrirHistoria = abrirHistoria;
window.abrirVideo = abrirVideo;