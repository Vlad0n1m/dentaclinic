const $targetEl = document.getElementById("popup-modal");

// options with default values
const options = {
  placement: "bottom-right",
  backdrop: "dynamic",
  backdropClasses: "bg-gray-900/50 dark:bg-gray-900/80 fixed inset-0 z-40",
  closable: true,
  onHide: () => {
    console.log("modal is hidden");
  },
  onShow: () => {
    console.log("modal is shown");
  },
  onToggle: () => {
    console.log("modal has been toggled");
  },
};

// instance options object
const instanceOptions = {
  id: "popup-modal",
  override: true,
};

const modal = new Modal($targetEl, options, instanceOptions);

function addOneHourToDate(dateString) {
  // Преобразуем строку в объект Date
  const originalDate = new Date(dateString);

  // Создаем новый объект Date, копируя время в миллисекундах из исходного объекта
  const newDate = new Date(originalDate.getTime());

  // Прибавляем один час к новой дате
  newDate.setHours(newDate.getHours() + 1);

  // Возвращаем новый объект Date
  return newDate;
}
