const main_content = document.querySelector('.main_content');
const loginUrl = main_content.getAttribute("data-login-url");

const accessToken = localStorage.getItem('access_token')

const btn = document.getElementById('auth-btn')

console.log(accessToken)

if (accessToken != null) {
    window.location.assign('http://localhost:8009/chat')
}

async function handleLogin(loginUrl) {
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value

    try {
        const response = await fetch(loginUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            // Сохраняем токены в localStorage
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);

            // Перезагружаем страницу для обновления интерфейса
            window.location.assign('http://localhost:8009/chat');
        } else {
            alert("Ошибка при входе: " + data.detail);
        }
    } catch (error) {
        console.error("Ошибка:", error);
    }
}

btn.addEventListener('click', () => {
    handleLogin(loginUrl)
})