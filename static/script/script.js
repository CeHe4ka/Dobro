document.addEventListener('DOMContentLoaded', function () {
    const LoginForm = document.querySelector('.LoginForm');
    const RegisterForm = document.querySelector('.RegisterForm');
    const RegisterLink = document.querySelector('.RegisterLink');
    const LoginLink = document.querySelector('.LoginLink');

    // Обработка клика по "Зарегистрироваться"
    if (RegisterLink) {
        RegisterLink.addEventListener('click', function (e) {
            e.preventDefault();
            RegisterForm.classList.add('active');
            LoginForm.classList.add('active');

            // Сохраняем флаг, что пользователь открыл форму регистрации
            localStorage.setItem('show_register_form', '1');
        });
    }

    // Обработка клика по "Войти"
    if (LoginLink) {
        LoginLink.addEventListener('click', function (e) {
            e.preventDefault();
            RegisterForm.classList.remove('active');
            LoginForm.classList.remove('active');

            // Удаляем флаг, если пользователь вернулся к логину
            localStorage.removeItem('show_register_form');
        });
    }

    // Проверка: была ли открыта форма регистрации ранее (например, после ошибки)
    if (localStorage.getItem('show_register_form') === '1') {
        RegisterForm.classList.add('active');
        LoginForm.classList.add('active');
    }

    // Удалим флаг, если форма уже показана (предотвращает повторное срабатывание)
    localStorage.removeItem('show_register_form');
});
