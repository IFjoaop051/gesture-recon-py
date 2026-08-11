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
function mover(){
    track.style.transition = "transform 0.4s ease";

    track.style.transform = `translateX(-${posicao * larguraCard}px)`;
}

// PRÓXIMA HISTÓRIA
function avancar(){
    posicao++;
    mover();

    // chegou no clone do primeiro card
    if(posicao === cards.length - 1){
        setTimeout(()=>{

            track.style.transition = "none";

            posicao = 1;

            track.style.transform = `translateX(-${posicao * larguraCard}px)`;

        },400);
    }
}

// HISTÓRIA ANTERIOR
function voltar(){
    posicao--;
    mover();

    // chegou no clone do último card
    if(posicao === 0){
        setTimeout(()=>{

            track.style.transition = "none";

            posicao = cards.length - 2;

            track.style.transform = `translateX(-${posicao * larguraCard}px)`;

        },400);
    }
}

// ABRIR HISTÓRIA ESCRITA
function abrirHistoria(){
    /* Como existem clones no carrossel: posição real começa em 1. Então subtraímos 1 para pegar o índice correto dos dados.*/

    const historiaAtual = posicao - 1;

    window.location.href = `historia.html?id=${historiaAtual}`;
}

// ABRIR VÍDEO DA HISTÓRIA
function abrirVideo(){


    /*
        O vídeo ainda não existe.

        Deixamos preparado para quando
        você adicionar o vídeo.

        Futuramente pode virar:

        historiaVideo.html?id=${historiaAtual}

        ou abrir um modal.
    */

    const historiaAtual = posicao - 1;

    console.log(  "Abrir vídeo da história:",  historiaAtual);

    alert("Vídeo desta história em desenvolvimento.");

}


// DISPONIBILIZA PARA OUTROS JS
window.avancar = avancar;
window.voltar = voltar;
window.abrirHistoria = abrirHistoria;
window.abrirVideo = abrirVideo;