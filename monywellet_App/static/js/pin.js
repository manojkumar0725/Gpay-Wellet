document.getElementById('pinForm').addEventListener('submit', function(e) {
    e.preventDefault(); // படிவம் சப்மிட் ஆகி பக்கம் ரீலோடு ஆவதைத் தடுக்கிறது
    
    const pinValue = document.getElementById('pinInput').value;
    const errorDiv = document.getElementById('error-msg');
    
    // எரர் மெசேஜை முதலில் மறைக்கிறோம்
    errorDiv.classList.add('d-none');
    errorDiv.textContent = '';

    // பேக்-எண்ட் பைத்தான் கோடிற்கு டேட்டாவை அனுப்புகிறோம்
    fetch('/check_pin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pin: pinValue })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // பின் சரியாக இருந்தால், பைத்தான் சொல்லும் இடத்திற்கு (balance பக்கத்திற்கு) அழைத்துச் செல்லும்
            window.location.href = data.redirect;
        } else {
            // பின் தவறாக இருந்தால் எரர் காட்டும்
            errorDiv.textContent = data.message;
            errorDiv.classList.remove('d-none');
            document.getElementById('pinInput').value = ''; // இன்புட்டை கிளியர் செய்கிறது
        }
    })
    .catch(err => {
        errorDiv.textContent = "Something went wrong. Try again!";
        errorDiv.classList.remove('d-none');
    });
});