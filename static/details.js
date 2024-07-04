



document.addEventListener('DOMContentLoaded', function() {
    var urlParams = new URLSearchParams(window.location.search);
    var date = urlParams.get('date');
    document.getElementById('selected-date').innerText = date;

    fetch(`http://127.0.0.1:5000/api/ecg_features?date=${date}`)
        .then(response => response.json())
        .then(features => {
            var tableBody = document.getElementById('features-table-body');
            features.forEach(feature => {
                var row = document.createElement('tr');
                row.classList.add('border-b', 'hover:bg-gray-100');
                row.innerHTML = `
                    <td class="py-2 px-4">${new Date(feature.time).toLocaleTimeString()}</td>
                    <td class="py-2 px-4">${feature.hrv.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.sdnn.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.rmssd.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.sdsd.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.pnn50.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.lf_hf.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.lf.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.hf.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.sd1.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.sd2.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.rr.toFixed(2)}</td>
                    <td class="py-2 px-4">${feature.murmur}</td>
                    <td class="py-2 px-4">${feature.sleep_quality === 1 ? 'Baik' : 'Buruk'}</td>
                    <td class="py-2 px-4">${feature.sleep_apnea === 1 ? 'Ada' : 'Tidak Ada'}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching features:', error));
});
