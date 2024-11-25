document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const taskModal = document.getElementById('taskModal');
    const taskForm = document.getElementById('taskForm');
    const newTaskBtn = document.getElementById('newTaskBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const closeModal = document.querySelector('.close-modal');
    const modalTitle = document.getElementById('modalTitle');
    const tasksList = document.getElementById('tasksList');
    const filterButtons = document.querySelectorAll('.filter-btn');

    let currentTaskId = null;
    const listId = window.location.pathname.split('/')[2]; // Obtiene el ID de la lista de la URL

    // Functions
    function showModal(title = 'Nueva Tarea', taskData = {}) {
        modalTitle.textContent = title;
        document.getElementById('taskTitle').value = taskData.title || '';
        document.getElementById('taskDueDate').value = taskData.due_date || '';
        document.getElementById('taskNotes').value = taskData.notes || '';
        taskModal.classList.add('active');
        document.getElementById('taskTitle').focus();
    }

    function hideModal() {
        taskModal.classList.remove('active');
        taskForm.reset();
        currentTaskId = null;
    }

    function createTaskElement(task) {
        const taskElement = document.createElement('div');
        taskElement.className = `task-item ${task.is_completed ? 'completed' : ''}`;
        taskElement.dataset.taskId = task.id;

        const dueDate = task.due_date ? new Date(task.due_date).toLocaleDateString() : '';
        
        taskElement.innerHTML = `
            <div class="task-checkbox">
                <input type="checkbox" id="task-${task.id}" ${task.is_completed ? 'checked' : ''}>
                <label for="task-${task.id}"></label>
            </div>
            <div class="task-content">
                <h3 class="task-title">${task.title}</h3>
                ${dueDate ? `
                    <div class="task-due-date">
                        <i class="fas fa-calendar"></i>
                        ${dueDate}
                    </div>
                ` : ''}
                ${task.notes ? `<div class="task-notes">${task.notes}</div>` : ''}
            </div>
            <div class="task-actions">
                <button class="btn-icon edit-task" title="Editar tarea">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn-icon delete-task" title="Eliminar tarea">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return taskElement;
    }

    function showNotification(message, type = 'success') {
        // Implementar sistema de notificaciones
        alert(message);
    }

    // Event Listeners
    newTaskBtn.addEventListener('click', () => showModal());
    cancelBtn.addEventListener('click', hideModal);
    closeModal.addEventListener('click', hideModal);

    // Filter tasks
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const filter = button.dataset.filter;
            const tasks = document.querySelectorAll('.task-item');
            
            tasks.forEach(task => {
                switch(filter) {
                    case 'pending':
                        task.style.display = task.classList.contains('completed') ? 'none' : '';
                        break;
                    case 'completed':
                        task.style.display = task.classList.contains('completed') ? '' : 'none';
                        break;
                    default:
                        task.style.display = '';
                }
            });
        });
    });

    // Handle task form submission
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(taskForm);
        const taskData = {
            title: formData.get('title'),
            due_date: formData.get('due_date') || null,
            notes: formData.get('notes') || null
        };

        try {
            if (currentTaskId) {
                // Update existing task
                const response = await fetch(`/lists/${listId}/tasks/${currentTaskId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(taskData)
                });

                if (!response.ok) throw new Error('Error al actualizar la tarea');

                const updatedTask = await response.json();
                const taskElement = document.querySelector(`[data-task-id="${currentTaskId}"]`);
                taskElement.replaceWith(createTaskElement(updatedTask));
                showNotification('Tarea actualizada exitosamente');
            } else {
                // Create new task
                const response = await fetch(`/lists/${listId}/tasks`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(taskData)
                });

                if (!response.ok) throw new Error('Error al crear la tarea');

                const newTask = await response.json();
                const taskElement = createTaskElement(newTask);
                tasksList.appendChild(taskElement);
                showNotification('Tarea creada exitosamente');
            }

            hideModal();
        } catch (error) {
            console.error('Error:', error);
            showNotification(error.message, 'error');
        }
    });

    // Handle task actions (complete, edit, delete)
    tasksList.addEventListener('click', async (e) => {
        const taskItem = e.target.closest('.task-item');
        if (!taskItem) return;

        const taskId = taskItem.dataset.taskId;

        // Handle checkbox click
        if (e.target.type === 'checkbox') {
            try {
                const response = await fetch(`/lists/${listId}/tasks/${taskId}/toggle`, {
                    method: 'PUT'
                });

                if (!response.ok) throw new Error('Error al actualizar el estado de la tarea');

                taskItem.classList.toggle('completed');
            } catch (error) {
                console.error('Error:', error);
                showNotification(error.message, 'error');
                e.target.checked = !e.target.checked; // Revert checkbox state
            }
        }

        // Handle edit button click
        if (e.target.closest('.edit-task')) {
            currentTaskId = taskId;
            const taskData = {
                title: taskItem.querySelector('.task-title').textContent,
                due_date: taskItem.querySelector('.task-due-date')?.textContent.trim(),
                notes: taskItem.querySelector('.task-notes')?.textContent
            };
            showModal('Editar Tarea', taskData);
        }

        // Handle delete button click
        if (e.target.closest('.delete-task')) {
            if (!confirm('¿Estás seguro de que quieres eliminar esta tarea?')) return;

            try {
                const response = await fetch(`/lists/${listId}/tasks/${taskId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) throw new Error('Error al eliminar la tarea');

                taskItem.remove();
                showNotification('Tarea eliminada exitosamente');
            } catch (error) {
                console.error('Error:', error);
                showNotification(error.message, 'error');
            }
        }
    });

    // Close modal on outside click
    taskModal.addEventListener('click', (e) => {
        if (e.target === taskModal) {
            hideModal();
        }
    });

    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && taskModal.classList.contains('active')) {
            hideModal();
        }
    });
});