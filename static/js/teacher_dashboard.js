function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => section.style.display = 'none');

    // Show the selected section
    document.getElementById(sectionId).style.display = 'block';

    // Update active class on sidebar items
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelector(`.nav-item[onclick="showSection('${sectionId}')"]`)?.classList.add('active');
}