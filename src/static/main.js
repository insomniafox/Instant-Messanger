const authSection = document.getElementById("auth-section");
const userListSection = document.getElementById("user-list-section");
const chatSection = document.getElementById("chat-section");
const loginBtn = document.getElementById("login-btn");
const registerBtn = document.getElementById("register-btn");
const userSearch = document.getElementById("user-search");
const userList = document.getElementById("user-list");
const chatLog = document.getElementById("chat-log");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");

// Получаем URL для запросов и receiver_id из data-* атрибутов
const usersUrl = authSection.getAttribute("data-users-url");
const loginUrl = authSection.getAttribute("data-login-url");
const registerUrl = authSection.getAttribute("data-register-url");
const chatUrl = authSection.getAttribute("data-chat-url");
let users = []

document.addEventListener("DOMContentLoaded", () => {
    // Проверка наличия токена в localStorage
    const accessToken = localStorage.getItem("access_token");

    if (accessToken) {
        loadPage(accessToken)
    } else {
        // Если токена нет, показываем кнопки "Вход" и "Регистрация"
        loginBtn.style.display = "inline";
        registerBtn.style.display = "inline";

        // Добавляем обработчики для кнопок "Вход" и "Регистрация"
        loginBtn.addEventListener("click", () => handleLogin(loginUrl));
        registerBtn.addEventListener("click", () => handleRegister(registerUrl));
    }

    // Функция для обработки логина
    async function handleLogin(loginUrl) {
        const username = prompt("Введите имя пользователя");
        const password = prompt("Введите пароль");

        try {
            const response = await fetch(loginUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();
            if (response.ok) {
                // Сохраняем токены в localStorage
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);

                // Перезагружаем страницу для обновления интерфейса
                window.location.reload();
            } else {
                alert("Ошибка при входе: " + data.detail);
            }
        } catch (error) {
            console.error("Ошибка:", error);
        }
    }

    // Функция для обработки регистрации
    async function handleRegister(registerUrl) {
        const username = prompt("Введите имя пользователя");
        const password = prompt("Введите пароль");
        const firstName = prompt("Введите ваше имя");
        const lastName = prompt("Введите вашу фамилию");

        try {
            const response = await fetch(registerUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password, first_name: firstName, last_name: lastName })
            });

            const data = await response.json();
            if (response.ok) {
                // Сохраняем токены в localStorage
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);

                // Перезагружаем страницу для обновления интерфейса
                window.location.reload();
            } else {
                alert("Ошибка при регистрации: " + data.detail);
            }
        } catch (error) {
            console.error("Ошибка:", error);
        }
    }

    // Функция для обработки поиска пользователей
    userSearch.addEventListener("input", (event) => {
        const query = event.target.value;
        fetchUsers(query); // Выполняем поиск при вводе в поле
    });

// Инициализация чата после выбора пользователя
function initializeChat(receiverId) {
        userListSection.style.display = "none"; // Скрываем список пользователей
        chatSection.style.display = "block"; // Показываем секцию чата

        const ws = new WebSocket(`${chatUrl}/${receiverId}`);

        // Отправляем токен авторизации при открытии WebSocket-соединения
        ws.onopen = function () {
            ws.send(JSON.stringify({
                type: 'authorization',
                token: accessToken
            }));
        };

        // Получение сообщений от сервера
        ws.onmessage = function(event) {
            const message = event.data;
            const messageElement = document.createElement("div");
            messageElement.textContent = message;
            chatLog.appendChild(messageElement);
        };

        // Отправка сообщения при нажатии на кнопку "Send"
        sendButton.onclick = function() {
            const message = messageInput.value;
            ws.send(message);
            messageInput.value = "";
        };

        // Отправка сообщения при нажатии клавиши Enter
        messageInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendButton.click();
            }
        });
    }
});

// Получаем список пользователей
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
        displayUsers(users);
    } catch (error) {
        console.error("Ошибка при получении пользователей:", error);
    }
}

// Отображаем список пользователей
function displayUsers(users) {
    if (users != null ){userList.innerHTML += `$users.map((user) => {<div>{user.username}</div>})`} // Очищаем список перед добавлением новых пользователей
    users.forEach(user => {
        const li = document.createElement("li");
        li.textContent = user.username;
        li.addEventListener("click", () => initializeChat(user.id)); // Начинаем чат с выбранным пользователем
        userList.appendChild(li);
    });
}

async function loadPage(accessToken) {
    // Если токен существует, показываем список пользователей
    // authSection.style.display = "none";
    // userListSection.style.display = "block";
    await fetchUsers(accessToken)  // Загружаем пользователей
    .then(() => console.log("Пользователи загружены"))
    .catch((error) => console.error("Ошибка при загрузке пользователей:", error));
}