document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    fetch('https://sleepcare.azurewebsites.net/api/events')
        .then(response => response.json())
        .then(events => {
            console.log('Fetched events:', events); // Debugging line
            var calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                events: events,
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                eventContent: function(info) {
                    return {
                        html: `<b>${info.event.title}</b><br>${info.event.extendedProps.description}<br><button class="mt-2 px-2 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600">Show More</button>`
                    };
                },
                dateClick: function(info) {
                    var date = info.dateStr;
                    window.location.href = `details.html?date=${date}`;
                }
            });

            calendar.render();
        })
        .catch(error => console.error('Error fetching events:', error));
});
