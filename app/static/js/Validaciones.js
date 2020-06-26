function validateForm() {

  var msg = ''
  var error = false;

  //Nombre
  var x = document.forms["registro"]["nombre"].value;

  if ((x == "") || (validarTexto(x) == false)) {
    msg = msg + "- Campo 'Nombre' vacio o nombre invalido <br />";
    error = true;
  }

  //Apellido
  var apellido = document.forms["registro"]["apellido"].value;

  if ((apellido == "") || (validarTexto(apellido) == false)) {
    msg = msg + "- Campo 'Apellido' vacio o apellido invalido <br />";
    error = true;
  }

  //Correo Electronico
  var email = document.forms["registro"]["correo"].value;

  if ((email == "") || (validarEmail(email) == false)) {
    msg = msg + "- Campo 'Correo Electronico' vacio o correo invalido <br />";
    error = true;
  }

  //Contraseñas
  var pass1 = document.forms["registro"]["password1"].value;
  var pass2 = document.forms["registro"]["password2"].value;

  if ((pass1 == "")) {
    msg = msg + "- Clave no es valida <br />";
    error = true;
  } else {
    if ((pass1 != pass2)) {
      msg = msg + "- Las claves no coinciden <br />";
      error = true;
    }
  }

  //DNI titular tarjeta
  var dnititular = document.forms["registro"]["titularTarj"].value;

  if ((dnititular == "")) {
    msg = msg + "- Por favor ingrese el DNI del titular de la tarjeta <br />";
    error = true;
  }

  //Numero de tarjeta de credito
  var num_tarjeta = document.forms["registro"]["numero_de_tarjeta"].value;

  if ((num_tarjeta.toString().length != 16)) {
    msg = msg + "- El numero de tarjeta ingresado no es valido <br />";
    error = true;
  }

  //Nombre y apellido del titular tarjeta
  var nombre_titular = document.forms["registro"]["nombre_titular_tarjeta"].value;

  if ((nombre_titular == "")) {
    msg = msg + "- Por favor ingrese el nombre y apellido del titular de la tarjeta <br />";
    error = true;
  }

  //Numero CVC de tarjeta
  var cvc_tarjeta = document.forms["registro"]["cvc_tarj"].value;

  if ((cvc_tarjeta.toString().length != 3)) {
    msg = msg + "- El numero de CVC ingresado no es valido <br />";
    error = true;
  }

  //Check vencimiento de tarjeta

  var mes_seleccionado = document.getElementById('mes_venc');
  var anio_seleccionado = document.getElementById('anio_venc');

  //Fechas actuales
  var d = new Date();
  var anioAct = d.getFullYear(); //2020
  var mesAct = d.getMonth() + 1; // Enero = 1 Febrero = 2

  //Datos subidos en el form
  var mesVenc = mes_seleccionado.value;
  var anioVenc = anio_seleccionado.value;

  if (anioVenc < anioAct || (anioVenc == anioAct && mesVenc < mesAct)) {
    msg = msg + "- La tarjeta de crédito está vencida, imposible realizar transacción <br />";
    error = true;
  }

  /* **************************************** */

  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    document.getElementById("hay_errores").innerHTML = "Se han encontrado errores en el formulario. Revísalo e intenta de nuevo.";
    return false;
  }
  return true;
}

function validarLibro2(){

  var msg = '';
  var error = false;


  var descripcion = document.forms["registroL"]["descripcion"].value;

  if (descripcion == "") {
    msg = msg + "- Complete el campo descripcion <br />";
    error = true;
  }

  var ISBN = document.forms["registroL"]["ISBN"].value;

  if (ISBN == "") {
    msg = msg + "- Complete el campo ISBN <br />";
    error = true;
  }

  var editorial = document.forms["registroL"]["editorial"].value;

  if (editorial == 0){
    msg = msg + "- No ha seleccionado una editorial <br />";
    error = true;
  }

  var autor = document.forms["registroL"]["autor"].value;

  if (autor == 0){
    msg = msg + "- No ha seleccionado un autor <br />";
    error = true;
  }

  var genero = document.forms["registroL"]["genero"].value;

  if (genero == 0){
    msg = msg + "- No ha seleccionado un genero <br/ >";
    error = true;
  }


  var edicion = document.forms["registroL"]["edicion"].value;

  if (edicion == ""){
    msg = msg + "- Complete la fecha de edicion <br/ >";
    error = true;
  }

  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    document.getElementById("hay_errores").innerHTML = "Se han encontrado errores en el formulario. Revísalo e intenta de nuevo.";
    return false;
  }
  return true;


}





