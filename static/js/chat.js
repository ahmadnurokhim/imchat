// Get references to HTML elements
var chatBox = document.getElementById('chat-box');
var msgInput = document.getElementById('msg-input');
var sendBtn = document.getElementById('send-btn');

// Initialize Socket.IO connection
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Handle incoming messages
socket.on('message', function(data) {
    chatBox.innerHTML += '<p>' + data.msg + '</p>';
});

// Send message to server
sendBtn.onclick = function() {
    var msg = msgInput.value;
    socket.emit('message', {msg: msg});
    msgInput.value = '';
};
