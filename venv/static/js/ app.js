document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const fileInput = document.querySelector('input[name="file"]');
    const userId = document.querySelector('input[name="user_id"]').value;
    const year = document.querySelector('input[name="year"]').value;

    if (!fileInput.files.length) {
        alert('Please select a file');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Add CSRF token for Django
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch(`/api/finance/upload/${userId}/${year}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        });

        const result = await response.json();
        alert(JSON.stringify(result));

        if (response.ok) {
            loadRecords(userId, year);  // load the table after upload
        }
    } catch (err) {
        console.error(err);
        alert('Upload failed');
    }
});

// Load records into table
async function loadRecords(userId, year) {
    const response = await fetch(`/api/finance/records/${userId}/${year}/`);
    const data = await response.json();

    const tbody = document.querySelector('#records-table tbody');
    tbody.innerHTML = '';

    data.forEach(record => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${record.month}</td><td>${record.amount}</td>`;
        tbody.appendChild(tr);
    });

    // TODO: Add chart rendering here if needed
}
