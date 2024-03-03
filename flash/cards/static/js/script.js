$(".sidebar-dropdown > a").click(function () {
    $(".sidebar-submenu").slideUp(200);
    if ($(this).parent().hasClass("active")) {
        $(".sidebar-dropdown").removeClass("active");
        $(this).parent().removeClass("active");
    } else {
        $(".sidebar-dropdown").removeClass("active");
        $(this).next(".sidebar-submenu").slideDown(200);
        $(this).parent().addClass("active");
    }
});
$("#close-sidebar").click(function () {
    $(".page-wrapper").removeClass("toggled");
});
$("#show-sidebar").click(function () {
    $(".page-wrapper").addClass("toggled");
});

const paginaDataElement = document.getElementById("pagina-data");
const paginaId = paginaDataElement.getAttribute("data-pagina-id");


const container = document.querySelector(".container");
const addQuestionCard = document.getElementById("add-question-card");
const cardButton = document.getElementById("save-btn");
const question = document.getElementById("question");
const answer = document.getElementById("answer");
const errorMessage = document.getElementById("error");
const addQquestion = document.getElementById("add-flashcard");
const closeBtn = document.getElementById("close-btn");
let editBool = false;

// funcoes de adicionar questao pelo click em "+"
addQquestion.addEventListener("click", () => {
    container.classList.add("hide");
    question.value = "";
    answer.value = "";

    addQuestionCard.classList.remove("hide");
})

closeBtn.addEventListener("click", (hideQuestion = () => {
    container.classList.remove("hide");
    addQuestionCard.classList.add("hide");
    if (editBool) {
        editBool = false;
        submitQuestion();
    }
})
);
// bloco de editar card
function edit_cards(cardId, pergunta, resposta) {
    // FAZER: colocar os valores nos textes area para caso aja erro de digitação e o usuario nao precise reescrever tudo


    document.getElementById('pergunta_get').value = pergunta
    document.getElementById('resposta_get').value = resposta

    document.getElementById('id_card').value = cardId;

    var modal = document.getElementById('modal')
    modal.style.display = 'block'

}
//fim bloco de editar card

// ver resposta
function ver_resposta(cardId) {
    var div_resposta = document.getElementById('ver_resposta_' + cardId);
    if (div_resposta.style.display === 'block') {
        div_resposta.style.display = 'none';
    } else {
        div_resposta.style.display = 'block';
    }
}

//fim ver resposta
// fecha o modal
function fecha_modal() {
    var modal = document.getElementById('modal')
    modal.style.display = 'none'
}
//fim fecha modal



// faz o botao salvar dentro do modal funcionar
cardButton.addEventListener("click", (submitQuestion = () => {

    editBool = false;
    tempQuestion = question.value.trim();
    tempoAnswer = answer.value.trim();

    if (!tempQuestion || !tempoAnswer) {
        errorMessage.classList.remove("hide");
    } else {
        container.classList.remove("hide");
        errorMessage.classList.add("hide");
        viewlist();
        question.value = "";
        answer.value = "";
    }
}));




function viewlist() {
    var div = document.createElement("div");
    div.classList.add("card");

    //question
    div.innerHTML += `<p class="question-div">${question.value}</p>`;
    var displayAnswer = document.createElement("p");
    displayAnswer.classList.add("answer-div", "hide");

    displayAnswer.innerText = answer.value;

    //salvando os cards no banco de dados ---------------
    document.getElementById('formQuestion').value = question.value;
    document.getElementById('formAnswer').value = answer.value;
    document.getElementById('cardForm').submit();
    console.log('enviou')
    // Submete o formulário
    document.getElementById('cardForm').submit();
    // fechando bloco --------------------------





}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function adicionarPagina2() {
    // Solicita ao usuário o título da nova página
    const tituloPagina = prompt("Digite o título da nova página:");
    const csrftoken = getCookie('csrftoken');

    // Verifica se o título foi fornecido
    if (tituloPagina) {
        fetch('/user/criar_pagina/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                // Inclua outros headers necessários, como CSRF token
            },
            body: JSON.stringify({
                titulo: tituloPagina, // Envie o título como parte da requisição

                // Você pode adicionar outros dados necessários aqui
            })
        })
            .then(response => response.json())
            .then(data => {

                alert("Nova página adicionada com sucesso!");

                // Atualiza a interface do usuário

                

                // Adiciona a nova página à lista existente
                const listaPaginas = document.querySelector(".sidebar-submenu ul");
                listaPaginas.appendChild(novaPagina);
            })
            .catch((error) => {
                console.error('Erro:', error);
                alert("Houve um erro ao adicionar a nova página. Por favor, tente novamente.");
            });
    } else {
        alert("A criação da página foi cancelada ou o título não foi fornecido.");
    }
}

carregarPaginasUsuario();
function carregarPaginasUsuario() {
    fetch('/user/listar_paginas/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // Adicione headers adicionais aqui se necessário, como tokens de autenticação
        }
    })
        .then(response => response.json())
        .then(data => {
            const listaPaginas = document.querySelector(".sidebar-submenu ul");
            data.paginas.forEach((pagina, index) => {





                if (index > 0) {
                    const iconeExcluir = document.createElement("i");
                    iconeExcluir.classList.add("fa-solid", "fa-trash");
                    iconeExcluir.style.marginLeft = "10px";
                    iconeExcluir.onclick = function (event) {
                        event.stopPropagation(); // Impede que o evento de clique no link seja acionado
                        event.preventDefault(); // Impede o comportamento padrão do link
                        excluirPagina(pagina.id);
                    };
                    // Adiciona um espaço e o ícone diretamente ao linkPagina
                    linkPagina.appendChild(iconeExcluir);
                }
                paginaElemento.appendChild(linkPagina);
                listaPaginas.appendChild(paginaElemento);
            });
        })
        .catch(error => console.error('Erro ao carregar páginas:', error));
}


function excluirPagina(paginaId) {
    if (!confirm(`Deseja realmente excluir essa página?`)) {
        return;
    }

    fetch(`/user/excluir_pagina/${paginaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),

        },
        body: JSON.stringify({ id: paginaId })
    }).then(response => {
        if (response.ok) {
            alert('Pagina excluida com sucesso!');
            window.location.reload();
        } else {
            alert('nao foi possivel excluir essa pagina')
        }
    }).catch(error => console.error('Erro ao excluir pagina:', error));
}



