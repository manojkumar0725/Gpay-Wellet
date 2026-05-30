// இது பட்டன் முழுசா லோட் ஆன அப்புறம் தான் வேலை செய்யும்
document.addEventListener('DOMContentLoaded', function() {
    const balanceBtn = document.getElementById('balance');

    if (balanceBtn) {
        console.log("Button found!"); // Console-ல் இது வருகிறதா என பாருங்கள்
        balanceBtn.addEventListener('click', function() {
            console.log("Button clicked!"); // பட்டனை கிளிக் செய்தால் இது வர வேண்டும்
            const password = prompt("Please enter the security password:");

            if (password) {
                fetch('/check_password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ password: password }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        window.location.href = data.redirect;
                    } else {
                        alert(data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    } else {
        console.log("Button NOT found!"); // பட்டன் ID தப்பா இருந்தா இது வரும்
    }
});
/*
document.addEventListener('DOMContentLoaded', function() {
    
    function setupSecurity(buttonId, targetPage) {
        const btn = document.getElementById(buttonId);
        if (btn) {
            btn.addEventListener('click', function() {
                const password = prompt("Enter Security Password:");
                if (password) {
                    fetch('/check_password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ password: password })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === "success") {
                            // Target page-ku redirect panna sollurom
                            window.location.href = "/targetPage"; 
                        } else {
                            alert(data.message);
                        }
                    });
                }
            });
        }
    }

    // Buttons-ah link pannunga
    setupSecurity('balance', '/balance');
    setupSecurity('transferBtn', '/transfer_page');
});  */