// messages.js - Handle Django message alerts
document.addEventListener('DOMContentLoaded', function() {
    // Close button functionality
    const closeButtons = document.querySelectorAll('.alert .close');
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            this.parentElement.style.opacity = '0';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });
    
    // Auto-dismiss after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Slide in animation
    alerts.forEach(alert => {
        alert.style.transform = 'translateX(100%)';
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.style.transform = 'translateX(0)';
            alert.style.opacity = '1';
        }, 50);
    });
});