function validarLibro(){

  var msg = '';
  var error = false;

  var x = document.forms["registroL"]["titulo"].value;

  if (x == "") {
    msg = msg + "- Complete el campo titulo <br />";
    error = true;
  }

  var descripcion = document.forms["registroL"]["descripcion"].value;

  if (descripcion == "") {
    msg = msg + "- Complete el campo descripcion <br />";
    error = true;
  }

  var ISBN = document.forms["registroL"]["ISBN"].value;

  if (ISBN == "") {
    msg = msg + "- Complete el campo ISBN <br />";
    error = true;
  }

  var editorial = document.forms["registroL"]["editorial"].value;

  if (editorial == 0){
    msg = msg + "- No ha seleccionado una editorial <br />";
    error = true;
  }

  var autor = document.forms["registroL"]["autor"].value;

  if (autor == 0){
    msg = msg + "- No ha seleccionado un autor <br />";
    error = true;
  }

  var genero = document.forms["registroL"]["genero"].value;

  if (genero == 0){
    msg = msg + "- No ha seleccionado un genero <br/ >";
    error = true;
  }


  var edicion = document.forms["registroL"]["edicion"].value;

  if (edicion == ""){
    msg = msg + "- Complete la fecha de edicion <br/ >";
    error = true;
  }

  var capitulos = document.forms["registroL"]["cantCap"].value;

  if (capitulos <= 0){
    msg = msg + "- Numero de capitulos inválido <br/ >";
    error = true;
  }


  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    document.getElementById("hay_errores").innerHTML = "Se han encontrado errores en el formulario. Revísalo e intenta de nuevo.";
    return false;
  }
  return true;


}




function validarGenero() {
  var msg = ''
  var error = false;
  var genero = document.forms["gen"]["genero"].value;

  if (genero == "") {
    msg= msg + "Género inválido";
    error = true;
  }
  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    return false;
  }
  return true;
}

function validarAutor() {
  var msg = ''
  var error = false;

  var autor = document.forms["aut"]["autor"].value;

  if ((autor == "")) {
    msg = msg + "Autor inválido";
    error = true;
  }
  if (error = true) {
    document.getElementById("los_errores").innerHTML = msg;
    return false;
  }
  return true;
}

function validarEditorial(){
  var msg = ''
  var error = false;
  var editorial = document.forms["edit"]["editorial"].value;

  if ((editorial == "")) {
    msg = msg + "Editorial inválida";
    error = true;
  }
  if (error == true){
    document.getElementById("los_errores").innerHTML = msg;
    return false;
  }
  return true;
}


function validarCapitulo(){
  var msg = ''
  var error = false;
  var cantP = document.forms["subirArchivo"]["cantPags"].value;

  if ((cantP == "") || (cantP <= 0)){
    msg = msg + "- Cantidad de paginas inválida </br>"
    error = true
  }
  var fecV = document.forms["subirArchivo"]["fec_ven"].value;
  if (fecV == ""){
    msg = msg + "- Fecha inválida"
    error = true
  }
  if (error == true){
    document.getElementById("los_errores").innerHTML = msg;
    return false;
  }
  return true;

}


function validarModCapitulo(){
  var msg = ''
  var error = false;
  var cantPags = documents.forms["modCap"]["cantPags"].value;

  if ((cantPags == "") || (cantPags <= 0)){
    msg = msg + "- Cantidad de paginas inválida </br>"
    error = true
  }

  var fecVen = documents.forms["modCap"]["fec_ven"].value;

  if (fecVen == ""){
    msg = msg + "- Fecha inválida"
    error = true
  }
  if (error == true){
    document.getElementById("los_errores").innerHTML = msg;
    return false;
  }
  return true;
}

