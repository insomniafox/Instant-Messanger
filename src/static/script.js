const userList = document.querySelector(".userList");
const messagesBlock = document.querySelector(".messages")
const userListSection = document.querySelector('.userListSection')
const nickname = document.querySelector('.nickname')

const authSection = document.getElementById("auth-section");
const chatSection = document.getElementById("chat-section");
const sendButton = document.getElementById("send-button");
const messageInput = document.getElementById("message-input");
const chatLog = document.getElementById('chat-log')

const usersUrl = authSection.getAttribute("data-users-url");
const chatUrl = authSection.getAttribute("data-chat-url");
const messageHistoryUrl = authSection.getAttribute("data-message-history-url");
const meUrl = authSection.getAttribute('data-me-url')
const baseUrl = authSection.getAttribute('data-base-url')

let users = []

const accessToken = localStorage.getItem('access_token')

if (accessToken == null) {
    window.location.assign(`${baseUrl}/sign-up`)
}


async function fetchUsers(accessToken, query = "") {
    try {
        const response = await fetch(usersUrl, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });
        users = await response.json();
        displayUsers(users)
    } catch (error) {
        console.error("Ошибка при получении пользователей:", error);
    }
}

function displayUsers(users) {
    if (users != null) {
        userList.innerHTML = "";

        users.map(user => {
            const li = document.createElement("li");
            li.textContent = user.username;
            const liClone = li.cloneNode(true);
            userList.appendChild(li);
            li.addEventListener("click", () => initializeChat(user.id));
        });
    }
}

async function getSenderName(accessToken) {
    try {
        const response = await fetch(meUrl, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });

        const currentUser = await response.json();
        return currentUser.username; // Возвращаем строку, например, `username`
    } catch (error) {
        console.error("Ошибка при получении пользователя:", error);
    }
}

async function getMessageHistory(accessToken, receiverId) {
    try {
        const response = await fetch(messageHistoryUrl + receiverId, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });
        messages = await response.json();
        return messages
    } catch (error) {
        console.error("Ошибка при получении истории сообщений:", error);
    }
}

function scrollToBottom() {
    chatLog.scrollTop = chatLog.scrollHeight;
}

function initializeChat(receiverId) {
    userListSection.style.display = "none"; // Скрываем список пользователей
    chatSection.style.display = "block"; // Показываем секцию чата

    let currentUser = ""; // Создаем переменную для хранения имени

    getSenderName(accessToken).then((result) => {
        currentUser = result;
    });

    const messages = getMessageHistory(accessToken, receiverId)
        .then(messages => {
            messages.map(message => {
                const elementMessage = document.createElement("div");
                const content = `${message.created_at} ${message.sender_username}: ${message.text}`;
                elementMessage.textContent = content;
                messagesBlock.appendChild(elementMessage);
            });
        })

    const getUserNickname = users.filter((user) => {
        return user.id === receiverId
    })

    nickname.textContent = getUserNickname[0].username

    const ws = new WebSocket(`${chatUrl}/${receiverId}?token=${accessToken}`);

    // Получение сообщений от сервера
    ws.onmessage = function (event) {
        const now = new Date();
        const currentTime = `${now.getUTCFullYear()}.${String(now.getUTCMonth() + 1).padStart(2, '0')}.${String(now.getUTCDate()).padStart(2, '0')} ${String(now.getUTCHours()).padStart(2, '0')}:${String(now.getUTCMinutes()).padStart(2, '0')}`;

        const message = `${currentTime} ${event.data}`
        const messageElement = document.createElement("div");
        messageElement.innerHTML = message;
        messagesBlock.appendChild(messageElement);
        scrollToBottom()
    };

    // Отправка сообщения при нажатии на кнопку "Send"
    sendButton.onclick = function () {
        const now = new Date();
        const currentTime = `${now.getUTCFullYear()}.${String(now.getUTCMonth() + 1).padStart(2, '0')}.${String(now.getUTCDate()).padStart(2, '0')} ${String(now.getUTCHours()).padStart(2, '0')}:${String(now.getUTCMinutes()).padStart(2, '0')}`;

        const message = `${currentTime} ${currentUser}: ${messageInput.value}`;
        ws.send(message);
        messageInput.value = "";
        const messageElement = document.createElement("div");
        messageElement.innerHTML = message;
        messagesBlock.appendChild(messageElement);
        scrollToBottom()
    };

    // Отправка сообщения при нажатии клавиши Enter
    messageInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendButton.click();
        }
    });
}

const telegramBtn = document.querySelector('.telegramBtn')

async function linkTelegram(accessToken) {
    const linkUrl = `${baseUrl}/api/telegram/get_token`
    try {
        const response = await fetch(linkUrl, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${accessToken}`,
                "Content-Type": "application/json"
            }
        });
        let telegramLink = await response.text();
        telegramLink = telegramLink.replace(/^"|"$/g, '');

        // Прямой переход по ссылке
        window.location.href = telegramLink; // Перенаправление на абсолютную ссылку
        if (response.status == 200 || response.status == 201) {
            window.location.href(res)
        }
    } catch (error) {
        console.error(error);
    }
}

fetchUsers(accessToken)

telegramBtn.addEventListener('click', () => {
    linkTelegram(accessToken)
})