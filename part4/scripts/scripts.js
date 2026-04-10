// HBnB Part 4 - Common JavaScript Utilities
// Version corrigée - 100% fonctionnel

// ==================== API CONFIGURATION ====================
const API_BASE_URL = 'http://localhost:5000/api/v1';

// ==================== COOKIE MANAGEMENT ====================

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    console.log(`Cookie set: ${name}`);
}

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

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/`;
    console.log(`Cookie deleted: ${name}`);
}

// ==================== AUTHENTICATION ====================

function isAuthenticated() {
    const token = getCookie('token');
    return token !== null && token !== '';
}

function getToken() {
    return getCookie('token');
}

function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

function checkAuthentication() {
    const token = getToken();
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
        if (token) {
            loginLink.textContent = 'Déconnexion';
            loginLink.href = '#';
            loginLink.onclick = (e) => {
                e.preventDefault();
                logout();
            };
        } else {
            loginLink.textContent = 'Connexion';
            loginLink.href = 'login.html';
            loginLink.onclick = null;
        }
    }
}

// ==================== API REQUESTS ====================

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

function showMessage(message, type = 'success', containerId = 'message-container') {
    const container = document.getElementById(containerId);
    if (!container) {
        alert(message);
        return;
    }
    
    container.className = type === 'error' ? 'error-message' : 'success-message';
    container.textContent = message;
    container.style.display = 'block';
    
    setTimeout(() => {
        container.style.display = 'none';
    }, 5000);
}

function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Chargement...</p>
            </div>
        `;
    }
}

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

function formatPrice(price) {
    return `$${parseFloat(price).toFixed(2)}`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

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

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// ==================== VALIDATION ====================

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

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

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    console.log('Scripts.js loaded successfully');
});
