// STATUSES = {
//     ('R', 'Запрошено'),
//     ('A', 'Подтверждено'),
//     ('S', 'Состоялось'),
//     ('C', 'Отменено')
// }

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