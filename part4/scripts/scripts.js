// HBnB Part 4 - Common JavaScript Utilities
// Author: Holberton School Project
// Description: Common functions for authentication, API calls, and UI helpers

// ==================== API CONFIGURATION ====================

const API_BASE_URL = 'http://localhost:5000/api/v1';

// ==================== COOKIE MANAGEMENT ====================

/**
 * Set a cookie
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Expiration in days (default: 7)
 */
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

/**
 * Delete a cookie
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/`;
}

// ==================== AUTHENTICATION ====================

/**
 * Check if user is authenticated
 * @returns {boolean} True if authenticated
 */
function isAuthenticated() {
    const token = getCookie('token');
    return token !== null && token !== '';
}

/**
 * Get authentication token
 * @returns {string|null} JWT token or null
 */
function getToken() {
    return getCookie('token');
}

/**
 * Logout user
 */
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

/**
 * Check authentication and update UI
 */
function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (token) {
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.onclick = (e) => {
                e.preventDefault();
                logout();
            };
        } else {
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
            loginLink.onclick = null;
        }
    }
}

// ==================== API REQUESTS ====================

/**
 * Make authenticated API request
 * @param {string} endpoint - API endpoint path
 * @param {object} options - Fetch options
 * @returns {Promise<Response>} Fetch response
 */
async function fetchWithAuth(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    return fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });
}

// ==================== UI UTILITIES ====================

/**
 * Show message to user
 * @param {string} message - Message text
 * @param {string} type - Message type ('success' or 'error')
 * @param {string} containerId - Container element ID
 */
function showMessage(message, type = 'success', containerId = 'message-container') {
    const container = document.getElementById(containerId);
    if (!container) {
        alert(message);
        return;
    }
    
    container.className = type === 'error' ? 'error-message' : 'success-message';
    container.textContent = message;
    container.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        container.style.display = 'none';
    }, 5000);
}

/**
 * Show loading spinner
 * @param {string} containerId - Container element ID
 */
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
        `;
    }
}

/**
 * Hide loading spinner
 * @param {string} containerId - Container element ID
 */
function hideLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        const loading = container.querySelector('.loading');
        if (loading) {
            loading.remove();
        }
    }
}

// ==================== FORMATTING UTILITIES ====================

/**
 * Format price for display
 * @param {number} price - Price value
 * @returns {string} Formatted price
 */
function formatPrice(price) {
    return `$${parseFloat(price).toFixed(2)}`;
}

/**
 * Format date for display
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Create star rating HTML
 * @param {number} rating - Rating value (1-5)
 * @returns {string} Star string
 */
function createStarRating(rating) {
    const fullStars = Math.floor(rating);
    const emptyStars = 5 - fullStars;
    
    let stars = '';
    for (let i = 0; i < fullStars; i++) {
        stars += '⭐';
    }
    for (let i = 0; i < emptyStars; i++) {
        stars += '☆';
    }
    
    return stars;
}

// ==================== URL UTILITIES ====================

/**
 * Get query parameter from URL
 * @param {string} param - Parameter name
 * @returns {string|null} Parameter value or null
 */
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// ==================== VALIDATION ====================

/**
 * Validate email format
 * @param {string} email - Email address
 * @returns {boolean} True if valid
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// ==================== INITIALIZATION ====================

// Run on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
});
