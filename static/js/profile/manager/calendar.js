document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");
  if (calendarEl) {
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridDay",
      headerToolbar: {
        left: "prev,next",
        center: "title",
        right: "dayGridYear,dayGridMonth,dayGridWeek,dayGridDay",
      },
      locale: "ru",
      dayMaxEvents: true,
      editable: true,
      events: events,
      eventDrop: function (info) {
        // Получаем данные события
        const eventData = info.event;
        const eventId = eventData.id;
        const newDate = info.event.start.toISOString(); // Новая дата перемещения

        // Отправляем запрос на изменение даты события в базе данных
        fetch("/update_event/" + eventId + "/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"), // Получаем CSRF-токен из cookie
          },
          body: JSON.stringify({ new_date: newDate }),
        })
          .then((response) => {
            if (response.ok) {
              console.log("Дата события успешно обновлена");
              // Дополнительные действия, если необходимо
            } else {
              console.error("Ошибка при обновлении даты события");
            }
          })
          .catch((error) => {
            console.error("Ошибка:", error);
          });
      },
      eventClick: function (info) {
        modal.show();
        var eventId = info.event.id;

        // Обработчик клика на кнопку удаления
        $("#delete-btn").click(function () {
          // Удаляем событие
          info.event.remove();

          // Отправляем запрос на удаление события
          fetch("/delete_event/" + eventId + "/", {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"), // Получаем CSRF-токен из cookie
            },
          })
            .then((response) => {
              // Обрабатываем ответ
              if (response.ok) {
                console.log("Событие успешно удалено");
                // Дополнительные действия, если необходимо
              } else {
                console.error("Ошибка при удалении события");
              }
            })
            .catch((error) => {
              console.error("Ошибка:", error);
            });
        });
      },
      eventMouseEnter: function (info) {
        
        info.el.style.backgroundColor = "lightyellow"; // Выделяем событие желтым цветом при наведении
        const editLink = document.createElement("span");
        editLink.textContent = "Edit Event";
        editLink.classList.add(
          "edit-link",
          "p-2",
          "cursor-pointer"
        ); // Добавляем классы для стилизации
        editLink.style.textDecoration = "underline"; // Подчеркиваем текст, чтобы он выглядел как ссылка

        info.el.appendChild(editLink);

        editLink.addEventListener("click", function (event) {
          event.stopPropagation(); // Останавливаем всплытие, чтобы не активировать eventClick календаря
          openModal(info);
        });
      },
      eventMouseLeave: function (info) {
        info.el.style.backgroundColor = ""; // Убираем подсветку при уходе курсора
        const editLink = info.el.querySelector(".edit-link"); // Ищем элемент с классом edit-link
        if (editLink) {
            editLink.remove(); // Удаляем текстовую ссылку
        }
      },
      
      dateClick: function (info) {
        var currentView = calendar.view.type;
        var newView;

        // Определите, какой вид следует переключиться на основе текущего вида
        switch (currentView) {
          case "dayGridMonth":
            newView = "timeGridWeek";
            break;
          case "timeGridWeek":
            newView = "timeGridDay";
            break;
          // Другие ваши варианты здесь
          default:
            newView = "dayGridMonth";
        }

        // Переключение на новый вид
        calendar.changeView(newView, info.dateStr);
      }

      
    });

    calendar.render();
  }
});
// footerToolbar: {
//   center: "addEventButton",
// },
// customButtons: {
//   addEventButton: {
//     text: "Add Event...",
//     click: function () {
//       var dateStr = "2000-12-21";
//       var date = new Date(dateStr + "T00:00:00"); // Преобразуем строку в объект Date

//       if (!isNaN(date.valueOf())) {
//         // Проверяем, является ли дата действительной
//         fetch("/add_event/", {
//           // Отправляем запрос на сервер для добавления события
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": getCookie("csrftoken"),
//           },
//           body: JSON.stringify({
//             // Отправляем данные о событии на сервер в формате JSON
//             title: "Dynamic Event",
//             start: date.toISOString(), // Преобразуем дату в строку формата ISO
//             allDay: true,
//           }),
//         })
//           .then((response) => {
//             if (response.ok) {
//               return response.json(); // Если запрос успешен, возвращаем ответ в формате JSON
//             } else {
//               throw new Error("Failed to add event"); // Если запрос не удался, генерируем ошибку
//             }
//           })
//           .then((data) => {
//             // Обработка успешного ответа
//             console.log(data);
//           })
//           .catch((error) => {
//             // Обработка ошибки
//             console.error("Error:", error);
//             alert("Failed to add event");
//           });
//       } else {
//         // Если дата недействительна, выводим сообщение об ошибке
//         alert("Invalid date.");
//       }
//     },
//   },
// },