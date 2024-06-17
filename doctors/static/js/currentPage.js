const activePage = window.location.pathname;
console.log(activePage)
const buttons = document.querySelectorAll('.nav-bar button');
buttons.forEach(button => {
    const parentForm = button.closest('form');
    if (parentForm) {
        const url = parentForm.getAttribute('action');
        console.log('URL:', url);
        if (url && url.includes(activePage)) {
            button.classList.add('active');
        }
    }
});
