// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const body = document.body;

themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark');
    const isDarkMode = body.classList.contains('dark');
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    updateThemeIcon(isDarkMode);
});

// Check Local Storage for Theme Preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    body.classList.add('dark');
    updateThemeIcon(true);
} else {
    body.classList.remove('dark');
    updateThemeIcon(false);
}

// Update Theme Icon
function updateThemeIcon(isDarkMode) {
    if (isDarkMode) {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    } else {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }
}

// Chart.js Initialization
let salesChart, visitorsChart;

function initializeCharts() {
    const salesChartCtx = document.getElementById('salesChart').getContext('2d');
    const visitorsChartCtx = document.getElementById('visitorsChart').getContext('2d');

    salesChart = new Chart(salesChartCtx, {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Sales',
                data: [65, 59, 80, 81, 56, 55, 40],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allow charts to resize freely
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    visitorsChart = new Chart(visitorsChartCtx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Visitors',
                data: [200, 300, 400, 500, 600, 700, 800],
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allow charts to resize freely
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Initialize charts on page load
initializeCharts();

// Redraw charts on window resize
window.addEventListener('resize', () => {
    if (salesChart) salesChart.resize();
    if (visitorsChart) visitorsChart.resize();
});
