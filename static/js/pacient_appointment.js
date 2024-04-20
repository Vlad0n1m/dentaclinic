// Находим все элементы списка
const slots = document.querySelectorAll(".js-slot");
const selected_date_message = document.getElementById("selected-date-message");

const popup = document.getElementById("myModal");

function closePopup() {
  popup.classList.add("hidden");
}
// Обработчик клика вне модального окна
window.onclick = function (event) {
  let modalContent = document.querySelector(".modal-content");
  if (event.target === document.getElementById("myModal")) {
    document.getElementById("myModal").classList.add("hidden");
  }
};

document.getElementById('closeModal').addEventListener('click', (event) => {
  document.getElementById("myModal").classList.add("hidden");
})

window.addEventListener("load", function () {
  // Находим элемент <div inline-datepicker="">
  var datepickerCells = document.querySelectorAll(".datepicker-cell");

  const selectElement = document.getElementById("doctor");
  const pop_up_time = document.getElementById("id_time");
  const pop_up_comment = document.getElementById("id_comment");
  let selectedDoctorId = selectElement.value;
  const form = document.getElementById("modal_form");

  const saveBtn = document.getElementById("submitForm");

  function availableSlots(date) {
    // Получаем дату из атрибута data-date элемента <span>
    const selectedDate = date;

      // console.log(selectedDate);

    // Форматируем дату для отправки запроса к базе данных
    const formattedDate = selectedDate.toLocaleDateString(); // Пример формата: '2022-02-02'

    // Отправляем запрос к серверу для проверки доступности даты
    fetch(`/available_slots/?date=${formattedDate}&doctor=${selectedDoctorId}`)
      .then((response) => response.json())
      .then((data) => {
        // Проверяем ответ от сервера и присваиваем класс "selected" выбранному элементу <span>
        if (data) {
          const container = document.querySelector("#mCSB_8_container ul"); // Получаем контейнер для слотов
          container.innerHTML = ""; // Очищаем существующие элементы

          // Перебираем каждое время и создаём элемент списка для каждого слота
          data.forEach((time) => {
            const li = document.createElement("li");
            li.className =
              "slots__item js-slot hover:bg-gray-100 cursor-pointer p-2";

            // Форматируем время
            const date = new Date(time);
            const formattedTime = date.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });

            // Function to pad numbers to two digits
            function padTo2Digits(num) {
              return num.toString().padStart(2, "0");
            }

            li.textContent = `${formattedTime}, свободно`;
            li.addEventListener("click", () => {
              console.log(selectElement.value);
              pop_up_comment.value = "";
              pop_up_time.value = `${date.getFullYear()}-${padTo2Digits(
                date.getMonth() + 1
              )}-${padTo2Digits(date.getDate())}T${padTo2Digits(
                date.getHours()
              )}:${padTo2Digits(date.getMinutes())}`;
              pop_up_time.setAttribute("readonly", "true");
              popup.classList.remove("hidden");
            }); // Устанавливаем текст для элемента списка
            container.appendChild(li); // Добавляем элемент в контейнер
          });
        } else {
          return "Ближайшая доступная дата: " + checkAvailableDate();
        }
      })
      .catch((error) => {
        console.error("Ошибка при выполнении запроса:", error);
      });
  }

  availableSlots(new Date());
  selectElement.addEventListener("change", function () {
    selectedDoctorId = this.value;
    availableSlots(new Date());
  });

  if (saveBtn) {
    saveBtn.addEventListener("click", function () {
      const formData = new FormData(form);
      formData.append("doctorId", selectedDoctorId);
  
      fetch("/create/", {
          method: "POST",
          headers: {
              "X-CSRFToken": getCookie("csrftoken"),
          },
          body: formData,
      })
      .then((response) => {
          if (response.ok) {
              return response.json();
          } else {
              throw new Error('Something went wrong on server side');
          }
      })
      .then((data) => {
          // alert("Событие сохранено!");
          data.message && window.location.replace(`/${data.message}`);
          document.getElementById("myModal").style.display = "none"; // Используйте "none" вместо "hidden"
      })
      .catch((error) => {
          console.error("Ошибка:", error);
          alert("Произошла ошибка при сохранении события.");
      });
  });
  
  }

  datepickerCells.forEach((cell) => {
    cell.addEventListener("click", () => availableSlots( new Date(parseInt(cell.getAttribute("data-date")))));
  });
});

// Перебираем элементы списка и добавляем обработчик события клика
slots.forEach((slot) => {
  slot.addEventListener("click", () => {
    //TODO

    // Создаем элемент для отображения надписи с выбранной датой
    selected_date_message.textContent = `Выбранная дата: ${123}`;

    // Добавляем обработчик события клика на кнопку "Записаться"
  });
});
