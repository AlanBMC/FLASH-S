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
addQquestion.addEventListener("click", ()=>{
    container.classList.add("hide");
    question.value = "";
    answer.value = "";

    addQuestionCard.classList.remove("hide");
})

closeBtn.addEventListener("click", (hideQuestion = ()=> {
    container.classList.remove("hide");
    addQuestionCard.classList.add("hide");
    if (editBool){
        editBool = false;
        submitQuestion();
    }
})
);

cardButton.addEventListener("click", (submitQuestion=()=>{
    
    editBool = false;
    tempQuestion = question.value.trim();
    tempoAnswer = answer.value.trim();
    if(!tempQuestion || !tempoAnswer){
        errorMessage.classList.remove("hide");
    }else{
        container.classList.remove("hide");
        errorMessage.classList.add("hide");
        viewlist();
        question.value = "";
        answer.value = "";
    }
}));

function viewlist(){
    var listCard = document.getElementsByClassName("card-list-container");
    var div = document.createElement("div");
    div.classList.add("card");

    //question
    div.innerHTML += `<p class="question-div">${question.value}</p>`;
    var displayAnswer = document.createElement("p");
    displayAnswer.classList.add("answer-div", "hide");
    displayAnswer.innerText = answer.value;
    console.log(question.value)
    console.log(answer.value)
    var link = document.createElement('a');
    link.setAttribute("href", "#");
    link.setAttribute("class", "show-hide-btn");
    link.innerHTML = "Show/Hide";
    link.addEventListener("click", () =>{
        displayAnswer.classList.toggle("hide");
    });

    div.appendChild(link);
    div.appendChild(displayAnswer);


    //edit button
    let buttonsCon = document.createElement("div");
    buttonsCon.classList.add("buttons-con");
    var editButton = document.createElement("button");
    editButton.setAttribute("class", "edit");
    editButton.innerHTML = `<i class="fa-solid fa-pen-to-square"></i>`;
    editButton.addEventListener("click", ()=>{
        editBool = true;
        modifyElement(editButton, true);
        addQuestionCard.classList.remove("hide");
    });

    //caso eu queria limitar o uso do usuario remover este botão
    buttonsCon.appendChild(editButton);
    disableButtons(false);

    //delete button
    var deleteButton = document.createElement("button");
    deleteButton.setAttribute("class","delete");
    deleteButton.innerHTML= `<i class="fa-solid fa-trash"></i>`;
    deleteButton.addEventListener("click", ()=>{
        modifyElement(deleteButton);
    });
    //caso eu queria limitar o uso do usuario remover este botão
    buttonsCon.appendChild(deleteButton);

    div.appendChild(buttonsCon);
    listCard[0].appendChild(div);
    hideQuestion();
}

//modifica elementos

const modifyElement = (element, edit=false)=>{
    let parentDiv = element.parentElement.parentElement;
    let parentQuestion = parentDiv.querySelector(".question-div").innerText;
    if(edit){
        let parentAns = parentDiv.querySelector(".answer-div").innerText;
        answer.value = parentAns;
        question.value = parentQuestion;
        disableButtons(true);
    }
    parentDiv.remove();

}
//desabilit edit e delete  botões
const disableButtons = (value) =>{
    let editButtons = document.getElementsByClassName("edit");
    Array.from(editButtons).forEach((element)=>{
        element.disabled = value;
    });
};



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
            const novaPagina = document.createElement("li");
            const linkNovaPagina = document.createElement("a");
            
            linkNovaPagina.href = data.urlPagina;
            linkNovaPagina.textContent = tituloPagina; // Usa o título fornecido pelo usuário
            novaPagina.appendChild(linkNovaPagina);

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
        data.paginas.forEach((pagina,index) => {

            const paginaElemento = document.createElement("li");
            const linkPagina = document.createElement("a");
            linkPagina.href = `/user/paginas/${pagina.id}/`;  // Ajuste o URL conforme necessário
            linkPagina.textContent = pagina.titulo;
            paginaElemento.appendChild(linkPagina);


            
            if (index > 0) {
                const iconeExcluir = document.createElement("i");
                iconeExcluir.classList.add("fa-solid", "fa-trash");
                iconeExcluir.style.marginLeft = "10px";
                iconeExcluir.onclick = function(event) {
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


function excluirPagina(paginaId){
    if(!confirm(`Deseja realmente excluir essa página?`)){
        return;
    }

    fetch(`/user/excluir_pagina/${paginaId}/`,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken' : getCookie('csrftoken'),

        },
        body: JSON.stringify({id: paginaId})
    }).then(response =>{
        if(response.ok){
            alert('Pagina excluida com sucesso!');
            window.location.reload();
        }else{
            alert('nao foi possivel excluir essa pagina')
        }
    }).catch(error => console.error('Erro ao excluir pagina:', error));
}