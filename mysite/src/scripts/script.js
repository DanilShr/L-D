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
// Скрипт для отображения текущей цены
const priceRange = document.getElementById('priceRange');
const currentPrice = document.getElementById('currentPrice');

if (priceRange && currentPrice) {
    priceRange.addEventListener('input', function() {
        currentPrice.textContent = this.value;
    });
}

// Скрипт для кнопок фильтров
document.querySelector('.apply-btn').addEventListener('click', function() {
    // Здесь будет логика применения фильтров
    console.log('Фильтры применены');
});

document.querySelector('.reset-btn').addEventListener('click', function() {
    // Сброс всех фильтров
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => checkbox.checked = false);
    priceRange.value = 5000;
    currentPrice.textContent = '5000';
});