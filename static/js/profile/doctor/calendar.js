document.addEventListener("DOMContentLoaded", function () {
  const calendarE2 = document.getElementById("calendar_doctor");
  if (calendarE2) {
    const replaceStatusBtn = document.getElementById("replace-status-btn");

    const calendar2 = new FullCalendar.Calendar(calendarE2, {
      initialView: "dayGridYear",
      headerToolbar: {
        left: "prev,next",
        center: "title",
        right: "dayGridYear,dayGridMonth,dayGridWeek,dayGridDay",
      },
      locale: "ru",
      events: events,
      eventClick: function (info) {
        var eventData = info.event;
        let eventId = eventData._def.publicId;
        modal.show();
        replaceStatusBtn.addEventListener("click", () => {
          fetch("replace_status/", {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: `eventId=${encodeURIComponent(eventId)}&status=${$(
              "#status-dropdown"
            ).val()}`,
          })
            .then((response) => response.json())
            .then((data) => {
              console.log(data);
              if (data.status == "success") {
                // Успешный ответ от сервера
                $("#notification").removeClass("hidden").addClass("block");
                $("#notification").text(data.message);
                setTimeout(
                  () =>
                    $("#notification").removeClass("block").addClass("hidden"),
                  3000
                );
              } else {
                // Обработка ошибки или другого неудачного сценария
                $("#notification")
                  .removeClass("hidden")
                  .addClass("block")
                  .removeClass("bg-green-500")
                  .addClass("bg-red-500");
                $("#notification").text("У этого доктора нет свободных дат");
                setTimeout(
                  () =>
                    $("#notification")
                      .removeClass("block")
                      .addClass("hidden")
                      .removeClass("bg-red-500")
                      .addClass("bg-green-500"),
                  3000
                );
              }
            })
            .catch((error) => {
              console.error("Ошибка:", error);
            });
        });
      },
      dateClick: function (info) {
        var currentView = calendar2.view.type;
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
        calendar2.changeView(newView, info.dateStr);
      },
    });

    calendar2.render();
  }
});
