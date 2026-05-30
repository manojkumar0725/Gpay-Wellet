// static/js/chat.js
document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chatBox');
    
    // சாட் பக்கம் திறந்தவுடன் ஸ்க்ரோல் தானாக கீழே செல்லும்
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    const chatForm = document.getElementById('chatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const receiverId = document.getElementById('receiverId').value;
            const messageInput = document.getElementById('messageInput');
            const messageText = messageInput.value;
            
            if (!messageText.trim()) return;

            // தற்போதைய நேரத்தை AM/PM வடிவில் கணக்கிடுதல்
            const now = new Date();
            let hours = now.getHours();
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; 
            const currentTimeString = `${hours}:${minutes} ${ampm}`;

            const formData = new FormData();
            formData.append('receiver_id', receiverId);
            formData.append('message', messageText);

            // Fetch API மூலம் பேக்-எண்டிற்குத் தரவை அனுப்புதல்
            fetch('/send_message', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const messagesList = document.getElementById('messagesList');
                    
                    // லைவ் ஆக மெசேஜை டபுள் டிக்குடன் ஸ்கிரீனில் சேர்த்தல்
                    const newMsg = `
                        <div class="d-flex mb-2">
                            <div class="msg-box msg-sent">
                                <div class="text-dark text-start">${messageText}</div>
                                <div class="msg-meta">
                                    <span>${currentTimeString}</span>
                                    <i class="bi bi-check2-all tick-blue"></i>
                                </div>
                            </div>
                        </div>
                    `;
                    messagesList.insertAdjacentHTML('beforeend', newMsg);
                    messageInput.value = ''; // Input பாக்ஸை காலி செய்தல்
                    
                    if (chatBox) {
                        chatBox.scrollTop = chatBox.scrollHeight; // மீண்டும் கீழே ஸ்க்ரோல் செய்தல்
                    }
                }
            })
            .catch(err => console.error("Error sending message:", err));
        });
    }
});