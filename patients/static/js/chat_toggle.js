document.addEventListener('DOMContentLoaded', function(){
    const chat_toggle = document.getElementById('chat-bot');
    const overlay = document.getElementById('overlay');
    const closeButton = document.getElementById('closeButton');

    chat_toggle.addEventListener('click', function(){
        if (overlay.classList.contains('visible')){
            overlay.classList.remove('visible');
        } else{
            overlay.classList.add('visible');
        }
    });

    closeButton.addEventListener('click', function (){
        overlay.classList.remove('visible');
    });
});