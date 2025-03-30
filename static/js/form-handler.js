// Function to handle blood donation form submission
function handleDonationSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const donationData = {
        donor_id: formData.get('donor_id'),
        blood_group: formData.get('blood_group'),
        units_donated: formData.get('units_donated'),
        health_status: formData.get('health_status'),
        notes: formData.get('notes')
    };

    fetch('donation_process.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(donationData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Donation recorded successfully!');
            loadDonationHistory();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your donation.');
    });
}

// Function to handle blood request form submission
function handleBloodRequestSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const requestData = {
        recipient_id: formData.get('recipient_id'),
        blood_group: formData.get('blood_group'),
        units_requested: formData.get('units_requested'),
        health_status: formData.get('health_status')
    };

    fetch('blood_requests.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Blood request submitted successfully!');
            loadRequestHistory();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while submitting your request.');
    });
}

// Function to load donation history
function loadDonationHistory() {
    fetch('donation_process.php')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('donor-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = '';
        
        data.forEach(donation => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${donation.donor_name}</td>
                <td>${donation.age}</td>
                <td>${donation.blood_group}</td>
                <td>${donation.units_donated}</td>
                <td>${donation.donation_date}</td>
                <td>${donation.health_status}</td>
                <td>
                    <button class="edit-button" onclick="editDonation(${donation.id})">Edit</button>
                    <button class="delete-button" onclick="deleteDonation(${donation.id})">Delete</button>
                </td>
            `;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading donation history.');
    });
}

// Function to load request history
function loadRequestHistory() {
    fetch('blood_requests.php')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('request-table').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = '';
        
        data.forEach(request => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <td>${request.recipient_name}</td>
                <td>${request.blood_group}</td>
                <td>${request.units_requested}</td>
                <td>${request.request_date}</td>
                <td>${request.status}</td>
                <td>
                    <button class="edit-button" onclick="editRequest(${request.id})">Edit</button>
                    <button class="delete-button" onclick="deleteRequest(${request.id})">Delete</button>
                </td>
            `;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading request history.');
    });
}

// Function to edit donation
function editDonation(id) {
    fetch(`donation_process.php?id=${id}`)
    .then(response => response.json())
    .then(data => {
        // Populate form with donation data
        document.getElementById('donor_id').value = data.donor_id;
        document.getElementById('blood_group').value = data.blood_group;
        document.getElementById('units_donated').value = data.units_donated;
        document.getElementById('health_status').value = data.health_status;
        document.getElementById('notes').value = data.notes;
        
        // Show edit form
        document.getElementById('donation-form').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading donation details.');
    });
}

// Function to delete donation
function deleteDonation(id) {
    if (confirm('Are you sure you want to delete this donation?')) {
        fetch('donation_process.php', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Donation deleted successfully!');
                loadDonationHistory();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting donation.');
        });
    }
}

// Function to edit request
function editRequest(id) {
    fetch(`blood_requests.php?id=${id}`)
    .then(response => response.json())
    .then(data => {
        // Populate form with request data
        document.getElementById('recipient_id').value = data.recipient_id;
        document.getElementById('blood_group').value = data.blood_group;
        document.getElementById('units_requested').value = data.units_requested;
        document.getElementById('health_status').value = data.health_status;
        
        // Show edit form
        document.getElementById('request-form').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading request details.');
    });
}

// Function to delete request
function deleteRequest(id) {
    if (confirm('Are you sure you want to delete this request?')) {
        fetch('blood_requests.php', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Request deleted successfully!');
                loadRequestHistory();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting request.');
        });
    }
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Load donation history if on donation page
    if (document.getElementById('donor-table')) {
        loadDonationHistory();
    }
    
    // Load request history if on request page
    if (document.getElementById('request-table')) {
        loadRequestHistory();
    }
    
    // Add form submit handlers
    const donationForm = document.getElementById('donation-form');
    if (donationForm) {
        donationForm.addEventListener('submit', handleDonationSubmit);
    }
    
    const requestForm = document.getElementById('request-form');
    if (requestForm) {
        requestForm.addEventListener('submit', handleBloodRequestSubmit);
    }
}); 