document.addEventListener('DOMContentLoaded', function(){
    const chat_toggle = document.getElementById('chat-bot');
    const overlay = document.getElementById('overlay');

    chat_toggle.addEventListener('click', function(){
        overlay.classList.toggle('visible');
    });
});