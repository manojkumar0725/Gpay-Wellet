function triggerFileInput() {
      document.getElementById('profileInput').click();
    }

    // 2. தேர்ந்தெடுத்த படத்தை சேமித்து காண்பிக்கும் செயல்பாடு
    function previewAndSaveImage(input) {
      if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
          const base64Image = e.target.result;
          
          // Local Storage-ல் படத்தை சேமிக்கிறது
          localStorage.setItem('wallet_profile_pic', base64Image);
          
          // திரையில் உள்ள இரண்டு இமேஜ்களையும் அப்டேட் செய்கிறது
          document.getElementById('profileDisplay').src = base64Image;
          document.getElementById('bottomNavDisplay').src = base64Image;
        };
        
        reader.readAsDataURL(input.files[0]);
      }
    }

    // 3. பக்கம் லோட் ஆகும் போது லோக்கல் ஸ்டோரேஜில் இருந்து படம் எடுக்கிறது
    document.addEventListener("DOMContentLoaded", function() {
      const savedImage = localStorage.getItem('wallet_profile_pic');
      if (savedImage) {
        document.getElementById('profileDisplay').src = savedImage;
        document.getElementById('bottomNavDisplay').src = savedImage;
      }
    });