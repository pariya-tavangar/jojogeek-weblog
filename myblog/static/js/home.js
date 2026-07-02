// --------------- Screen Loader ------------------
const hasSeenLoader = sessionStorage.getItem("loaderPlayed");

if (!hasSeenLoader) {
    // show loader normally
    window.addEventListener("load", function() {
        const wrapper = document.getElementById("loader-wrapper");
        sessionStorage.setItem("loaderPlayed", "yes");

        setTimeout(() => {
            wrapper.style.opacity = "0";
            setTimeout(() => {
                wrapper.style.display = "none";
            }, 300);
        }, 1800);
    });
} else {
    // user already saw it, hide instantly
    const wrapper = document.getElementById("loader-wrapper");
    wrapper.style.display = "none";
}


// --------------- Dark Mode Toggle ------------------

    // Dark Mode Toggle Functionality
    const themeToggle = document.getElementById('themeToggle');
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');
    const body = document.body;
        
    // Check for saved theme preference or respect OS preference
    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
    // Apply the saved theme
    body.setAttribute('data-theme', savedTheme);
        
    // Toggle theme on button click
    function toggleTheme() {
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }
        
    themeToggle.addEventListener('click', toggleTheme);
    mobileThemeToggle.addEventListener('click', toggleTheme);
        
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    // Only auto-switch if user hasn't manually set a preference
    if (!localStorage.getItem('theme')) {
        body.setAttribute('data-theme', e.matches ? 'dark' : 'light');}
        });
        
    // ---------------- NAV Menu Mobile ----------------------    

    // Mobile Navigation Toggle
    const mobileNavToggle = document.getElementById('mobileNavToggle');
    const mobileNav = document.getElementById('mobileNav');
    const overlay = document.getElementById('overlay');
        
    function toggleMobileNav() {
        mobileNav.classList.toggle('active');
        overlay.classList.toggle('active');
        document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
            
        // Change icon based on menu state
        const icon = mobileNavToggle.querySelector('i');
            if (mobileNav.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
        
    mobileNavToggle.addEventListener('click', toggleMobileNav);
    overlay.addEventListener('click', toggleMobileNav);
        
    // Close mobile menu when clicking on a link
    const mobileNavLinks = document.querySelectorAll('.mobile-nav a');
    mobileNavLinks.forEach(link => {link.addEventListener('click', toggleMobileNav);});
        
    // Close mobile menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
                toggleMobileNav();
            }
        });
        
    // -------------- Buttons Sound Effect -----------------

    // Add some 90s sound effects for buttons
    const buttons = document.querySelectorAll('.btn, .theme-toggle, .mobile-nav-toggle, .read-more, .page-number, .page-nav');
    buttons.forEach(button => {
    button.addEventListener('click', function() {
        // In a real implementation, you could play a sound effect here
        // For now, we'll just add a visual effect
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
            }, 100);
        });
    });


    // ---------------- Scrollbar --------------------
    // Add to your script
    window.addEventListener('scroll', () => {
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('readingProgress').style.width = scrolled + '%';
    });

    // Back to Top Button Functionality
    (function() {
        const backToTopBtn = document.getElementById('backToTop');
    
        if (!backToTopBtn) return;
    
    // Show/hide button based on scroll position
    function toggleBackToTop() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }
    
    // Smooth scroll to top
    function scrollToTop() {
        // Smooth scroll with easing
        const startPosition = window.pageYOffset;
        const duration = 800;
        const startTime = performance.now();
        
        function easeInOutCubic(t) {
            return t < 0.5 
                ? 4 * t * t * t 
                : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }
        
        function scrollAnimation(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = easeInOutCubic(progress);
            
            window.scrollTo(0, startPosition * (1 - easeProgress));
            
            if (progress < 1) {
                requestAnimationFrame(scrollAnimation);
            }
        }
        
        requestAnimationFrame(scrollAnimation);
    }
    
    // Throttle scroll events for performance
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                toggleBackToTop();
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // Click handler
    backToTopBtn.addEventListener('click', scrollToTop);
    
    // Keyboard support
    backToTopBtn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            scrollToTop();
        }
    });
    
    // Show button immediately if page is already scrolled
    toggleBackToTop();
    
    // Optional: Add scroll progress to button
    function updateProgress() {
        const winScroll = document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        
        // Update progress ring if it exists
        const ring = backToTopBtn.querySelector('.progress-ring circle');
        if (ring) {
            const circumference = 2 * Math.PI * 45; // r=45
            ring.style.strokeDashoffset = circumference - (scrolled / 100) * circumference;
        }
    }
    
    // Uncomment to enable progress ring
    // window.addEventListener('scroll', updateProgress);
})();


