// HBnB Part 4 - Login Page JavaScript
// Version corrigée - 100% fonctionnel

console.log('Login.js loaded');

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded for login page');
    
    const loginForm = document.getElementById('login-form');
    const togglePasswordBtn = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('error-message');
    
    // ==================== PASSWORD TOGGLE ====================
    
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Update icon
            const svg = togglePasswordBtn.querySelector('svg');
            if (type === 'text') {
                // Eye slash (password visible)
                svg.innerHTML = '<path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/>';
            } else {
                // Eye icon (password hidden)
                svg.innerHTML = '<path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>';
            }
        });
    }
    
    // ==================== FORM SUBMISSION ====================
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Form submitted');
            
            // Get form values
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            console.log('Email:', email);
            
            // Clear previous errors
            if (errorMessage) {
                errorMessage.style.display = 'none';
            }
            
            // Validate inputs
            if (!email || !password) {
                showError('Veuillez remplir tous les champs');
                return;
            }
            
            if (!validateEmail(email)) {
                showError('Veuillez entrer une adresse email valide');
                return;
            }
            
            // Disable submit button and show loading
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalButtonHTML = submitButton.innerHTML;
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <div class="spinner" style="width: 20px; height: 20px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.6s linear infinite;"></div>
                    Connexion...
                </div>
            `;
            
            try {
                console.log('Calling API:', `${API_BASE_URL}/auth/login`);
                
                // Call login API
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        email: email, 
                        password: password 
                    })
                });
                
                console.log('Response status:', response.status);
                
                const data = await response.json();
                console.log('Response data:', data);
                
                if (response.ok && data.access_token) {
                    console.log('Login successful!');
                    
                    // Store JWT token in cookie
                    setCookie('token', data.access_token, 7);
                    
                    // Show success message
                    showError('Connexion réussie! Redirection...');
                    
                    // Redirect to index page after short delay
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                    
                } else {
                    // Login failed
                    console.error('Login failed:', data);
                    const errorMsg = data.error || data.message || 'Email ou mot de passe incorrect';
                    showError(errorMsg);
                    
                    // Re-enable submit button
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalButtonHTML;
                }
                
            } catch (error) {
                console.error('Login error:', error);
                showError('Impossible de se connecter au serveur. Vérifiez que l\'API est lancée sur le port 5000.');
                
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonHTML;
            }
        });
    }
    
    // ==================== HELPER FUNCTION ====================
    
    function showError(message) {
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 5000);
        } else {
            alert(message);
        }
    }
});
