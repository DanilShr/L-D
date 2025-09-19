function openModal() {
    document.getElementById("myModal").style.display = "block";
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

// Закрыть модальное окно при клике вне его области
window.onclick = function(event) {
    let modal = document.getElementById("myModal");
    if (event.target == modal) {
        closeModal();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Вешаем обработчик на document, который сработает при изменении любого file input
    document.addEventListener('change', function(event) {
        if (event.target.id === 'file-input' && event.target.files[0]) {
            const file = event.target.files[0];
            const avatarPreview = document.getElementById('avatar-preview');

            if (avatarPreview && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        }
    });
});