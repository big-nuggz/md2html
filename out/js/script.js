// md2html - Static site JavaScript
// Provides interactive features for the generated pages.

(function () {
    'use strict';

    // --- Side Navigation: highlight current page ---
    var navTreeContainer = document.getElementById('sideNavTree');
    var navToggle = document.getElementById('navToggle');
    var sideNav = document.getElementById('sideNav');
    var navOverlay = document.getElementById('navOverlay');

    if (navTreeContainer) {
        highlightCurrentPage();
        setupNavFolderPersistence();
    }

    function setSideNavOpen(open) {
        if (open) {
            sideNav.classList.remove('-translate-x-full');
            sideNav.classList.add('translate-x-0');
            navOverlay.classList.remove('opacity-0', 'pointer-events-none');
            navOverlay.classList.add('opacity-100');
            document.body.classList.add('overflow-hidden', 'lg:overflow-auto');
        } else {
            sideNav.classList.remove('translate-x-0');
            sideNav.classList.add('-translate-x-full');
            navOverlay.classList.remove('opacity-100');
            navOverlay.classList.add('opacity-0', 'pointer-events-none');
            document.body.classList.remove('overflow-hidden', 'lg:overflow-auto');
        }
    }

    function highlightCurrentPage() {
        var currentPath = window.location.pathname;
        var idx = currentPath.indexOf('/files/');
        var relativeUrl;
        if (idx !== -1) {
            relativeUrl = currentPath.substring(idx + 1);
        } else {
            return;
        }

        var links = navTreeContainer.querySelectorAll('.nav-link');
        for (var i = 0; i < links.length; i++) {
            var link = links[i];
            var href = link.getAttribute('href');
            // Extract relative URL from href (remove any ../ prefixes)
            var cleanHref = href.replace(/^(\.\.\/)+/, '');
            if (cleanHref === relativeUrl) {
                link.classList.add('current');
                var parent = link.parentElement;
                while (parent) {
                    if (parent.tagName === 'DETAILS') {
                        parent.setAttribute('open', '');
                    }
                    parent = parent.parentElement;
                }
                break;
            }
        }
    }

    function setupNavFolderPersistence() {
        var details = navTreeContainer.querySelectorAll('.nav-details');
        details.forEach(function (d) {
            var summary = d.querySelector('summary');
            if (summary) {
                var key = 'nav_folder_' + summary.textContent.trim();
                var saved = localStorage.getItem(key);
                if (saved === 'closed') {
                    d.removeAttribute('open');
                }
                d.addEventListener('toggle', function () {
                    localStorage.setItem(key, d.open ? 'open' : 'closed');
                });
            }
        });
    }

    // --- Toggle sidebar navigation ---
    if (navToggle && sideNav && navOverlay) {
        navToggle.addEventListener('click', function () {
            var isOpen = sideNav.classList.contains('translate-x-0');
            setSideNavOpen(!isOpen);
        });

        navOverlay.addEventListener('click', function () {
            setSideNavOpen(false);
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && sideNav.classList.contains('translate-x-0')) {
                setSideNavOpen(false);
            }
        });

        navTreeContainer.addEventListener('click', function (e) {
            if (e.target.tagName === 'A') {
                setSideNavOpen(false);
            }
        });
    }

    // --- Keyboard shortcuts ---
    document.addEventListener('keydown', function (e) {
        if (e.key === 'h' && !e.ctrlKey && !e.metaKey && !e.altKey) {
            var target = e.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') return;
            var homeLink = document.querySelector('.nav-home');
            if (homeLink) {
                e.preventDefault();
                window.location.href = homeLink.getAttribute('href');
            }
        }

        if (e.key === 'n' && !e.ctrlKey && !e.metaKey && !e.altKey) {
            var target = e.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') return;
            if (navToggle) {
                e.preventDefault();
                navToggle.click();
            }
        }
    });

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var href = anchor.getAttribute('href');
            if (href === '#') return;
            var target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

})();