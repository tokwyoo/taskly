document.addEventListener('DOMContentLoaded', function () {
    const taskModal = new bootstrap.Modal(document.getElementById('taskModal'));
    const listId = window.location.pathname.split('/')[2];
    const taskForm = document.getElementById('taskForm');

    // Validación de formulario
    function validateForm() {
        const titleInput = document.getElementById('taskTitle');
        const dueDateInput = document.getElementById('taskDueDate');
        let isValid = true;

        // Validar título
        if (!titleInput.value.trim()) {
            titleInput.classList.add('is-invalid');
            isValid = false;
        } else {
            titleInput.classList.remove('is-invalid');
            titleInput.classList.add('is-valid');
        }

        // Validar fecha
        if (!dueDateInput.value) {
            dueDateInput.classList.add('is-invalid');
            isValid = false;
        } else {
            dueDateInput.classList.remove('is-invalid');
            dueDateInput.classList.add('is-valid');
        }

        return isValid;
    }

    // Task Checkbox Handler
    document.querySelectorAll('.task-checkbox input').forEach(checkbox => {
        checkbox.addEventListener('change', async function () {
            const taskId = this.closest('.task-item').dataset.taskId;
            const endpoint = this.checked ? 'complete' : 'uncomplete';

            try {
                const response = await fetch(`/tasks/${taskId}/${endpoint}`, { method: 'POST' });
                if (response.ok) {
                    window.location.reload();
                } else {
                    throw new Error('Failed to update task status');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to update task status');
                this.checked = !this.checked;
            }
        });
    });

    // New Task Button Handler
    document.getElementById('newTask').addEventListener('click', function () {
        document.getElementById('taskId').value = '';
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDueDate').value = '';
        document.getElementById('taskNotes').value = '';

        // Limpiar clases de validación
        ['taskTitle', 'taskDueDate'].forEach(id => {
            const input = document.getElementById(id);
            input.classList.remove('is-valid', 'is-invalid');
        });

        document.querySelector('#taskModal .modal-title').textContent = 'New Task';
        taskModal.show();
    });

    // Edit Task Handler
    document.querySelectorAll('.btn-edit').forEach(button => {
        button.addEventListener('click', async function () {
            const taskItem = this.closest('.task-item');
            const taskId = taskItem.dataset.taskId;

            try {
                const response = await fetch(`/tasks/${taskId}`);
                const task = await response.json();

                document.getElementById('taskId').value = task.id;
                document.getElementById('taskTitle').value = task.title;
                document.getElementById('taskDueDate').value =
                    task.due_date ? task.due_date.split('T')[0] : '';
                document.getElementById('taskNotes').value = task.notes || '';

                // Limpiar clases de validación
                ['taskTitle', 'taskDueDate'].forEach(id => {
                    const input = document.getElementById(id);
                    input.classList.remove('is-valid', 'is-invalid');
                });

                document.querySelector('#taskModal .modal-title').textContent = 'Edit Task';
                taskModal.show();
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to load task details');
            }
        });
    });

    // Save Task Handler
    document.getElementById('saveTask').addEventListener('click', async function () {
        // Validar el formulario
        if (!validateForm()) {
            return; // No continuar si la validación falla
        }

        const taskId = document.getElementById('taskId').value;
        const formData = {
            title: document.getElementById('taskTitle').value,
            due_date: document.getElementById('taskDueDate').value || null,
            notes: document.getElementById('taskNotes').value || null
        };

        try {
            const url = taskId ? `/tasks/${taskId}` : `/lists/${listId}/tasks`;
            const method = taskId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                window.location.reload();
            } else {
                // Si la respuesta no es exitosa, no recargar
                const errorData = await response.json();
                alert(errorData.message || 'Failed to save task');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to save task');
        }
    });

    // Agregar validación en tiempo real
    ['taskTitle', 'taskDueDate'].forEach(id => {
        const input = document.getElementById(id);
        input.addEventListener('input', validateForm);
    });

    // Delete Task Handler
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', async function () {
            if (!confirm('Are you sure you want to delete this task?')) return;

            const taskItem = this.closest('.task-item');
            const taskId = taskItem.dataset.taskId;

            try {
                const response = await fetch(`/tasks/${taskId}`, { method: 'DELETE' });

                if (response.ok) {
                    window.location.reload();
                } else {
                    throw new Error('Failed to delete task');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to delete task');
            }
        });
    });
});