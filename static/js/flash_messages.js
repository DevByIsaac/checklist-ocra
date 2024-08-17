// static/js/flash_messages.js

document.addEventListener('DOMContentLoaded', function() {
    // Recupera los mensajes flash del HTML
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(messageElement) {
        // Muestra el mensaje en una ventana emergente (alerta)
        alert(messageElement.innerText);
    });
});
