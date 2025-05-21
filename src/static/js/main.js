/**
 * Main JavaScript for Coco Bambu Alphaville Buffet Evaluation Site
 * Follows principles of modern web development with focus on interactivity and user experience
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initNavigation();
    initAnimations();
    initRatingSystem();
    initFormValidation();
    initFilterSystem();
});

/**
 * Mobile navigation toggle
 */
function initNavigation() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('nav ul');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate hamburger to X
            const spans = menuToggle.querySelectorAll('span');
            spans.forEach(span => span.classList.toggle('active'));
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('nav') && !event.target.closest('.menu-toggle')) {
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    const spans = menuToggle.querySelectorAll('span');
                    spans.forEach(span => span.classList.remove('active'));
                }
            }
        });
    }
}

/**
 * Scroll animations for elements
 */
function initAnimations() {
    // Animate elements when they come into view
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Star rating system functionality
 */
function initRatingSystem() {
    const ratingInputs = document.querySelectorAll('.rating input');
    
    if (ratingInputs.length > 0) {
        ratingInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Update visual feedback
                const categoryId = this.getAttribute('name');
                const ratingValue = this.value;
                const ratingDisplay = document.querySelector(`.rating-value[data-category="${categoryId}"]`);
                
                if (ratingDisplay) {
                    ratingDisplay.textContent = ratingValue;
                }
                
                // Calculate and update average rating if needed
                updateAverageRating();
            });
        });
    }
}

/**
 * Calculate and update the average rating across all categories
 */
function updateAverageRating() {
    const ratingCategories = document.querySelectorAll('.rating-category');
    let totalRating = 0;
    let ratedCategories = 0;
    
    ratingCategories.forEach(category => {
        const checkedInput = category.querySelector('input:checked');
        if (checkedInput) {
            totalRating += parseInt(checkedInput.value);
            ratedCategories++;
        }
    });
    
    const averageRatingElement = document.getElementById('average-rating');
    if (averageRatingElement && ratedCategories > 0) {
        const average = (totalRating / ratedCategories).toFixed(1);
        averageRatingElement.textContent = average;
    }
}

/**
 * Form validation for the evaluation form
 */
function initFormValidation() {
    const evaluationForm = document.getElementById('evaluation-form');
    
    if (evaluationForm) {
        evaluationForm.addEventListener('submit', function(e) {
            let isValid = true;
            const errorMessages = [];
            
            // Check if at least one rating is selected
            const hasRating = document.querySelector('.rating input:checked');
            if (!hasRating) {
                isValid = false;
                errorMessages.push('Por favor, avalie pelo menos uma categoria.');
            }
            
            // Check if comment is provided and has minimum length
            const commentField = document.getElementById('comment');
            if (commentField && commentField.value.trim().length < 10) {
                isValid = false;
                errorMessages.push('Por favor, deixe um comentário com pelo menos 10 caracteres.');
            }
            
            // Check name field
            const nameField = document.getElementById('name');
            if (nameField && nameField.value.trim() === '') {
                isValid = false;
                errorMessages.push('Por favor, informe seu nome.');
            }
            
            // If form is invalid, prevent submission and show errors
            if (!isValid) {
                e.preventDefault();
                
                // Display error messages
                const errorContainer = document.getElementById('form-errors');
                if (errorContainer) {
                    errorContainer.innerHTML = '';
                    errorMessages.forEach(message => {
                        const errorElement = document.createElement('p');
                        errorElement.textContent = message;
                        errorElement.classList.add('error-message');
                        errorContainer.appendChild(errorElement);
                    });
                    
                    // Scroll to error messages
                    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }
}

/**
 * Filter system for feedback display
 */
function initFilterSystem() {
    const filterForm = document.getElementById('feedback-filter');
    
    if (filterForm) {
        // Handle filter changes
        const filterInputs = filterForm.querySelectorAll('select, input');
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                applyFilters();
            });
        });
        
        // Handle filter form submission
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            applyFilters();
        });
    }
}

/**
 * Apply filters to feedback items
 */
function applyFilters() {
    const ratingFilter = document.getElementById('rating-filter');
    const dateFilter = document.getElementById('date-filter');
    const categoryFilter = document.getElementById('category-filter');
    
    const feedbackItems = document.querySelectorAll('.feedback-item');
    
    feedbackItems.forEach(item => {
        let showItem = true;
        
        // Apply rating filter
        if (ratingFilter && ratingFilter.value !== '') {
            const itemRating = parseInt(item.getAttribute('data-rating'));
            const filterValue = parseInt(ratingFilter.value);
            
            if (itemRating < filterValue) {
                showItem = false;
            }
        }
        
        // Apply date filter
        if (dateFilter && dateFilter.value !== '') {
            const itemDate = new Date(item.getAttribute('data-date'));
            const filterDate = new Date();
            
            switch (dateFilter.value) {
                case 'week':
                    filterDate.setDate(filterDate.getDate() - 7);
                    break;
                case 'month':
                    filterDate.setMonth(filterDate.getMonth() - 1);
                    break;
                case 'year':
                    filterDate.setFullYear(filterDate.getFullYear() - 1);
                    break;
            }
            
            if (itemDate < filterDate) {
                showItem = false;
            }
        }
        
        // Apply category filter
        if (categoryFilter && categoryFilter.value !== '') {
            if (!item.classList.contains(`category-${categoryFilter.value}`)) {
                showItem = false;
            }
        }
        
        // Show or hide item based on filters
        item.style.display = showItem ? 'block' : 'none';
    });
    
    // Update results count
    updateResultsCount();
}

/**
 * Update the count of visible feedback items
 */
function updateResultsCount() {
    const visibleItems = document.querySelectorAll('.feedback-item[style="display: block;"]');
    const countElement = document.getElementById('results-count');
    
    if (countElement) {
        countElement.textContent = visibleItems.length;
    }
}

/**
 * Image gallery functionality for menu items
 */
function initImageGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    if (galleryItems.length > 0) {
        galleryItems.forEach(item => {
            item.addEventListener('click', function() {
                const imgSrc = this.querySelector('img').getAttribute('src');
                const imgAlt = this.querySelector('img').getAttribute('alt');
                
                // Create modal with full-size image
                const modal = document.createElement('div');
                modal.classList.add('image-modal');
                
                const modalContent = document.createElement('div');
                modalContent.classList.add('modal-content');
                
                const closeBtn = document.createElement('span');
                closeBtn.classList.add('close-modal');
                closeBtn.innerHTML = '&times;';
                
                const img = document.createElement('img');
                img.setAttribute('src', imgSrc);
                img.setAttribute('alt', imgAlt);
                
                const caption = document.createElement('p');
                caption.textContent = imgAlt;
                
                modalContent.appendChild(closeBtn);
                modalContent.appendChild(img);
                modalContent.appendChild(caption);
                modal.appendChild(modalContent);
                
                document.body.appendChild(modal);
                
                // Prevent scrolling when modal is open
                document.body.style.overflow = 'hidden';
                
                // Close modal functionality
                closeBtn.addEventListener('click', function() {
                    document.body.removeChild(modal);
                    document.body.style.overflow = 'auto';
                });
                
                // Close modal when clicking outside content
                modal.addEventListener('click', function(e) {
                    if (e.target === modal) {
                        document.body.removeChild(modal);
                        document.body.style.overflow = 'auto';
                    }
                });
            });
        });
    }
}
