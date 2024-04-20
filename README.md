# dentaclinic

У заявки всего 4 статуса ( appointment.status ):
1) 'R' (requested) - запрошено, значит пациент отправил заявку на прием к доктору (ставит юзер)
2) 'A' (ascepted) - подтверждено, модератор подтвердил дату приема (ставит модер)
3) 2 случая
    3.1) 'S' (successful) - завершен, доктор завершил прием успешно (ставит доктор)
    3.1) 'С' (canceled) - отменен, прием не состоялся (ставит доктор или модер)

Цвета статусов:

function statusToColor(status) {
    switch (status) {
        case 'R':
            return "#fc0303"
        case 'A':
            return "#03fcf4"
        case 'S':
            return "#03fc03"
        case 'C':
            return "#fff"

        default:
            return "#fcfc03"

    }
}