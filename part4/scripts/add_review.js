// HBnB Part 4 - Add Review Page JavaScript (TASK 4)
// Author: Holberton School Project
// Description: Handle add review form submission with authentication check

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication - redirect if not logged in
    const token = checkAuthenticationForReview();
    
    if (!token) {
        return; // Already redirected by checkAuthenticationForReview
    }
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        alert('No place specified');
        window.location.href = 'index.html';
        return;
    }
    
    // Setup character counter
    setupCharacterCounter();
    
    // Setup form submission
    setupReviewFormSubmission(placeId, token);
});

// ==================== CHECK AUTHENTICATION ====================

/**
 * Check if user is authenticated, redirect if not
 * @returns {string|null} Token or null
 */
function checkAuthenticationForReview() {
    const token = getToken();
    
    if (!token) {
        alert('You must be logged in to add a review');
        window.location.href = 'index.html';
        return null;
    }
    
    return token;
}

// ==================== GET PLACE ID ====================

/**
 * Get place ID from URL query parameters
 * @returns {string|null} Place ID or null
 */
function getPlaceIdFromURL() {
    return getQueryParam('place_id');
}

// ==================== CHARACTER COUNTER ====================

/**
 * Setup real-time character counter for textarea
 */
function setupCharacterCounter() {
    const commentTextarea = document.getElementById('comment');
    const charCount = document.getElementById('char-count');
    
    if (commentTextarea && charCount) {
        commentTextarea.addEventListener('input', () => {
            const count = commentTextarea.value.length;
            charCount.textContent = count;
            
            // Change color based on count
            if (count > 900) {
                charCount.style.color = '#c00';
                charCount.style.fontWeight = 'bold';
            } else if (count > 800) {
                charCount.style.color = '#f90';
                charCount.style.fontWeight = 'bold';
            } else {
                charCount.style.color = '#767676';
                charCount.style.fontWeight = 'normal';
            }
        });
    }
}

// ==================== FORM SUBMISSION ====================

/**
 * Setup review form submission with validation
 * @param {string} placeId - Place ID
 * @param {string} token - JWT token
 */
function setupReviewFormSubmission(placeId, token) {
    const reviewForm = document.getElementById('review-form');
    
    if (!reviewForm) return;
    
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        // Get form values
        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value.trim();
        
        // ==================== VALIDATION ====================
        
        if (!rating) {
            showMessage('Please select a rating', 'error');
            return;
        }
        
        if (!comment) {
            showMessage('Please write a review comment', 'error');
            return;
        }
        
        if (comment.length < 10) {
            showMessage('Review comment must be at least 10 characters long', 'error');
            return;
        }
        
        if (comment.length > 1000) {
            showMessage('Review comment must not exceed 1000 characters', 'error');
            return;
        }
        
        // Validate rating is between 1-5
        const ratingValue = parseInt(rating);
        if (ratingValue < 1 || ratingValue > 5) {
            showMessage('Rating must be between 1 and 5', 'error');
            return;
        }
        
        // ==================== SUBMIT REVIEW ====================
        
        // Disable submit button and show loading
        const submitButton = reviewForm.querySelector('button[type="submit"]');
        const originalButtonHTML = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                <div class="spinner" style="width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite;"></div>
                Submitting...
            </div>
        `;
        
        try {
            const response = await fetchWithAuth('/reviews', {
                method: 'POST',
                body: JSON.stringify({
                    place_id: placeId,
                    rating: ratingValue,
                    comment: comment
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Success
                showMessage('Review submitted successfully! Redirecting...', 'success');
                
                // Clear form
                reviewForm.reset();
                document.getElementById('char-count').textContent = '0';
                
                // Redirect to place details after 2 seconds
                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 2000);
            } else {
                // Error from API
                const errorMsg = data.error || 'Failed to submit review. Please try again.';
                showMessage(errorMsg, 'error');
                
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonHTML;
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            showMessage('Unable to submit review. Please check your connection and try again.', 'error');
            
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.innerHTML = originalButtonHTML;
        }
    });
}
