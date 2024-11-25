document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const listModal = document.getElementById('listModal');
    const listForm = document.getElementById('listForm');
    const newListBtn = document.getElementById('newListBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const closeModal = document.querySelector('.close-modal');
    const modalTitle = document.getElementById('modalTitle');
    const listTitleInput = document.getElementById('listTitle');
    const listsGrid = document.getElementById('listsGrid');

    let currentListId = null;

    // Functions
    function showModal(title = 'Nueva Lista', listTitle = '') {
        modalTitle.textContent = title;
        listTitleInput.value = listTitle;
        listModal.classList.add('active');
        listTitleInput.focus();
    }

    function hideModal() {
        listModal.classList.remove('active');
        listForm.reset();
        currentListId = null;
    }

    function createListCard(list) {
        const card = document.createElement('div');
        card.className = 'list-card';
        card.dataset.listId = list.id;
        
        const date = new Date(list.created_at).toLocaleDateString();
        
        card.innerHTML = `
            <div class="list-card-header">
                <h3 class="list-title">${list.title}</h3>
                <div class="list-actions">
                    <button class="btn-icon edit-list" title="Editar lista">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-icon delete-list" title="Eliminar lista">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="list-card-footer">
                <span class="list-date">Creada: ${date}</span>
            </div>
        `;
        
        return card;
    }

    function showNotification(message, type = 'success') {
        // Puedes implementar tu propio sistema de notificaciones
        alert(message);
    }

    // Event Listeners
    newListBtn.addEventListener('click', () => showModal());
    cancelBtn.addEventListener('click', hideModal);
    closeModal.addEventListener('click', hideModal);

    // Cerrar modal al hacer clic fuera de él
    listModal.addEventListener('click', (e) => {
        if (e.target === listModal) {
            hideModal();
        }
    });

    listForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = listTitleInput.value.trim();
        if (!title) return;

        try {
            if (currentListId) {
                // Update existing list
                const response = await fetch(`/lists/${currentListId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ title })
                });

                if (!response.ok) throw new Error('Error al actualizar la lista');

                const updatedList = await response.json();
                const listCard = document.querySelector(`[data-list-id="${currentListId}"]`);
                listCard.querySelector('.list-title').textContent = updatedList.title;
                showNotification('Lista actualizada exitosamente');
            } else {
                // Create new list
                const response = await fetch('/lists/create', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ title })
                });

                if (!response.ok) throw new Error('Error al crear la lista');

                const newList = await response.json();
                const listCard = createListCard(newList);
                listsGrid.appendChild(listCard);
                showNotification('Lista creada exitosamente');
            }

            hideModal();
        } catch (error) {
            console.error('Error:', error);
            showNotification(error.message, 'error');
        }
    });

    listsGrid.addEventListener('click', async (e) => {
        const listCard = e.target.closest('.list-card');
        if (!listCard) return;

        const listId = listCard.dataset.listId;

        if (e.target.closest('.edit-list')) {
            currentListId = listId;
            const title = listCard.querySelector('.list-title').textContent;
            showModal('Editar Lista', title);
        }

        if (e.target.closest('.delete-list')) {
            if (!confirm('¿Estás seguro de que quieres eliminar esta lista?')) return;

            try {
                const response = await fetch(`/lists/${listId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) throw new Error('Error al eliminar la lista');

                listCard.remove();
                showNotification('Lista eliminada exitosamente');
            } catch (error) {
                console.error('Error:', error);
                showNotification(error.message, 'error');
            }
        }
    });

    // Prevenir que la tecla Enter cierre el modal
    listModal.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
        }
    });

    // Escape key para cerrar el modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && listModal.classList.contains('active')) {
            hideModal();
        }
    });
});