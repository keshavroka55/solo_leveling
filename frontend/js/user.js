const API_URL = "http://127.0.0.1:8000/api/people/";

// Display message
function showMessage(text, type) {
  const messageDiv = document.getElementById('message');
  messageDiv.textContent = text;
  messageDiv.className = `mb-4 p-4 rounded-lg fade-in ${type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`;
  messageDiv.classList.remove('hidden');
  setTimeout(() => {
    messageDiv.classList.add('fade-out');
    setTimeout(() => {
      messageDiv.classList.add('hidden');
      messageDiv.classList.remove('fade-out');
    }, 500);
  }, 3000);
}

// Clear input fields
function clearFields() {
  document.getElementById('name').value = '';
  document.getElementById('age').value = '';
  document.getElementById('address').value = '';
}

// Create user
function createUser() {
  const name = document.getElementById("name").value;
  const age = parseInt(document.getElementById("age").value);
  const address = document.getElementById("address").value;

  if (!name || !age || !address) {
    showMessage('Please fill in all fields', 'error');
    return;
  }

  fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, age, address })
  })
  .then(res => {
    if (!res.ok) throw new Error('Failed to create user');
    return res.json();
  })
  .then(data => {
    showMessage("User created successfully!", 'success');
    clearFields();
    listUsers();
  })
  .catch(error => {
    showMessage("Failed to create user", 'error');
  });
}

// List users
function listUsers() {
  fetch(API_URL)
    .then(res => {
      if (!res.ok) throw new Error('Failed to fetch users');
      return res.json();
    })
    .then(users => {
      const container = document.getElementById("userList");
      container.innerHTML = "";

      users.forEach(user => {
        container.innerHTML += `
          <div class="user-card">
            <div>
              <p><strong>Name:</strong> ${user.name}</p>
              <p><strong>Age:</strong> ${user.age}</p>
              <p><strong>Address:</strong> ${user.address}</p>
            </div>
            <div class="space-x-2">
              <button onclick="showUpdateForm(${user.id}, '${user.name}', ${user.age}, '${user.address}')" class="btn bg-yellow-500 text-white px-3 py-1 rounded-lg hover:bg-yellow-600 transition">Edit</button>
              <button onclick="deleteUser(${user.id})" class="btn bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600 transition">Delete</button>
            </div>
          </div>
        `;
      });
    })
    .catch(error => {
      showMessage("Failed to load users", 'error');
    });
}

// Delete user
function deleteUser(id) {
  if (confirm('Are you sure you want to delete this user?')) {
    fetch(`${API_URL}${id}/`, {
      method: "DELETE"
    })
    .then(res => {
      if (!res.ok) throw new Error('Failed to delete user');
      showMessage("User deleted successfully!", 'success');
      listUsers();
    })
    .catch(error => {
      showMessage("Failed to delete user", 'error');
    });
  }
}

// Show update form
function showUpdateForm(id, name, age, address) {
  const container = document.getElementById("userList");
  const editForm = document.createElement('div');
  editForm.className = 'edit-form';
  editForm.innerHTML = `
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <input type="text" id="editName" value="${name}" class="border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
      <input type="number" id="editAge" value="${age}" class="border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
      <input type="text" id="editAddress" value="${address}" class="border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
    </div>
    <button onclick="updateUser(${id})" class="btn bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">Update</button>
  `;
  container.prepend(editForm);
}

// Update user
function updateUser(id) {
  const name = document.getElementById("editName").value;
  const age = parseInt(document.getElementById("editAge").value);
  const address = document.getElementById("editAddress").value;

  if (!name || !age || !address) {
    showMessage('Please fill in all fields', 'error');
    return;
  }

  fetch(`${API_URL}${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name, age, address })
  })
  .then(res => {
    if (!res.ok) throw new Error('Failed to update user');
    return res.json();
  })
  .then(data => {
    showMessage("User updated successfully!", 'success');
    listUsers();
  })
  .catch(error => {
    showMessage("Failed to update user", 'error');
  });
}

// Load on page
window.onload = listUsers;