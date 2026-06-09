// Active menu highlighting
document.addEventListener('DOMContentLoaded', function() {
    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', function(e) {
        const sidebar = document.getElementById('sidebar');
        const toggle = document.getElementById('sidebarToggle');
        if (window.innerWidth < 992) {
            if (!sidebar.contains(e.target) && e.target !== toggle) {
                sidebar.classList.remove('show');
            }
        }
    });
    
    // Auto-hide alerts after 4 seconds
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        });
    }, 4000);
});

// Confirm delete function
function confirmDelete(url) {
    if (confirm('آیا از حذف این آیتم اطمینان دارید؟ این عملیات قابل بازگشت نیست.')) {
        window.location.href = url;
    }
}