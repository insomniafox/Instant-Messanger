const main_content = document.querySelector('.main_content');
const registerUrl = main_content.getAttribute("data-register-url");
const baseUrl = main_content.getAttribute('data-base-url')

const accessToken = localStorage.getItem('access_token')

const btn = document.getElementById('auth-btn')

if (accessToken != null) {
    window.location.assign(`${baseUrl}/chat`)
}

async function handleRegister(registerUrl) {
    const username = document.getElementById('username').value
    const firstName = document.getElementById('firstName').value
    const lastName = document.getElementById('lastName').value
    const password = document.getElementById('password').value

    try {
        const response = await fetch(registerUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password,
                first_name: firstName,
                last_name: lastName
            })
        });

        const data = await response.json();
        if (response.ok) {
            // Сохраняем токены в localStorage
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);

            // Перезагружаем страницу для обновления интерфейса
            window.location.assign(`${baseUrl}/chat`)
        } else {
            alert("Ошибка при регистрации: " + data.detail);
        }
    } catch (error) {
        console.error("Ошибка:", error);
    }
}

btn.addEventListener('click', () => {
    handleRegister(registerUrl)
})