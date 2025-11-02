// Add any JavaScript functionality here
document.addEventListener('DOMContentLoaded', function() {
    console.log('Web application loaded');

    const fileInput = document.querySelector('.file-input');
    const fileNameDisplay = document.querySelector('.selected-file-name');

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileNameDisplay.textContent = this.files[0].name;
            } else {
                fileNameDisplay.textContent = '';
            }
        });
    }
}); 