document.addEventListener('DOMContentLoaded', function() {
    var bell = document.getElementById('notification-bell');
    var notifications = document.getElementById('notifications');

    if (bell) {
        bell.addEventListener('click', function() {
            notifications.classList.toggle('show');
        });
    }
});