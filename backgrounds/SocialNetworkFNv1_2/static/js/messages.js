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
    let selectedChatId = null;
    let chatType = null;
    let selectedMessageId = null;
    let username = null;
    
// Обработчик клика на элементе .chat-header
    $(document).on('click', '.chat-header', function() {
        console.log('ClickLol');
        $('.chat').removeClass('selected');
        $(this).closest('.chat').addClass('selected'); 
        
        selectedChatId = $(this).closest('.chat').data('chat-id'); // Получаем ID выбранного чата
        console.log('Выбранный чат ID:', selectedChatId);
        
        var chatElement = $(`.chat[data-chat-id="${selectedChatId}"]`);
        chatType = chatElement.data('type');  // Получаем тип чата
        console.log('Выбранный чат type:', chatType);
        if(chatType === "D"){
        
        username = $(this).find('h2').text();; // Получаем имя пользователя
        console.log('Выбранный username:', username);
        }else{
            console.log("Not the D");
        };
        var Messages = $('.message');
        if(Messages.length>0){
            var lastMessage=Messages.last();
            var selectedMessageId = lastMessage.data('message-id');
            console.log('Id Last Message:', selectedMessageId);
        }else{
            console.log('No messages');
        }
        
    });

    // Функция отправки сообщения
    function sendMessage(selectedMessageId) {
        var url = chatType === 'D' ? `/messages/dialogs/${selectedChatId}/${selectedMessageId}/${username}/` : `/messages/chat/${selectedChatId}/`;
        var messageInput = $('.message-input');
        var messageContent = messageInput.val().trim(); // Удаляем пробелы в начале и конце
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        if (selectedChatId) { // Проверяем, что selectedChatId определен
            if (messageContent !== '') { // Проверяем, что сообщение не пустое
                // Определяем URL в зависимости от типа чата
                

                // Отправляем сообщение
                $.ajax({
                    url: url, // Замените на ваш URL для отправки сообщения
                    method: 'POST',
                     headers: {
                           'X-CSRFToken': csrfToken // Добавляем CSRF-токен в заголовки
                       },
                    data: {
                        chat_id: selectedChatId, // Передаем ID выбранного чата
                        message: messageContent, // Передаем содержимое сообщения
                        last_message_id: selectedMessageId // Передаем ID последнего сообщения, если нужно
                    },
                    success: function(response) {
                    console.log('response of text  was sucesesfull', response)
                        // Обработка успешного ответа от сервера
                        var chatWindow = $('.chat-windows').find(`.chat-${selectedMessageId}`); // Получаем окно чата по ID
                        chatWindow.find('.chat-messages').append(`
                            <div class="messages">
                                <strong>Вы:</strong> <div class="message" data-message-id="{{ message.id }}">${messageContent}</div>
                                <small>${new Date().toLocaleString()}</small>
                            </div>
                        `);
                            // Прокручиваем сообщения до самого низа
                        var chatMessages = chatWindow.find('.chat-messages');
                        if (chatMessages.length > 0) {
                            chatMessages.scrollTop(chatMessages[0].scrollHeight);
                        }

                        // Очищаем поле ввода
                        messageInput.val('');
                    },
                    error: function(xhr, status, error) {
                        console.log('selectedChatId:', selectedChatId);
                        console.log('selectedMessageId:', selectedMessageId);
                        console.log('username:', username);
                        console.log('Выбранный чат type:', chatType);
                        console.error('Ошибка при отправке сообщения:', error);
                    }
                });
            } else {
                console.error('Ошибка: сообщение пустое'); // Логирование ошибки
            }
        } else {
            console.error('Ошибка: selectedChatId не определен'); // Логирование ошибки
        }
    }
    // Вызов функции отправки сообщения при нажатии кнопки
    $(document).on('click', '.send-button', function() {
            var csrfToken = $('meta[name="csrf-token"]').attr('content');
            var Messages = $('.message');
            if(Messages.length>0){
                var lastMessage=Messages.last();
                var selectedMessageId = lastMessage.data('message-id');
                console.log('Id Last Message:', selectedMessageId);
            }else{
                console.log('No messages');
            }
    // Получаем ID последнего сообщения
    $.ajax({
        url: '/messages/chats/send_message/',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: {
            'chat_id': selectedChatId,
            'content': $('#message-input').val()
        },
        success: function(response) {
            if (response.success) {
                $('#message-input').val('');
                console.log('Сообщение успешно отправлено');
            }
        },
        error: function(xhr, status, error) {
            console.error('Ошибка при отправке сообщения:', error);
            console.log('Статус ошибки:', xhr.status);
            console.log('Ответ сервера:', xhr.responseText);
        }
    });
});
    // Обработчик клика по кнопке закрытия
    $(document).on('click', '.close-chat', function() {
        $(this).closest('.chat-window').remove(); // Закрываем окно чата
        console.log('Чат закрыт'); // Отладка
    });
});
