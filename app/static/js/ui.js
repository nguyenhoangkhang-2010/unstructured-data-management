document.addEventListener('DOMContentLoaded', function() {
    
    // Sidebar Toggle
    const sidebarToggle = document.getElementById("sidebarToggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", function(e) {
            e.preventDefault();
            document.getElementById("wrapper").classList.toggle("toggled");
        });
    }

    // Dark Mode Toggle
    const darkModeToggle = document.getElementById("darkModeToggle");
    if (darkModeToggle) {
        // Check for saved 'darkMode' in localStorage
        if (localStorage.getItem('darkMode') === 'enabled') {
            document.body.classList.add('dark-theme');
            darkModeToggle.innerHTML = '☀️ Light Mode';
        }

        darkModeToggle.addEventListener("click", function(e) {
            e.preventDefault();
            document.body.classList.toggle("dark-theme");
            const isDark = document.body.classList.contains('dark-theme');
            darkModeToggle.innerHTML = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
            localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
        });
    }
});