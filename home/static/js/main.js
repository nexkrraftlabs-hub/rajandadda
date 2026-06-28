// Rajan Dadda Tours - Main JS

document.addEventListener('DOMContentLoaded', function () {

    // ---- Navbar active link highlight ----
    const currentPath = window.location.pathname;
    document.querySelectorAll('.main-navbar .nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ---- Gallery filter ----
    const filterBtns = document.querySelectorAll('[data-filter]');
    const galleryItems = document.querySelectorAll('[data-category]');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.getAttribute('data-filter');
            galleryItems.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-category') === filter) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // ---- Scroll to top on page load ----
    window.scrollTo(0, 0);

    // ---- Animate stats on scroll ----
    function animateCounter(el, target) {
        let start = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(() => {
            start += step;
            if (start >= target) { el.textContent = target + '+'; clearInterval(timer); }
            else { el.textContent = start + '+'; }
        }, 30);
    }

    const statNums = document.querySelectorAll('.stat-num[data-count]');
    if (statNums.length > 0) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target.querySelector('span') || entry.target;
                    const target = parseInt(entry.target.getAttribute('data-count'));
                    animateCounter(el, target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        statNums.forEach(el => observer.observe(el));
    }

    // ---- Contact form basic validation ----
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const name = document.getElementById('name').value.trim();
            const mobile = document.getElementById('mobile').value.trim();
            const message = document.getElementById('message').value.trim();
            if (!name || !mobile || !message) {
                alert('Please fill all required fields.');
                return;
            }
            // Proceed with AJAX or form action
            alert('Message sent! We will contact you shortly.');
            contactForm.reset();
        });
    }

    // ---- Booking form today-min for date ----
    const dateInput = document.querySelector('input[type="date"]');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }

    // ---- Royal Feature Hover/Click Image Change ----
    const featureItems = document.querySelectorAll('.royal-feature-item');
    const royalImg = document.getElementById('royal-feature-img');
    
    if (featureItems.length > 0 && royalImg) {
        featureItems.forEach(item => {
            // Trigger on both hover and click/touch
            const triggerChange = function() {
                // Remove active class from all
                featureItems.forEach(f => f.classList.remove('active'));
                // Add active to current
                this.classList.add('active');

                const newImgUrl = this.getAttribute('data-image');
                if (royalImg.src !== newImgUrl) {
                    royalImg.style.opacity = '0.5';
                    setTimeout(() => {
                        royalImg.src = newImgUrl;
                        royalImg.style.opacity = '1';
                    }, 150);
                }
            };
            
            item.addEventListener('mouseenter', triggerChange);
            item.addEventListener('click', triggerChange);
            item.addEventListener('touchstart', function(e) {
                // prevent default if we want to avoid double firing with click, but simple is better
                triggerChange.call(this);
            }, {passive: true});
        });
    }

    // ---- Floating button pulse animation ----
    const waBtn = document.querySelector('.whatsapp-float');
    if (waBtn) {
        setInterval(() => {
            waBtn.classList.add('pulse');
            setTimeout(() => waBtn.classList.remove('pulse'), 600);
        }, 3000);
    }

    // ---- Vanilla Tilt Initialization ----
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll(".card-3d, .img-3d, .route-card, .info-card, .vehicle-card"), {
            max: 12,
            speed: 400,
            glare: true,
            "max-glare": 0.15,
        });
    }
});

// Pulse animation
const style = document.createElement('style');
style.textContent = `
.float-btn.pulse {
    box-shadow: 0 0 0 8px rgba(37,211,102,0.2) !important;
    transition: box-shadow 0.3s;
}
`;
document.head.appendChild(style);