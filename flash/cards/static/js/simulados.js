



// --------------- SCRIPT DE EDIÇÃO ---------------- //


const modal_editado = document.getElementById('modal_edit')
const alternavaA = document.getElementById('alternativaA')
const alternavaB = document.getElementById('alternativaB')
const alternavaC = document.getElementById('alternativaC')
const alternavaD = document.getElementById('alternativaD')
const pergunta = document.getElementById('pergunta')
const id_questao = document.getElementById('id_questao')
const id_pg = document.getElementById('id_pagina')


function modal_edit(simulado_id, pergunta_simulado, a, b, c, d, id_pagina) {
    modal_editado.style.display = 'block'
    const ID_PAGINA = id_pagina
    id_pg.value = id_pagina
    id_questao.value = simulado_id
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
