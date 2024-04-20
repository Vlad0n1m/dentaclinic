function checkAvailableDate() {
    //TODO
    fetch('chech_available_date/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: 'formattedDate=' + encodeURIComponent(formattedDate)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.date) {
            return data.date
        } else {
            return "У этого доктора нет свободных дат"
        }
        // Здесь вы можете обновить HTML или выполнить другие действия с полученными данными
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}