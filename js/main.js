// Main functionality for interactions

document.addEventListener('DOMContentLoaded', () => {
    // Contact form submission via API
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button');
            const originalText = btn.innerText;
            btn.innerText = 'Sending...';
            
            try {
                const formData = new FormData(contactForm);
                const data = Object.fromEntries(formData.entries());
                
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    btn.innerText = 'Message Sent!';
                    btn.style.background = '#00f3ff';
                    btn.style.color = '#000';
                    contactForm.reset();
                } else {
                    btn.innerText = 'Error Sending';
                    btn.style.background = 'var(--neon-red)';
                }
            } catch (err) {
                console.error('Contact form error:', err);
                btn.innerText = 'Network Error';
            }
            
            setTimeout(() => {
                btn.innerText = originalText;
                // Note: The original color relies on stylesheet inheritance or var(--neon-red). 
                // We'll reset it to empty so it falls back to stylesheet
                btn.style.background = '';
                btn.style.color = '';
            }, 3000);
        });
    }

    // Scroll Animations (Simple Intersection Observer)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }
        });
    }, { threshold: 0.1 });

// Initialize elements with fade-in setup
    document.querySelectorAll('.glass-panel, .section-title, .sdg-section').forEach(el => {
        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
        observer.observe(el);
    });
});
