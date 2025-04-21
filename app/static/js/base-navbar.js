const sidebar = document.getElementById('sidebar');
document.getElementById('sidebarToggle')?.addEventListener('click', function () {
    sidebar.classList.toggle('active');
});
document.getElementById('sidebarClose')?.addEventListener('click', function () {
    sidebar.classList.remove('active');
});