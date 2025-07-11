// transitions.js

// Add fade-in class when the page loads
document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('fade-in');
});

// Optional: Fade-out effect on link clicks (for full-page transitions)
document.querySelectorAll('a').forEach(link => {
    // Ignore links with target="_blank" or anchor/hash links
    if (
        link.getAttribute('target') === '_blank' ||
        link.href.startsWith('#') ||
        link.href.startsWith('javascript:')
    ) return;

    link.addEventListener('click', function (e) {
        // Prevent default, fade out, then follow link
        e.preventDefault();
        document.body.classList.remove('fade-in');
        document.body.style.opacity = 0;
        setTimeout(() => {
            window.location = this.href;
        }, 300); // Match CSS transition time
    });
});
