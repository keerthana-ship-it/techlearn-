document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility in forms
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = document.querySelector(this.getAttribute('data-target'));
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle icon
            const icon = this.querySelector('i');
            if (type === 'password') {
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Handle multi-select skill dropdowns with Bootstrap Select
    if (document.querySelector('.skill-select')) {
        $('.skill-select').selectpicker();
    }
    
    // Tooltips initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Quiz timer functionality
    const quizTimerElement = document.getElementById('quiz-timer');
    if (quizTimerElement) {
        const timeLimit = parseInt(quizTimerElement.getAttribute('data-time-limit'));
        let timeRemaining = timeLimit * 60; // Convert to seconds
        
        const timerInterval = setInterval(function() {
            timeRemaining--;
            
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            
            quizTimerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                document.getElementById('quiz-form').submit();
            }
        }, 1000);
    }
    
    // AJAX bookmark functionality
    const bookmarkButtons = document.querySelectorAll('.bookmark-button');
    bookmarkButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const itemId = this.getAttribute('data-id');
            const itemType = this.getAttribute('data-type');
            const isBookmarked = this.getAttribute('data-bookmarked') === 'true';
            
            const url = isBookmarked ? 
                `/${itemType}/remove-bookmark/${itemId}` : 
                `/${itemType}/bookmark/${itemId}`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle button state
                    this.setAttribute('data-bookmarked', !isBookmarked);
                    
                    // Update icon and text
                    const icon = this.querySelector('i');
                    if (!isBookmarked) {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        this.querySelector('span').textContent = 'Bookmarked';
                    } else {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        this.querySelector('span').textContent = 'Bookmark';
                    }
                    
                    // Show toast notification
                    const toastMessage = !isBookmarked ? 
                        `${itemType === 'content' ? 'Content' : 'Event'} bookmarked successfully` : 
                        'Bookmark removed';
                    
                    // Create and show toast
                    const toastContainer = document.getElementById('toast-container');
                    if (toastContainer) {
                        const toastEl = document.createElement('div');
                        toastEl.className = 'toast';
                        toastEl.setAttribute('role', 'alert');
                        toastEl.setAttribute('aria-live', 'assertive');
                        toastEl.setAttribute('aria-atomic', 'true');
                        
                        toastEl.innerHTML = `
                            <div class="toast-header">
                                <strong class="me-auto">TechLearn</strong>
                                <small>Just now</small>
                                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                            <div class="toast-body">
                                ${toastMessage}
                            </div>
                        `;
                        
                        toastContainer.appendChild(toastEl);
                        const toast = new bootstrap.Toast(toastEl);
                        toast.show();
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Progress tracking for roadmap topics
    const topicCheckboxes = document.querySelectorAll('.topic-checkbox');
    topicCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const topicId = this.getAttribute('data-topic-id');
            const topicRow = document.getElementById(`topic-${topicId}`);
            
            // Submit form to update progress
            document.getElementById(`mark-topic-form-${topicId}`).submit();
            
            // Update UI immediately for better UX
            if (this.checked) {
                topicRow.classList.add('topic-completed');
            } else {
                topicRow.classList.remove('topic-completed');
            }
        });
    });
    
    // Filter form submission
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Remove empty fields to keep URL clean
            const formElements = this.elements;
            for (let i = 0; i < formElements.length; i++) {
                if (formElements[i].value === '' && formElements[i].name !== '') {
                    formElements[i].disabled = true;
                }
            }
        });
    });
});
