document.addEventListener("DOMContentLoaded", function() {
      const savedImage = localStorage.getItem('wallet_profile_pic');
      
      if (savedImage) {
        const topProfilePhoto = document.getElementById('homeTopProfileDisplay');
        const bottomNavPhoto = document.getElementById('homeBottomNavDisplay');
        
        // ஒரே இமேஜை டாப் மற்றும் பாட்டம் இரண்டு இடங்களிலும் வைக்கிறது
        if (topProfilePhoto) {
          topProfilePhoto.src = savedImage;
        }
        if (bottomNavPhoto) {
          bottomNavPhoto.src = savedImage;
        }
      }
    });

   document.getElementById('userSearchInput').addEventListener('input', function() {
    let query = this.value.trim();
    let displayDiv = document.getElementById('searchResultDisplay');
    let nameSpan = document.getElementById('searchResultName');
    let chatLink = document.getElementById('searchUserChatLink');

    if (query.length === 0) {
        displayDiv.style.display = 'none';
        return;
    }

    // Fetch call to your Python search_user route
    fetch(`/search_user?userid=${query}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayDiv.style.display = 'block';
                nameSpan.innerText = data.name;
                // Set link to chat page with the searched user ID
                chatLink.href = `/chat/${query}`;
                chatLink.style.pointerEvents = 'auto'; // Enable clicking
            } else {
                displayDiv.style.display = 'block';
                nameSpan.innerText = 'User Not Found!';
                chatLink.href = '#';
                chatLink.style.pointerEvents = 'none'; // Disable clicking if not found
            }
        })
        .catch(err => console.error(err));
});