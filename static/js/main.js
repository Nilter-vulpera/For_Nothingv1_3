function popup(){
    var change1= document.getElementById("Audio");
    change1.classList.toggle('show');
}


function color(){
    document.querySelector('form').addEventListener('submit', function(event) {
        var message = document.getElementById('message');
        var colorSelector = document.getElementById('colorSelector');
        var selectedColor = colorSelector.options[colorSelector.selectedIndex].value;
        message.style.color = selectedColor;
    });
}
//function open() {
//    document.getElementById("openButtonForm").onclick = function(event) {
//        var form123 = document.getElementById('message-formFromAccount');
//        if (form123.classList.contains('messageFormInAccount')) {
//            form123.classList.remove('messageFormInAccount');
//            form123.classList.add('show123');
//        } else {
//            form123.classList.remove('show123');
//            form123.classList.add('messageFormInAccount');
//        }
//    };
//}
//document.addEventListener("DOMContentLoaded", open);
document.addEventListener('DOMContentLoaded', function() {
            const button = document.getElementById('openButtonForm');
            const formContainer = document.getElementById('message-formFromAccount');

            button.addEventListener('click', function() {
                if (formContainer.classList.contains('show')) {
                    formContainer.classList.remove('show');
                } else {
                    formContainer.classList.add('show');
                }
            });
});
document.addEventListener('DOMContentLoaded', function() {

            const formContainer = document.getElementById('AudioHover');

            formContainer.addEventListener('click', function() {
                formContainer.classList.toggle("show123")
            });
             document.querySelector('#Audio').addEventListener('click', function(event) {
                        const AudioContainer = document.getElementById('Audio');
                        event.stopPropagation(); // Предотвращает дальнейшее распространение события
              });
});
        // Получить CSRF-токен из cookies
function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Проверка, начинается ли cookie с нужного имени
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

const csrftoken = getCookie('csrftoken');

 document.addEventListener("DOMContentLoaded", function(event){
        var dialog = document.getElementById("messages");
        dialog.scrollTop = dialog.scrollHeight;
    });

document.addEventListener("DOMContentLoaded", function() {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    var observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    var observer = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var message = entry.target;
                var messageId = message.getAttribute('data-id');
                fetch(`/messages/${messageId}/read/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                    }
                }).then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                }).then(data => {
                    if (data.status === 'success') {
                        var statusElem = message.querySelector('small');
                        statusElem.innerText = 'Прочитано';
                    }
                }).catch(error => {
                    console.error('Error:', error);
                });
                observer.unobserve(message);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.list-group-item').forEach(function(message) {
        observer.observe(message);
    });
});

// Обновление: определите переменную csrfToken






