document.querySelector('form').addEventListener('submit', function(event) {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert('Please fill in all fields.');
        event.preventDefault();
    } else {
        alert('Login Successful!');
    }
});
