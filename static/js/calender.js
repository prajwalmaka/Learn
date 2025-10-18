document.addEventListener('DOMContentLoaded', function() {
    // Calendar navigation
    document.querySelectorAll('.calendar-nav').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const month = this.dataset.month;
            window.location.href = `?month=${month}`;
        });
    });
    
    // Assignment submission form handling
    const submissionForm = document.getElementById('submission-form');
    if (submissionForm) {
        submissionForm.addEventListener('submit', function(e) {
            const fileInput = this.querySelector('input[type="file"]');
            if (fileInput.files.length > 0) {
                const fileSize = fileInput.files[0].size / 1024 / 1024; // MB
                if (fileSize > 5) {
                    e.preventDefault();
                    alert('File size must be less than 5MB');
                }
            }
        });
    }
});