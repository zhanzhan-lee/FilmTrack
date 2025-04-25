const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarClose = document.getElementById('sidebarClose');

// Toggle sidebar and change button content
sidebarToggle?.addEventListener('click', function () {
    sidebar.classList.toggle('active');

    // Change button content based on sidebar state
    if (sidebar.classList.contains('active')) {
        sidebarToggle.textContent = '✕'; 
      
    } else {
        sidebarToggle.textContent = '☰';
       
    }
});

// Close sidebar and reset button content
sidebarClose?.addEventListener('click', function () {
    sidebar.classList.remove('active');
    sidebarToggle.textContent = '☰'; 
    // Reset to "☰" when sidebar is closed
});