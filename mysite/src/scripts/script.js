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