// Flash mesajları 3 saniyədən sonra avtomatik gizlət
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        }, 3000);
    });
});
