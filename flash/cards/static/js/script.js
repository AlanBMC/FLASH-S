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

function adicionarPagina() {
    const novaPagina = document.createElement("li");
    const linkNovaPagina = document.createElement("a");
    linkNovaPagina.href = "perfil.html"; // Defina o link da nova página
    linkNovaPagina.textContent = "Nova Página"; // Defina o texto da nova página
    novaPagina.appendChild(linkNovaPagina);
    
    // Adicione a nova página à lista existente
    const listaPaginas = document.querySelector(".sidebar-submenu ul");
    listaPaginas.appendChild(novaPagina);

    alert("Nova página adicionada!");
}
