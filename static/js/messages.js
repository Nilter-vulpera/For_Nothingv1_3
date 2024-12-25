$(document).ready(function() {
    console.log('Документ готов'); // Отладка

    // Обработчик клика по заголовку чата
    $(document).on('click', '.chat-header', function() {
        console.log('Заголовок чата нажат'); // Отладка
        var chatElement = $(this).closest('.chat'); // Получаем родительский элемент .chat
        var chatId = chatElement.attr('id') ? chatElement.attr('id').split('-')[1] : null; // Получаем chatId
        var chatName = $(this).find('h2').text(); // Получаем название чата

        // Проверка на наличие chatId и chatName
        if (chatId && chatName) {
            console.log(`Открытие чата: ${chatName} (ID: ${chatId})`); // Отладка

            // Проверяем, открыто ли окно чата
            var existingChatWindow = $('#chat-windows').find(`#chat-${chatId}`);
            if (existingChatWindow.length > 0) {
                // Если окно уже открыто, обновляем его
                existingChatWindow.show();
            } else {
                // Извлекаем сообщения из текущего чата
                var messagesHtml = chatElement.find('.chat-messages').html() || '<p>Нет сообщений.</p>'; // Заглушка, если сообщений нет

                // Создаем новое окно чата
                $('#chat-windows').append(`
                    <div class="chat-window" id="chat-${chatId}">
                        <div class="chat-header">
                            ${chatName}
                            <button class="close-chat" style="float: right;">✖️</button>
                        </div>
                        <div class="chat-messages" style="max-height: 300px; overflow-y: auto;">
                            ${messagesHtml} <!-- Отображаем все сообщения -->
                        </div>
                        <input type="text" class="message-input" placeholder="Введите сообщение..." data-chat-id="${chatId}">
                        <button class="send-button" data-chat-id="${chatId}">Отправить</button>
                    </div>
                `);
                console.log('Чат добавлен в chat-windows'); // Отладка
            }

                // Прокручиваем сообщения до самого низа
          var chatWindow = $('#chat-windows').find(`#chat-${chatId}`);
          var chatMessages = chatWindow.find('.chat-messages');
            if (chatMessages.length > 0) {
                chatMessages.scrollTop(chatMessages[0].scrollHeight);
            }
        }
    });
    
    // Обработчик клика по кнопке отправки сообщения
    $(document).on('click', '.send-button', function() {
        var chatId = $(this).data('chat-id');
        var messageInput = $(this).siblings('.message-input');
        var messageContent = messageInput.val();

        if (messageContent.trim() !== '') {
            // Отправляем сообщение на сервер
            $.ajax({
                url: '/messages/send_message/', // URL вашего API для отправки сообщения
                method: 'POST',
                data: {
                    chat_id: chatId,
                    message: messageContent
                },
                success: function(response) {
                    // Обработка успешного ответа от сервера
                    // Добавляем новое сообщение в окно чата
                    var chatWindow = $('#chat-windows').find(`#chat-${chatId}`);
                    chatWindow.find('.chat-messages').append(`
                        <div class="messages">
                            <strong>Вы:</strong> <div class="message">${messageContent}</div>
                            <small>${new Date().toLocaleString()}</small>
                        </div>
                    `);

                    // Очищаем поле ввода
                    messageInput.val('');

                    // Прокручиваем сообщения до самого низа
                    var chatMessages = chatWindow.find('.chat-messages');
                    if (chatMessages.length > 0) {
                        chatMessages.scrollTop(chatMessages[0].scrollHeight);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при отправке сообщения:', error);
                }
            });
        }
    });

    // Обработчик клика по кнопке закрытия
    $(document).on('click', '.close-chat', function() {
        $(this).closest('.chat-window').remove(); // Закрываем окно чата
        console.log('Чат закрыт'); // Отладка
    });
});
