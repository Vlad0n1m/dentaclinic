document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('updateProfileForm');
    form.addEventListener('submit', function(event) {
      event.preventDefault(); // Предотвращаем стандартную отправку формы
  
      const formData = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': '{{ csrf_token }}' // Обязательно для Django, чтобы избежать ошибок CSRF
        }
      })
      .then(response => response.json())  // Предполагаем, что сервер возвращает JSON
      .then(data => {
        console.log('Success:', data);
        if(data.status == 'success') {
            $('#notification').text(data.message);
        } else {
            $('#notification').text("произошла ошибка, поавторите запрос позже");
        }
        $('#notification').removeClass('hidden').addClass('block');
        
        
        // Скрываем уведомление через 3000 миллисекунд (3 секунды)
        setTimeout(function() {
          $('#notification').addClass('hidden').removeClass('block');
        }, 3000);
        // Обработка ответа, например, вывод сообщения об успешной отправке
      })
      .catch((error) => {
        console.error('Error:', error);
        // Обработка ошибки отправки формы
      });
    });
  });