document.addEventListener('DOMContentLoaded', function() {
    // Header scroll effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile Menu Toggle
    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (menuBtn) {
        menuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            menuBtn.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    const navLinksItems = document.querySelectorAll('.nav-links a');
    navLinksItems.forEach(item => {
        item.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                menuBtn.classList.remove('active');
            }
        });
    });

    // Flash message close
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const flashMessage = this.parentElement;
            flashMessage.style.opacity = '0';
            setTimeout(() => {
                flashMessage.remove();
            }, 300);
        });
    });

    // Fade out flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Demo upload simulation
    const uploadArea = document.querySelector('.upload-area');
    const demoResult = document.querySelector('.demo-result');

    if (uploadArea && demoResult) {
        uploadArea.addEventListener('click', function() {
            // Simulate upload loading
            uploadArea.innerHTML = '<div class="upload-icon"><i class="fas fa-spinner fa-spin"></i></div><p>Processing diagram...</p>';

            // Simulate processing delay
            setTimeout(() => {
                // Show results after "processing"
                demoResult.classList.add('active');
                uploadArea.innerHTML = '<div class="upload-icon"><i class="fas fa-check-circle"></i></div><p>Upload another diagram</p>';

                // Scroll to results
                demoResult.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Initialize the tabs in results
                initResultTabs();
            }, 2000);
        });
    }

    // Demo result tabs
    function initResultTabs() {
        const resultTabs = document.querySelectorAll('.result-tab');
        const resultContents = document.querySelectorAll('.result-content');

        resultTabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const target = this.getAttribute('data-target');

                // Remove active class from all tabs and contents
                resultTabs.forEach(t => t.classList.remove('active'));
                resultContents.forEach(c => c.classList.remove('active'));

                // Add active class to clicked tab and target content
                this.classList.add('active');
                document.querySelector(`.result-content[data-content="${target}"]`).classList.add('active');
            });
        });
    }

    // Animate elements when they come into view
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const animationClass = el.getAttribute('data-animation') || 'fade-in';
                el.classList.add(animationClass);
                observer.unobserve(el);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => {
        observer.observe(el);
    });
});
