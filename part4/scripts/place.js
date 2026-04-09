// HBnB Part 4 - Place Details Page JavaScript (TASK 3)
// Author: Holberton School Project
// Description: Display place details, reviews, and handle review submission

document.addEventListener('DOMContentLoaded', () => {
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        alert('No place specified');
        window.location.href = 'index.html';
        return;
    }
    
    // Check authentication
    const token = getToken();
    const addReviewSection = document.getElementById('add-review');
    
    if (addReviewSection) {
        if (token) {
            // User is authenticated - show review form
            addReviewSection.style.display = 'block';
            setupReviewForm(placeId, token);
        } else {
            // User not authenticated - hide review form
            addReviewSection.style.display = 'none';
        }
    }
    
    // Load place details and reviews
    loadPlaceDetails(placeId);
    loadReviews(placeId);
});

// ==================== GET PLACE ID FROM URL ====================

/**
 * Extract place ID from URL query parameters
 * @returns {string|null} Place ID or null
 */
function getPlaceIdFromURL() {
    return getQueryParam('id');
}

// ==================== LOAD PLACE DETAILS ====================

/**
 * Fetch place details from API
 * @param {string} placeId - Place ID
 */
async function loadPlaceDetails(placeId) {
    const placeDetailsContainer = document.getElementById('place-details');
    
    if (!placeDetailsContainer) return;
    
    // Show loading
    showLoading('place-details');
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
        
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            placeDetailsContainer.innerHTML = `
                <div class="error-message">
                    <p>Place not found.</p>
                    <a href="index.html" class="btn-secondary">Back to Places</a>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading place details:', error);
        placeDetailsContainer.innerHTML = `
            <div class="error-message">
                <p>Unable to load place details. Please try again later.</p>
                <a href="index.html" class="btn-secondary">Back to Places</a>
            </div>
        `;
    }
}

// ==================== DISPLAY PLACE DETAILS ====================

/**
 * Display place details in the DOM
 * @param {Object} place - Place object
 */
function displayPlaceDetails(place) {
    const placeDetailsContainer = document.getElementById('place-details');
    
    if (!placeDetailsContainer) return;
    
    // Get data
    const imageUrl = place.image_url || 'images/placeholder.svg';
    const rating = place.average_rating || 0;
    const ratingStars = createStarRating(rating);
    
    // Build amenities HTML
    const amenitiesHTML = place.amenities && place.amenities.length > 0
        ? place.amenities.map(amenity => 
            `<span class="amenity-tag">${escapeHtml(amenity.name)}</span>`
          ).join('')
        : '<p>No amenities listed</p>';
    
    // Get location
    const cityName = place.city ? escapeHtml(place.city.name) : 'Unknown';
    const countryName = place.city && place.city.country ? escapeHtml(place.city.country.name) : '';
    
    // Get host name
    const hostName = place.host 
        ? escapeHtml(`${place.host.first_name} ${place.host.last_name}`)
        : 'Unknown';
    
    // Build HTML
    placeDetailsContainer.innerHTML = `
        <div class="place-info">
            <img src="${imageUrl}" 
                 alt="${escapeHtml(place.name)}" 
                 style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 10px; margin-bottom: 20px;" 
                 onerror="this.src='images/placeholder.svg'">
            
            <h1>${escapeHtml(place.name)}</h1>
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0; flex-wrap: wrap; gap: 15px;">
                <p class="rating" style="font-size: 18px;">
                    ${ratingStars} ${rating > 0 ? rating.toFixed(1) : 'No reviews yet'}
                </p>
                <p class="price" style="font-size: 28px; font-weight: bold;">
                    ${formatPrice(place.price_per_night)}
                    <span style="font-size: 16px; font-weight: normal;">/night</span>
                </p>
            </div>
            
            <div style="margin: 20px 0; padding: 20px; background: #f7f7f7; border-radius: 8px;">
                <p><strong>📍 Location:</strong> ${cityName}${countryName ? ', ' + countryName : ''}</p>
                ${place.address ? `<p><strong>🏠 Address:</strong> ${escapeHtml(place.address)}</p>` : ''}
                <p><strong>👤 Host:</strong> <span class="host">${hostName}</span></p>
                <p><strong>👥 Max Guests:</strong> ${place.max_guests} guests</p>
                <p><strong>🛏️ Rooms:</strong> ${place.number_of_rooms} | <strong>🚿 Bathrooms:</strong> ${place.number_of_bathrooms}</p>
            </div>
            
            ${place.description ? `
                <div style="margin: 20px 0;">
                    <h3>About this place</h3>
                    <p style="line-height: 1.8; color: #484848;">${escapeHtml(place.description)}</p>
                </div>
            ` : ''}
            
            <div style="margin: 20px 0;">
                <h3>Amenities</h3>
                <div class="amenities-list">
                    ${amenitiesHTML}
                </div>
            </div>
        </div>
    `;
}

// ==================== LOAD REVIEWS ====================

/**
 * Fetch reviews for a place
 * @param {string} placeId - Place ID
 */
async function loadReviews(placeId) {
    const reviewsContainer = document.getElementById('reviews-list');
    
    if (!reviewsContainer) return;
    
    // Show loading
    reviewsContainer.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading reviews...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
        
        if (response.ok) {
            const data = await response.json();
            const reviews = data.reviews || data || [];
            displayReviews(reviews);
        } else {
            reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
        reviewsContainer.innerHTML = '<p>Unable to load reviews.</p>';
    }
}

// ==================== DISPLAY REVIEWS ====================

/**
 * Display reviews in the DOM
 * @param {Array} reviews - Array of review objects
 */
function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews-list');
    
    if (!reviewsContainer) return;
    
    if (!reviews || reviews.length === 0) {
        reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review this place!</p>';
        return;
    }
    
    reviewsContainer.innerHTML = '';
    
    reviews.forEach(review => {
        const reviewCard = createReviewCard(review);
        reviewsContainer.appendChild(reviewCard);
    });
}

// ==================== CREATE REVIEW CARD ====================

/**
 * Create a review card element
 * @param {Object} review - Review object
 * @returns {HTMLElement} Review card element
 */
function createReviewCard(review) {
    const card = document.createElement('div');
    card.className = 'review-card';
    
    const stars = createStarRating(review.rating);
    const userName = review.user 
        ? escapeHtml(`${review.user.first_name} ${review.user.last_name}`)
        : 'Anonymous';
    const reviewDate = review.created_at ? formatDate(review.created_at) : '';
    
    card.innerHTML = `
        <div class="review-header">
            <span class="review-author">${userName}</span>
            <span class="review-rating">${stars}</span>
        </div>
        <p class="review-comment">${escapeHtml(review.comment)}</p>
        ${reviewDate ? `<p class="review-date">${reviewDate}</p>` : ''}
    `;
    
    return card;
}

// ==================== SETUP REVIEW FORM ====================

/**
 * Setup review form submission
 * @param {string} placeId - Place ID
 * @param {string} token - JWT token
 */
function setupReviewForm(placeId, token) {
    const reviewForm = document.getElementById('review-form');
    
    if (!reviewForm) return;
    
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        // Get form values
        const rating = document.getElementById('review-rating').value;
        const comment = document.getElementById('review-text').value.trim();
        
        // Validate
        if (!rating || !comment) {
            alert('Please provide both a rating and a comment.');
            return;
        }
        
        if (comment.length < 10) {
            alert('Review comment must be at least 10 characters long.');
            return;
        }
        
        // Disable submit button
        const submitButton = reviewForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Submitting...';
        
        try {
            const response = await fetchWithAuth('/reviews', {
                method: 'POST',
                body: JSON.stringify({
                    place_id: placeId,
                    rating: parseInt(rating),
                    comment: comment
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                alert('Review submitted successfully!');
                reviewForm.reset();
                
                // Reload reviews and place details
                loadReviews(placeId);
                loadPlaceDetails(placeId);
            } else {
                alert(data.error || 'Failed to submit review. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('Unable to submit review. Please try again later.');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
}
