function scrollToCourses() {
    const section = document.getElementById('courses');
    section.scrollIntoView({ behavior: 'smooth' });
}
function toggleMenu() {
    const nav = document.getElementById('navLinks');
    nav.classList.toggle('show');
}

