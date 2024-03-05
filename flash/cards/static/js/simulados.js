

// --------------- SCRIPT DE EDIÇÃO ---------------- //


const modal_editado = document.getElementById('modal_edit')
const alternavaA = document.getElementById('alternativaA')
const alternavaB = document.getElementById('alternativaB')
const alternavaC = document.getElementById('alternativaC')
const alternavaD = document.getElementById('alternativaD')
const pergunta = document.getElementById('pergunta')
const id_questao_edit = document.getElementById('id_questao')
const id_pg = document.getElementById('id_pagina')


function modal_edit(simulado_id, pergunta_simulado, a, b, c, d, id_pagina) {
    modal_editado.style.display = 'block'
    const ID_PAGINA = id_pagina
    id_pg.value = id_pagina
    id_questao_edit.value = simulado_id
    pergunta.value = pergunta_simulado
    alternavaA.value = a
    alternavaB.value = b
    alternavaC.value = c
    alternavaD.value = d
}

function enviar() {
    modal_editado.style.display = 'none'
}


// --------------- FIM SCRIPT DE EDIÇÃO ---------------- //

// --------------- SCRIPT DE EXCLUSÃO ---------------- //
const modalDelete = document.getElementById('modal_delete')

function abrir_modal_delete(id_pagina, id_questao){
    var id_pagina_delete = document.getElementById('id_pagina_delete')
    var id_questao_delete = document.getElementById('id_questao_delete')
    id_pagina_delete.value=id_pagina;
    id_questao_delete.value =id_questao
    modalDelete.style.display='block'
}
function fechar_modal_delete(){
    modalDelete.style.display = 'none'
}
// --------------- SCRIPT DE EXCLUSÃO ---------------- //




// ---------- script de add pg simulado no template
const modal_add_pg_simulado = document.getElementById('modal_add_pg_simulado')

function abre_modal_simulados(){
    console.log('Entrou aqui')
    modal_add_pg_simulado.style.display = 'block'
}
function fecha_modal_add_pg(){
    modal_add_pg_simulado.style.display = 'none'
}