 // Cerrar automáticamente mensajes después de 5 segundos
 $(document).ready(function(){
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log('#####')
    $(".alert").delay(1000).slideUp(300, function(){
        $(this).alert('close');
    });
});