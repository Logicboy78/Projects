// Elements
const btnLogin   = document.getElementById('btn-login');
const btnSignup  = document.getElementById('btn-signup');
const formLogin  = document.getElementById('form-login');
const formSignup = document.getElementById('form-signup');
const linkSignup = document.getElementById('link-signup');
const linkLogin  = document.getElementById('link-login');

// Show Login
function showLogin() {
  btnLogin.classList.add('active');
  btnSignup.classList.remove('active');
  formLogin.classList.add('active');
  formSignup.classList.remove('active');
}

// Show Signup
function showSignup() {
  btnSignup.classList.add('active');
  btnLogin.classList.remove('active');
  formSignup.classList.add('active');
  formLogin.classList.remove('active');
}

// Tab clicks
btnLogin.addEventListener('click', showLogin);
btnSignup.addEventListener('click', showSignup);

// Footer links
linkSignup.addEventListener('click', e => { e.preventDefault(); showSignup(); });
linkLogin.addEventListener('click', e => { e.preventDefault(); showLogin(); });

// Signup form
formSignup.addEventListener('submit', e => {
  e.preventDefault();
  const name = document.getElementById('signup-name').value;
  const email = document.getElementById('signup-email').value;
  const password = document.getElementById('signup-password').value;

  fetch('/api/auth/signup', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name, email, password})
  })
  .then(res => res.json())
  .then(data => {
    if (data.message) alert(data.message);
    if (data.error) alert(data.error);
  })
  .catch(err => console.error(err));
});

// Login form
formLogin.addEventListener('submit', e => {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  fetch('/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email, password})
  })
  .then(res => res.json())
  .then(data => {
    if (data.redirect) {
      window.location.href = data.redirect;  // Redirect to your second page
    } else if (data.error) {
      alert(data.error);
    }
  })
  .catch(err => console.error(err));
});

// Init
showLogin();