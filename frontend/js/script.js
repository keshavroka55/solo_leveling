// Load header and footer dynamically
fetch('nav.html')
  .then(res => res.text())
  .then(data => document.getElementById('header').innerHTML = data);

fetch('footer.html')
  .then(res => res.text())
  .then(data => document.getElementById('footer').innerHTML = data);

// Navigation functions
function goToHealthPage() {
  window.location.href = "health.html";
}

function goToHomePage() {
  window.location.href = "index.html";
}
