// HBnB Part 4 - Index Page JavaScript (TASK 2)
// Author: Holberton School Project
// Description: Display places list with client-side price filtering

document.addEventListener('DOMContentLoaded', () => {
    const priceFilter = document.getElementById('price-filter');
    let allPlaces = []; // Store all places for filtering
    
    // Load places on page load
    loadPlaces();
    
    // Setup price filter event listener
    if (priceFilter) {
        priceFilter.addEventListener('change', () => {
            filterPlacesByPrice();
        });
    }
    
    // ==================== LOAD PLACES FROM API ====================
    
    /**
     * Fetch all places from API
     */
    async function loadPlaces() {
        const placesContainer = document.getElementById('places-list');
        
        if (!placesContainer) return;
        
        // Show loading state
        showLoading('places-list');
        
        try {
            const response = await fetch(`${API_BASE_URL}/places`);
            
            if (response.ok) {
                const data = await response.json();
                allPlaces = data.places || data || [];
                displayPlaces(allPlaces);
            } else {
                placesContainer.innerHTML = `
                    <div class="error-message">
                        <p>Failed to load places. Please try again later.</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading places:', error);
            placesContainer.innerHTML = `
                <div class="error-message">
                    <p>Unable to connect to the server. Please try again later.</p>
                </div>
            `;
        }
    }
    
    // ==================== DISPLAY PLACES ====================
    
    /**
     * Display places in the DOM
     * @param {Array} places - Array of place objects
     */
    function displayPlaces(places) {
        const placesContainer = document.getElementById('places-list');
        
        if (!placesContainer) return;
        
        // Clear container
        placesContainer.innerHTML = '';
        
        // Check if places exist
        if (!places || places.length === 0) {
            placesContainer.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                    <p style="color: #767676; font-size: 18px;">No places found matching your criteria.</p>
                </div>
            `;
            return;
        }
        
        // Create place cards
        places.forEach(place => {
            const placeCard = createPlaceCard(place);
            placesContainer.appendChild(placeCard);
        });
    }
    
    // ==================== CREATE PLACE CARD ====================
    
    /**
     * Create a place card element
     * @param {Object} place - Place object
     * @returns {HTMLElement} Place card element
     */
    function createPlaceCard(place) {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price_per_night);
        
        // Get image URL or use placeholder
        const imageUrl = place.image_url || 'images/placeholder.svg';
        
        // Calculate rating
        const rating = place.average_rating || 0;
        const ratingStars = createStarRating(rating);
        
        // Get location
        const location = place.city ? escapeHtml(place.city.name) : 'Unknown';
        
        // Build card HTML
        card.innerHTML = `
            <img src="${imageUrl}" alt="${escapeHtml(place.name)}" onerror="this.src='images/placeholder.svg'">
            <h3>${escapeHtml(place.name)}</h3>
            <p class="place-location">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16" style="vertical-align: middle;">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                ${location}
            </p>
            ${place.description ? `<p class="place-description">${escapeHtml(place.description.substring(0, 100))}${place.description.length > 100 ? '...' : ''}</p>` : ''}
            <div class="place-info">
                <p class="rating">${ratingStars} ${rating > 0 ? rating.toFixed(1) : 'New'}</p>
                <p class="price">${formatPrice(place.price_per_night)}<span>/night</span></p>
            </div>
            <button class="details-button" onclick="viewPlaceDetails('${place.id}')">
                View Details
            </button>
        `;
        
        return card;
    }
    
    // ==================== CLIENT-SIDE FILTERING ====================
    
    /**
     * Filter places by selected price
     */
    function filterPlacesByPrice() {
        const selectedPrice = priceFilter.value;
        
        let filteredPlaces = allPlaces;
        
        // Apply filter if not "all"
        if (selectedPrice !== 'all') {
            const maxPrice = parseFloat(selectedPrice);
            filteredPlaces = allPlaces.filter(place => {
                return parseFloat(place.price_per_night) <= maxPrice;
            });
        }
        
        // Display filtered places
        displayPlaces(filteredPlaces);
    }
});

// ==================== GLOBAL FUNCTIONS ====================

/**
 * Navigate to place details page
 * @param {string} placeId - Place ID
 */
function viewPlaceDetails(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}
