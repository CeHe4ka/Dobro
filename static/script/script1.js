const LoginForm = document.querySelector('.LoginForm');
        const RegisterForm = document.querySelector('.RegisterForm')
        const RegisterLink = document.querySelector('.RegisterLink');
        const LoginLink = document.querySelector('.LoginLink');
        RegisterLink.onclick=()=>{
            RegisterForm.classList.add('active');
            LoginForm.classList.add('active');
        }
        LoginLink.onclick=()=>{
            RegisterForm.classList.remove('active');
            LoginForm.classList.remove('active');
        }


