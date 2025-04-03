function selectUser(uid) {
  const url = document.getElementById("selectUserBtn").getAttribute("data-url");
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected_uid: uid })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        document.getElementById("message").innerText = "User selected. Reloading...";
        setTimeout(() => {
          location.reload();
        }, 1000);
      } else {
        document.getElementById("message").innerText = "Error selecting user.";
      }
    })
    .catch(error => {
      document.getElementById("message").innerText = "An error occurred.";
    });
  }