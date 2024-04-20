document.querySelector(".close").addEventListener("click", function () {
  document.getElementById("editModal").classList.add("hidden");
});

window.addEventListener("click", function (event) {
  const modal = document.getElementById("editModal");
  if (event.target === modal) {
    modal.classList.add("hidden");
  }
});

function extractUsername(text) {
    if(text) {
        const prefix = "Пациент: ";
        const suffix = ".";
        const startIndex = text.indexOf(prefix) + prefix.length;
        const endIndex = text.indexOf(suffix, startIndex);
        const username = text.substring(startIndex, endIndex).trim();
        return username;
    } else {
        return "Не определен"
    }
    
  }

function openModal(info) {
  document.getElementById("doctor_id").value =
    info.event._def.title;
  document.getElementById("patien_id").value =
    extractUsername(info.event._def.extendedProps.description);
    document.getElementById("patien_id").setAttribute('readonly', 'true')
//   document.getElementById("status").value =
//     info.event.extendedProps.patien_id;
  document.getElementById("eventTime").value = info.event.start
    .toISOString()
    .slice(0, -1);
  document.getElementById("editEventBtn").addEventListener("click", () => {
    submitEdit(info.event.id)
    
  })
    document.getElementById("comment_id").value =
      info.event._def.extendedProps.description;
    document.getElementById("comment_id").setAttribute('readonly', 'true')
    
  document.getElementById("editModal").classList.remove("hidden");
}
