const parametros = new URLSearchParams(window.location.search);
const id = parametros.get("id");
const mulher = mulheres[id];

// Verifica se a mulher existe
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
            <h1>História não encontrada</h1>
            <a href="/">Voltar para a galeria</a>
        </div>
    `;

} else {

    // Título da aba
    document.title = `${mulher.nome} | Galeria de Histórias`;

    // Hero
    document.getElementById("nome").textContent = mulher.nome;
    document.getElementById("resumo").textContent = mulher.resumo;
    document.querySelector(".categoria").textContent = mulher.categoria;

    // Imagem de fundo
    document.querySelector(".hero").style.backgroundImage =
        `url('${mulher.imagem}')`;

    // História
    document.getElementById("historia").innerHTML =
        mulher.historia;

    // Importância
    document.getElementById("importancia").innerHTML =
        mulher.importancia;

    // Destaque
    const destaque = document.getElementById("destaque");

    if (mulher.destaque) {
        destaque.innerHTML = mulher.destaque;
        destaque.style.display = "block";
    } else {
        destaque.style.display = "none";
    }

    // Informações rápidas
    const infoRapida = document.getElementById("infoRapida");

    let infoHTML = "";

    if (mulher.nascimento) {
        infoHTML += `
            <li><strong>Nascimento:</strong> ${mulher.nascimento}</li>
        `;
    }

    if (mulher.periodo) {
        infoHTML += `
            <li><strong>Período:</strong> ${mulher.periodo}</li>
        `;
    }

    if (mulher.local) {
        infoHTML += `
            <li><strong>Local:</strong> ${mulher.local}</li>
        `;
    }

    if (mulher.falecimento) {
        infoHTML += `
            <li><strong>Falecimento:</strong> ${mulher.falecimento}</li>
        `;
    }

    infoRapida.innerHTML = infoHTML;

    // Obras
    const obras = document.getElementById("obras");
    const tituloObras = document.getElementById("tituloObras");

    if (mulher.obras && mulher.obras.length > 0) {

        let obrasHTML = "";

        mulher.obras.forEach(obra => {
            obrasHTML += `<li>${obra}</li>`;
        });

        obras.innerHTML = obrasHTML;

    } else {

        tituloObras.style.display = "none";
        obras.style.display = "none";
    }

    // Referências
    const referencias = document.getElementById("referencias");

    if (mulher.referencias && mulher.referencias.length > 0) {

        let refsHTML = "";

        mulher.referencias.forEach(ref => {
            refsHTML += `<li>${ref}</li>`;
        });

        referencias.innerHTML = refsHTML;

    } else {

        referencias.innerHTML =
            "<li>Referências não informadas.</li>";
    }

}