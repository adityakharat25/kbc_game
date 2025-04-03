 // Poll every 3 seconds to check if the game status has changed.
 setInterval(function() {
   fetch(`/check_game_status/${currentUserUid}`)
     .then(response => response.json())
     .then(data => {
       if (data.status === 'accepted') {
         window.location.href = `/game/${currentUserUid}`;
       } else if (data.status === 'rejected') {
         alert('You were not selected for the game. Redirecting to login.');
         window.location.href = '/not_selected';
       }
     })
     .catch(error => console.error('Error:', error));
 }, 3000);

 // Add this to waiting.html
function checkStatus() {
 const uid = currentUserUid;
 fetch(`/check_game_status/${uid}`)
     .then(response => response.json())
     .then(data => {
         if (data.status === 'accepted') {
             window.location.href = `/game/${uid}`;
         }
     });
}

// Check every 2 seconds
setInterval(checkStatus, 2000);
