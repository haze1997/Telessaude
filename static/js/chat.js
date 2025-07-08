let user_id = Number(sessionStorage.getItem('UID'))
const canal = sessionStorage.getItem('sala')
let resposta = await fetch(`/get_user/?uid=${user_id}`, {Cache: 'reload', credentials: 'include'})
let dados = await resposta.json()
let nome_usuario = dados.username
/*
document.querySelector('#enviarmensagem').onclick = function (e) {
  const messageInputDom = document.querySelector('#mensagem');
  const message = messageInputDom.value;
  chatSocket.send(JSON.stringify({
      'message': message,
      'username': user_username,
  }));
  messageInputDom.value = '';
};


const chatSocket = new WebSocket(
  'ws://' +
  window.location.host +
  '/ws/chat/' +
  canal +
  '/'
);

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log(data)
  document.querySelector('#mensagens').innerHTML = (data.message + ' sent by ' + data.username   + '\n') // add message to text box
}
*/

const roomName = JSON.parse(canal);
const userName = JSON.parse(nome_usuario);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + roomName
    + '/'
);

chatSocket.onclose = function(e) {
    console.log('onclose')
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.message) {
        document.querySelector('#chat-messages').innerHTML += ('<b>' + data.username + '</b>: ' + data.message + '<br>');
    } else {
        alert('The message was empty!')
    }

    scrollToBottom();
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    console.log({
        'message': message,
        'username': userName,
        'room': roomName
    })

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'room': roomName
    }));

    messageInputDom.value = '';

    return false
};

/**
* A function for finding the messages element, and scroll to the bottom of it.
*/
function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

// Add this below the function to trigger the scroll on load.
scrollToBottom();
