function validateInput(inputElement) {
    // Remove espaços em branco do valor inserido
    const inputValue = inputElement.value.replace(/\s/g, '');

    // Atualize o valor do campo com os caracteres válidos
    inputElement.value = inputValue;

    // Verifique se há espaços
    if (inputValue.includes(' ')) {
        document.getElementById('error-message').textContent = 'Não são permitidos espaços.';
    } else {
        document.getElementById('error-message').textContent = '';
    }
}



function verificaForcaSenha() 
{
	var numeros = /([0-9])/;
	var alfabeto = /([a-zA-Z])/;
	var chEspeciais = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;

	if($('#password').val().length<6) 
	{
        $('#password-status').html("<span style='color:red'>Fraco, insira no mínimo 6 caracteres</span>");
        
	} else {  	
		if($('#password').val().match(numeros) && $('#password').val().match(alfabeto) && $('#password').val().match(chEspeciais))
		{            
            $('#password-status').html("<span style='color:green'><b>Forte</b></span>");
            liberaButton();
		} else {
            $('#password-status').html("<span style='color:orange'>Médio, insira um caracter especial</span>");
            
		}
	}
}