// ------------------ Floating Header Symbols ----------------------
(function() {
    const header = document.querySelector('header');
    const symbolsContainer = document.createElement('div');
    symbolsContainer.className = 'floating-symbols';
    symbolsContainer.setAttribute('aria-hidden', 'true');
    
    // Symbol options
    const symbolSet = ['✦', '◈', '❖', '✧', '★', '⌘', '♦', '♢', '⚡', '☯', '♠', '♥', '♦', '♣', '✿'];
    
    // Generate random symbols
    const numSymbols = 25; // More symbols for better coverage
    for (let i = 0; i < numSymbols; i++) {
        const span = document.createElement('span');
        span.className = 'symbol';
        span.textContent = symbolSet[Math.floor(Math.random() * symbolSet.length)];
        
        // Random positioning
        span.style.left = Math.random() * 95 + '%';
        span.style.top = Math.random() * 90 + '%';
        span.style.setProperty('--duration', (20 + Math.random() * 20) + 's');
        span.style.setProperty('--delay', (Math.random() * 8) + 's');
        span.style.fontSize = (1.5 + Math.random() * 2) + 'rem'; // Larger symbols
        span.style.opacity = (0.3 + Math.random() * 0.4); // Medium opacity range (0.3 - 0.7)
        
        // Random rotation speed
        const rotationSpeed = (Math.random() - 0.5) * 2;
        span.dataset.rotation = rotationSpeed;
        
        // Random movement path
        span.dataset.driftX = (Math.random() - 0.5) * 100;
        span.dataset.driftY = (Math.random() - 0.5) * 100;
        
        symbolsContainer.appendChild(span);
    }
    
    // Insert into header
    const headerContent = header.querySelector('.header-content');
    if (headerContent) {
        header.insertBefore(symbolsContainer, headerContent);
    } else {
        header.prepend(symbolsContainer);
    }
    
    // Advanced animation with smooth drift
    let symbols = symbolsContainer.querySelectorAll('.symbol');
    
    function animateSymbols() {
        symbols.forEach((symbol, index) => {
            const rect = symbol.getBoundingClientRect();
            const parentRect = symbol.parentElement.getBoundingClientRect();
            
            // Create a subtle floating effect using multiple sine waves
            const time = Date.now() / 1000;
            const speed = parseFloat(symbol.style.getPropertyValue('--duration')) || 25;
            const offsetX = Math.sin(time / speed * 2 + index) * 25;
            const offsetY = Math.cos(time / speed * 1.5 + index * 1.2) * 25;
            const rotation = Math.sin(time / speed * 3 + index * 0.5) * 20;
            
            // Apply transform with smooth interpolation
            symbol.style.transform = `
                translate(${offsetX}px, ${offsetY}px) 
                rotate(${rotation}deg)
            `;
            
            // Pulsing opacity - medium range
            const opacityBase = 0.3 + (index % 5) * 0.05;
            const opacityPulse = Math.sin(time / 2 + index) * 0.15 + 0.15;
            symbol.style.opacity = Math.min(opacityBase + opacityPulse, 0.7);
        });
        
        requestAnimationFrame(animateSymbols);
    }
    
    // Start animation
    animateSymbols();
    
    // Update on resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            symbols = symbolsContainer.querySelectorAll('.symbol');
        }, 500);
    });
})();

