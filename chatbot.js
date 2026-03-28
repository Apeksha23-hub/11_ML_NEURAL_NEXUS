document.addEventListener('DOMContentLoaded', () => {
    const chatFab = document.getElementById('chat-fab');
    const chatbotContainer = document.getElementById('chatbot-container');
    const toggleBtn = document.getElementById('chatbot-toggle-btn');
    const sendBtn = document.getElementById('chat-send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    
    let chatHistory = [];

    // Toggle Chatbot Window
    chatFab.addEventListener('click', () => {
        chatbotContainer.style.display = 'flex';
        chatFab.style.display = 'none';
        chatInput.focus();
    });

    toggleBtn.addEventListener('click', () => {
        chatbotContainer.style.display = 'none';
        chatFab.style.display = 'block';
    });

    // Send Message
    const sendMessage = async () => {
        const query = chatInput.value.trim();
        if (!query) return;

        // Display user message
        appendMessage('user', query);
        chatInput.value = '';

        // Determine context (from the main form prediction)
        const context = window.currentStudentContext ? { "student_profile": window.currentStudentContext } : null;

        // Show typing indicator
        const typingId = appendTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    context: context,
                    history: chatHistory
                })
            });

            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            
            // Remove typing indicator
            removeElement(typingId);
            
            // Display bot reply
            appendMessage('bot', data.reply);
            
            // Save to history
            chatHistory.push({ role: 'user', content: query });
            chatHistory.push({ role: 'advisor', content: data.reply });
            
        } catch (error) {
            console.error('Chat error:', error);
            removeElement(typingId);
            appendMessage('bot', 'Sorry, I am having trouble connecting to the server. Please try again.');
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // UI Helper Functions
    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender === 'user' ? 'user-message' : 'bot-message'}`;
        
        // Simple markdown parsing for bold and line breaks
        let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedText = formattedText.replace(/\n/g, '<br>');
        
        msgDiv.innerHTML = formattedText;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'message bot-message';
        msgDiv.textContent = 'Typing...';
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }
    
    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});