function validarModificacion() {

  var msg = ''
  var error = false;

  //Nombre
  var x = document.forms["modificar_datos_personales"]["nombre"].value;

  if ((x == "") || (validarTexto(x) == false)) {
    msg = msg + "- Campo 'Nombre' vacio o nombre invalido <br />";
    error = true;
  }

  //Apellido
  var apellido = document.forms["modificar_datos_personales"]["apellido"].value;

  if ((apellido == "") || (validarTexto(apellido) == false)) {
    msg = msg + "- Campo 'Apellido' vacio o apellido invalido <br />";
    error = true;
  }

  //Contraseñas
  var pass1 = document.forms["modificar_datos_personales"]["password1"].value;
  var pass2 = document.forms["modificar_datos_personales"]["password2"].value;

  if ((pass1 == "")) {
    msg = msg + "- Clave no es valida <br />";
    error = true;
  } else {
    if ((pass1 != pass2)) {
      msg = msg + "- Las claves no coinciden <br />";
      error = true;
    }
  }

  //DNI titular tarjeta
  var dnititular = document.forms["modificar_datos_personales"]["titularTarj"].value;

  if ((dnititular == "")) {
    msg = msg + "- Por favor ingrese el DNI del titular de la tarjeta <br />";
    error = true;
  }

  //Numero de tarjeta de credito
  var num_tarjeta = document.forms["modificar_datos_personales"]["numero_de_tarjeta"].value;

  if ((num_tarjeta.toString().length != 16)) {
    msg = msg + "- El numero de tarjeta ingresado no es valido <br />";
    error = true;
  }

  //Nombre y apellido del titular tarjeta
  var nombre_titular = document.forms["modificar_datos_personales"]["nombre_titular_tarjeta"].value;

  if ((nombre_titular == "")) {
    msg = msg + "- Por favor ingrese el nombre y apellido del titular de la tarjeta <br />";
    error = true;
  }

  //Numero CVC de tarjeta
  var cvc_tarjeta = document.forms["modificar_datos_personales"]["cvc_tarj"].value;

  if ((cvc_tarjeta.toString().length != 3)) {
    msg = msg + "- El numero de CVC ingresado no es valido <br />";
    error = true;
  }

  //Check vencimiento de tarjeta

  var mes_seleccionado = document.getElementById('mes_venc');
  var anio_seleccionado = document.getElementById('anio_venc');

  //Fechas actuales
  var d = new Date();
  var anioAct = d.getFullYear(); //2020
  var mesAct = d.getMonth() + 1; // Enero = 1 Febrero = 2

  //Datos subidos en el form
  var mesVenc = mes_seleccionado.value;
  var anioVenc = anio_seleccionado.value;

  if (anioVenc < anioAct || (anioVenc == anioAct && mesVenc < mesAct)) {
    msg = msg + "- La tarjeta de crédito está vencida, intente con una nueva <br />";
    error = true;
  }

  /* **************************************** */

  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    document.getElementById("hay_errores").innerHTML = "Se han encontrado errores en el formulario. Revísalo e intenta de nuevo.";
    return false;
  }
  return true;
}

function validarNuevoPerfil_premium() {
  var msg = ''
  var error = false;

  //Nombre de perfil
  var x = document.forms["agregar_profile"]["profile_name"].value;

  if ((x == "") || (validarTexto(x) == false)) {
    msg = msg + "- Campo 'Nombre' vacio o nombre invalido <br />";
    error = true;
  }

  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    document.getElementById("hay_errores").innerHTML = "Se han encontrado errores en el formulario. Revísalo e intenta de nuevo.";
    return false;
  }
  return true;

}

function validarNuevoPerfil() {
  var msg = ''
  var error = false;

  //Nombre de perfil
  var x = document.forms["agregar_profile"]["profile_name"].value;

  if ((x == "") || (validarTexto(x) == false)) {
    msg = msg + "- Campo 'Nombre' vacio o nombre invalido <br />";
    error = true;
  }

  if (error == true) {
    document.getElementById("los_errores").innerHTML = msg;
    document.getElementById("hay_errores").innerHTML = "Se han encontrado errores en el formulario. Revísalo e intenta de nuevo.";
    return false;
  }
  return true;

}



function confirmarBorrarPerfil() {
  if (!confirm("¿Estas seguro de que quieres borrar este perfil?")) {
    event.preventDefault();
  }
}

function validarTexto(text) {
  return /^[A-Za-z ]+$/.test(text);
}

function validarEmail(mail) {
  return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/.test(mail);
}

function validarTextoAlfanumerico(alfanum){
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%#*?&])([A-Za-z\d$@$!%#*?&]$/.test(alfanum);
}
function validarContraseña(contraseña) {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%#*?&])([A-Za-z\d$@$!%#*?&]|[^ ]){6,}$/.test(contraseña);
}

function validarUsuario(usuario) {
  return /^[A-Za-z0-9]+$/.test(usuario);
}
