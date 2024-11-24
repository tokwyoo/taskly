// Utility functions
function showAlert(message, type = 'error') {
    const alert = document.getElementById('alert');
    alert.textContent = message;
    alert.className = `alert ${type}`;
    alert.classList.remove('hidden');
    setTimeout(() => alert.classList.add('hidden'), 5000);
}

// Profile photo preview and upload
document.getElementById('photo-input')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-preview').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Profile update handler
document.getElementById('profile-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('bio', document.getElementById('bio').value);
    
    const photoInput = document.getElementById('photo-input');
    if (photoInput.files.length > 0) {
        formData.append('photo', photoInput.files[0]);
    }

    try {
        const response = await fetch('/api/update-profile', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.error);
        
        showAlert('Profile updated successfully', 'success');
    } catch (error) {
        showAlert(error.message);
    }
});

// Security settings update handler
document.getElementById('security-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        email: document.getElementById('email').value,
        current_password: document.getElementById('current-password').value,
        new_password: document.getElementById('new-password').value
    };

    try {
        const response = await fetch('/api/update-security', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) throw new Error(result.error);
        
        showAlert('Security settings updated successfully', 'success');
        document.getElementById('current-password').value = '';
        document.getElementById('new-password').value = '';
    } catch (error) {
        showAlert(error.message);
    }
});

// Delete account modal handlers
const deleteModal = document.getElementById('delete-modal');
const deleteButton = document.getElementById('delete-account-button');
const cancelButton = document.getElementById('cancel-delete');
const confirmDeleteButton = document.getElementById('confirm-delete');

deleteButton?.addEventListener('click', () => {
    deleteModal.classList.remove('hidden');
});

cancelButton?.addEventListener('click', () => {
    deleteModal.classList.add('hidden');
});

document.getElementById('delete-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        password: document.getElementById('delete-password').value
    };

    try {
        const response = await fetch('/api/delete-account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) throw new Error(result.error);
        
        window.location.href = '/login';
    } catch (error) {
        showAlert(error.message);
    }
});