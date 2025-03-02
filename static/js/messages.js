document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.chat-header').forEach(function(header) {
        header.addEventListener('click', function(event) {
            event.stopPropagation(); // Предотвращаем дальнейшее распространение события
            
            var chatWindow = this.closest('.chat'); // Находим родительский элемент .chat
            var chatMessages = chatWindow.querySelector('.chat-messages'); // Находим сообщения в этом чате

            // Закрываем все другие сообщения
            

            // Переключаем видимость текущих сообщений
            if (chatMessages.style.display === 'none' || chatMessages.style.display === '') {
                chatMessages.style.display = 'block'; // Открываем сообщения
                chatMessages.scrollTop = chatMessages.scrollHeight; // Прокручиваем до самого низа
            } else {
                chatMessages.style.display = 'none'; // Закрываем сообщения
            }
        });
    });
});
