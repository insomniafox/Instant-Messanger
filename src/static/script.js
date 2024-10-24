const userList = document.querySelector(".userList");
const messagesBlock = document.querySelector(".messages")
const userListSection = document.querySelector('.userListSection')
const nickname = document.querySelector('.nickname')

const authSection = document.getElementById("auth-section");
const chatSection = document.getElementById("chat-section");
const sendButton = document.getElementById("send-button");
const messageInput = document.getElementById("message-input");

const usersUrl = authSection.getAttribute("data-users-url");
const chatUrl = authSection.getAttribute("data-chat-url");

let users = []

const accessToken = localStorage.getItem('access_token')

if (accessToken == null) {
    window.location.assign('http://localhost:8009/sign-up')
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
        console.log("Полученные пользователи:", users);
        displayUsers(users)
    } catch (error) {
        console.error("Ошибка при получении пользователей:", error);
    }
}

function displayUsers(users) {
    if (users != null) {
        userList.innerHTML = "";
        // chatLogUserList.innerHTML = ""; // Очищаем перед добавлением

        users.map(user => {
            const li = document.createElement("li");
            li.textContent = user.username;
            const liClone = li.cloneNode(true);
            userList.appendChild(li);
            // chatLogUserList.appendChild(liClone);
            li.addEventListener("click", () => initializeChat(user.id));
        });
    }
}

function initializeChat(receiverId) {
    userListSection.style.display = "none"; // Скрываем список пользователей
    chatSection.style.display = "block"; // Показываем секцию чата

    const getUserNickname = users.filter((user) => {
        return user.id === receiverId
    })

    nickname.textContent = getUserNickname[0].username

    const ws = new WebSocket(`${chatUrl}/${receiverId}?token=${accessToken}`);

    // Получение сообщений от сервера
    ws.onmessage = function(event) {
        const message = event.data;
        const messageElement = document.createElement("div");
        messageElement.innerHTML = message;
        messagesBlock.appendChild(messageElement);
    };

    // Отправка сообщения при нажатии на кнопку "Send"
    sendButton.onclick = function() {
        const message = messageInput.value;
        ws.send(message);
        messageInput.value = "";
        const messageElement = document.createElement("div");
        messageElement.innerHTML = message;
        messagesBlock.appendChild(messageElement);
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
    const linkUrl = 'http://localhost:8009/api/telegram/get_token'
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

telegramBtn.addEventListener('click',() => {
    linkTelegram(accessToken)
})