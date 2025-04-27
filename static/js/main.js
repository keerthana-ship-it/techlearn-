document.addEventListener('DOMContentLoaded', function() {
    // Apply animations to elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 50) {
                const animationClass = element.getAttribute('data-animation') || 'fadeIn';
                element.classList.add('animate__animated', `animate__${animationClass}`);
                element.classList.remove('animate-on-scroll');
            }
        });
    };
    
    // Check for elements to animate on initial load
    animateOnScroll();
    
    // Continue checking on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Animated counters on stats
    const animateCounters = function() {
        const counters = document.querySelectorAll('.stat-value');
        
        counters.forEach(counter => {
            // Skip if already animated
            if (counter.classList.contains('counted')) return;
            
            const elementTop = counter.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 50) {
                counter.classList.add('counted');
                
                const target = parseInt(counter.textContent);
                const plus = counter.textContent.includes('+') ? '+' : '';
                let count = 0;
                const duration = 1500; // ms
                const increment = Math.ceil(target / (duration / 30)); // Update every 30ms
                
                const updateCount = () => {
                    count += increment;
                    if (count >= target) {
                        counter.textContent = target + plus;
                        clearInterval(timer);
                    } else {
                        counter.textContent = count + plus;
                    }
                };
                
                const timer = setInterval(updateCount, 30);
            }
        });
    };
    
    // Trigger counter animation on page load and scroll
    animateCounters();
    window.addEventListener('scroll', animateCounters);
    
    // Toggle password visibility in forms
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = document.querySelector(this.getAttribute('data-target'));
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Toggle icon with animation
            const icon = this.querySelector('i');
            icon.classList.add('animate__animated', 'animate__flipX');
            
            if (type === 'password') {
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
            
            // Remove animation class after animation completes
            setTimeout(() => {
                icon.classList.remove('animate__animated', 'animate__flipX');
            }, 500);
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
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Enhanced quiz timer functionality
    const quizTimerElement = document.getElementById('quiz-timer');
    if (quizTimerElement) {
        const timeLimit = parseInt(quizTimerElement.getAttribute('data-time-limit'));
        let timeRemaining = timeLimit * 60; // Convert to seconds
        
        const timerInterval = setInterval(function() {
            timeRemaining--;
            
            const minutes = Math.floor(timeRemaining / 60);
            const seconds = timeRemaining % 60;
            
            quizTimerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            
            // Add visual cue when time is running low
            if (timeRemaining <= 60) { // Last minute
                quizTimerElement.classList.add('text-danger');
                quizTimerElement.classList.add('animate__animated', 'animate__pulse');
                quizTimerElement.style.animationIterationCount = 'infinite';
            }
            
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                
                // Show time's up message
                const quizForm = document.getElementById('quiz-form');
                const timeUpMessage = document.createElement('div');
                timeUpMessage.className = 'alert alert-danger animate__animated animate__fadeIn';
                timeUpMessage.textContent = "Time's up! Submitting your answers...";
                quizForm.prepend(timeUpMessage);
                
                // Submit form after showing message
                setTimeout(() => {
                    quizForm.submit();
                }, 1500);
            }
        }, 1000);
    }
    
    // Enhanced AJAX bookmark functionality
    const bookmarkButtons = document.querySelectorAll('.bookmark-button');
    bookmarkButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add loading state
            this.classList.add('disabled');
            const originalContent = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            
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
                    // Remove loading state
                    this.classList.remove('disabled');
                    
                    // Toggle button state
                    this.setAttribute('data-bookmarked', !isBookmarked);
                    
                    // Update button with animation
                    if (!isBookmarked) {
                        this.innerHTML = '<i class="fas fa-bookmark animate__animated animate__bounceIn"></i> <span>Bookmarked</span>';
                        this.classList.remove('btn-outline-primary');
                        this.classList.add('btn-primary');
                    } else {
                        this.innerHTML = '<i class="far fa-bookmark"></i> <span>Bookmark</span>';
                        this.classList.remove('btn-primary');
                        this.classList.add('btn-outline-primary');
                    }
                    
                    // Show enhanced toast notification
                    const toastMessage = !isBookmarked ? 
                        `<i class="fas fa-check-circle text-success me-2"></i>${itemType === 'content' ? 'Content' : 'Event'} bookmarked successfully` : 
                        '<i class="fas fa-info-circle text-info me-2"></i>Bookmark removed';
                    
                    // Create and show enhanced toast
                    const toastContainer = document.getElementById('toast-container');
                    if (toastContainer) {
                        const toastEl = document.createElement('div');
                        toastEl.className = 'toast';
                        toastEl.setAttribute('role', 'alert');
                        toastEl.setAttribute('aria-live', 'assertive');
                        toastEl.setAttribute('aria-atomic', 'true');
                        
                        const toastClass = !isBookmarked ? 'border-success' : 'border-info';
                        const headerClass = !isBookmarked ? 'text-success' : 'text-info';
                        
                        toastEl.innerHTML = `
                            <div class="toast-header ${headerClass}">
                                <strong class="me-auto">TechLearn</strong>
                                <small>Just now</small>
                                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                            <div class="toast-body">
                                ${toastMessage}
                            </div>
                        `;
                        
                        toastEl.classList.add(toastClass, 'animate__animated', 'animate__fadeInRight');
                        
                        toastContainer.appendChild(toastEl);
                        const toast = new bootstrap.Toast(toastEl, {
                            autohide: true,
                            delay: 3000
                        });
                        toast.show();
                    }
                } else {
                    // Handle error
                    this.classList.remove('disabled');
                    this.innerHTML = originalContent;
                    
                    // Show error toast
                    const toastContainer = document.getElementById('toast-container');
                    if (toastContainer) {
                        const toastEl = document.createElement('div');
                        toastEl.className = 'toast border-danger';
                        toastEl.setAttribute('role', 'alert');
                        toastEl.setAttribute('aria-live', 'assertive');
                        toastEl.setAttribute('aria-atomic', 'true');
                        
                        toastEl.innerHTML = `
                            <div class="toast-header text-danger">
                                <strong class="me-auto">Error</strong>
                                <small>Just now</small>
                                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                            <div class="toast-body">
                                <i class="fas fa-exclamation-circle text-danger me-2"></i>
                                Failed to update bookmark. Please try again.
                            </div>
                        `;
                        
                        toastEl.classList.add('animate__animated', 'animate__fadeInRight');
                        
                        toastContainer.appendChild(toastEl);
                        const toast = new bootstrap.Toast(toastEl);
                        toast.show();
                    }
                }
            })
            .catch(error => {
                // Remove loading state
                this.classList.remove('disabled');
                this.innerHTML = originalContent;
                
                console.error('Error:', error);
                
                // Show error toast
                const toastContainer = document.getElementById('toast-container');
                if (toastContainer) {
                    const toastEl = document.createElement('div');
                    toastEl.className = 'toast border-danger';
                    toastEl.innerHTML = `
                        <div class="toast-header text-danger">
                            <strong class="me-auto">Error</strong>
                            <small>Just now</small>
                            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                        <div class="toast-body">
                            <i class="fas fa-exclamation-circle text-danger me-2"></i>
                            Network error. Please check your connection.
                        </div>
                    `;
                    
                    toastContainer.appendChild(toastEl);
                    const toast = new bootstrap.Toast(toastEl);
                    toast.show();
                }
            });
        });
    });
    
    // Enhanced progress tracking for roadmap topics
    const topicCheckboxes = document.querySelectorAll('.topic-checkbox');
    topicCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const topicId = this.getAttribute('data-topic-id');
            const topicRow = document.getElementById(`topic-${topicId}`);
            
            // Submit form to update progress
            const form = document.getElementById(`mark-topic-form-${topicId}`);
            
            // Show loading state
            const loadingIndicator = document.createElement('span');
            loadingIndicator.className = 'ms-2 spinner-border spinner-border-sm text-primary';
            loadingIndicator.setAttribute('role', 'status');
            this.parentNode.appendChild(loadingIndicator);
            
            // Update UI immediately for better UX
            if (this.checked) {
                topicRow.classList.add('topic-completed');
                topicRow.classList.add('animate__animated', 'animate__fadeIn');
                
                // Update progress bar if exists
                const progressBar = document.querySelector('.roadmap-progress-bar');
                if (progressBar) {
                    const currentValue = parseInt(progressBar.getAttribute('aria-valuenow'));
                    const maxValue = parseInt(progressBar.getAttribute('aria-valuemax'));
                    const newValue = currentValue + 1;
                    const percentage = Math.round((newValue / maxValue) * 100);
                    
                    progressBar.style.width = `${percentage}%`;
                    progressBar.setAttribute('aria-valuenow', newValue);
                    
                    // Animation for smooth transition
                    progressBar.style.transition = 'width 0.5s ease-in-out';
                    
                    // Update progress text if exists
                    const progressText = document.querySelector('.progress-text');
                    if (progressText) {
                        progressText.textContent = `${newValue}/${maxValue} completed (${percentage}%)`;
                    }
                }
            } else {
                topicRow.classList.remove('topic-completed');
                
                // Update progress bar if exists
                const progressBar = document.querySelector('.roadmap-progress-bar');
                if (progressBar) {
                    const currentValue = parseInt(progressBar.getAttribute('aria-valuenow'));
                    const maxValue = parseInt(progressBar.getAttribute('aria-valuemax'));
                    const newValue = currentValue - 1;
                    const percentage = Math.round((newValue / maxValue) * 100);
                    
                    progressBar.style.width = `${percentage}%`;
                    progressBar.setAttribute('aria-valuenow', newValue);
                    
                    // Animation for smooth transition
                    progressBar.style.transition = 'width 0.5s ease-in-out';
                    
                    // Update progress text if exists
                    const progressText = document.querySelector('.progress-text');
                    if (progressText) {
                        progressText.textContent = `${newValue}/${maxValue} completed (${percentage}%)`;
                    }
                }
            }
            
            // Submit form via AJAX instead of page reload
            const formData = new FormData(form);
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Remove loading indicator
                loadingIndicator.remove();
                
                // Show success toast notification
                const toastContainer = document.getElementById('toast-container');
                if (toastContainer) {
                    const toastEl = document.createElement('div');
                    toastEl.className = 'toast';
                    toastEl.innerHTML = `
                        <div class="toast-header">
                            <strong class="me-auto">Progress Updated</strong>
                            <small>Just now</small>
                            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                        <div class="toast-body">
                            <i class="fas fa-check-circle text-success me-2"></i>
                            Your progress has been updated.
                        </div>
                    `;
                    
                    toastContainer.appendChild(toastEl);
                    const toast = new bootstrap.Toast(toastEl, {autohide: true, delay: 3000});
                    toast.show();
                }
            })
            .catch(error => {
                // Remove loading indicator
                loadingIndicator.remove();
                console.error('Error:', error);
                
                // Revert changes on error
                this.checked = !this.checked;
                if (this.checked) {
                    topicRow.classList.add('topic-completed');
                } else {
                    topicRow.classList.remove('topic-completed');
                }
                
                // Show error toast
                const toastContainer = document.getElementById('toast-container');
                if (toastContainer) {
                    const toastEl = document.createElement('div');
                    toastEl.className = 'toast border-danger';
                    toastEl.innerHTML = `
                        <div class="toast-header text-danger">
                            <strong class="me-auto">Error</strong>
                            <small>Just now</small>
                            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                        <div class="toast-body">
                            <i class="fas fa-exclamation-circle text-danger me-2"></i>
                            Failed to update progress. Please try again.
                        </div>
                    `;
                    
                    toastContainer.appendChild(toastEl);
                    const toast = new bootstrap.Toast(toastEl);
                    toast.show();
                }
            });
            
            // Prevent form from submitting normally
            return false;
        });
    });
    
    // Filter form enhancements
    const filterForms = document.querySelectorAll('.filter-form');
    filterForms.forEach(form => {
        // Add reset button functionality
        const resetButton = form.querySelector('.reset-filter');
        if (resetButton) {
            resetButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Reset all form fields
                form.reset();
                
                // If using select2 or similar, trigger change event
                const selects = form.querySelectorAll('select');
                selects.forEach(select => {
                    if (select.classList.contains('selectpicker')) {
                        $(select).selectpicker('refresh');
                    }
                });
                
                // Submit the form with reset parameters
                form.submit();
            });
        }
        
        // Enhance form submission
        form.addEventListener('submit', function(e) {
            // Remove empty fields to keep URL clean
            const formElements = this.elements;
            for (let i = 0; i < formElements.length; i++) {
                if (formElements[i].value === '' && formElements[i].name !== '') {
                    formElements[i].disabled = true;
                }
            }
            
            // Add active filters indicators to the results section
            const activeFilters = [];
            for (let i = 0; i < formElements.length; i++) {
                if (formElements[i].value && formElements[i].name && !formElements[i].classList.contains('btn')) {
                    let filterName = formElements[i].name;
                    let filterValue = formElements[i].value;
                    
                    // Format name for display
                    filterName = filterName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    
                    // Handle select elements
                    if (formElements[i].tagName === 'SELECT') {
                        const option = formElements[i].options[formElements[i].selectedIndex];
                        filterValue = option.textContent;
                    }
                    
                    activeFilters.push(`${filterName}: ${filterValue}`);
                }
            }
            
            // Store active filters in sessionStorage for use after page load
            if (activeFilters.length > 0) {
                sessionStorage.setItem('activeFilters', JSON.stringify(activeFilters));
            } else {
                sessionStorage.removeItem('activeFilters');
            }
        });
        
        // Display active filters on page load
        const activeFiltersContainer = document.getElementById('active-filters');
        if (activeFiltersContainer) {
            const storedFilters = sessionStorage.getItem('activeFilters');
            if (storedFilters) {
                const filters = JSON.parse(storedFilters);
                
                if (filters.length > 0) {
                    activeFiltersContainer.innerHTML = '<div class="mb-3"><strong>Active Filters:</strong></div>';
                    const filtersDiv = document.createElement('div');
                    filtersDiv.className = 'd-flex flex-wrap gap-2 mb-4';
                    
                    filters.forEach(filter => {
                        const badge = document.createElement('span');
                        badge.className = 'badge bg-primary';
                        badge.innerHTML = `${filter} <button type="button" class="btn-close btn-close-white ms-2" aria-label="Remove"></button>`;
                        filtersDiv.appendChild(badge);
                    });
                    
                    activeFiltersContainer.appendChild(filtersDiv);
                    activeFiltersContainer.classList.add('animate__animated', 'animate__fadeIn');
                }
            }
        }
    });
});
