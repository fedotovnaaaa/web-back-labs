let currentUser = null;

// Получаем элементы
const loginForm = document.getElementById('login-form');
const loginInput = document.getElementById('login');
const passwordInput = document.getElementById('password');
const loginError = document.getElementById('login-error');

const clientPanel = document.getElementById('client-panel');
const managerPanel = document.getElementById('manager-panel');
const userInfo = document.getElementById('user-info');
const logoutBtn = document.getElementById('logout-btn');

const addUserBtn = document.getElementById('add-user-btn');
const userModal = document.getElementById('user-modal');

const saveUserBtn = document.getElementById('save-user-btn');
const cancelUserBtn = document.getElementById('cancel-user-btn');
const transferBtn = document.getElementById('transfer-btn');

function validateLogin() {
    const loginVal = loginInput.value.trim();
    const passVal = passwordInput.value.trim();

    if (!loginVal || !passVal) {
        loginError.innerText = 'Введите логин и пароль';
        return false;
    }

    if (loginVal.length < 3 || loginVal.length > 50) {
        loginError.innerText = 'Логин должен быть от 3 до 50 символов';
        return false;
    }

    if (!/^[a-zA-Z0-9_.-]+$/.test(loginVal)) {
        loginError.innerText = 'Логин может содержать только латинские буквы, цифры, _, . и -';
        return false;
    }

    if (passVal.length < 6) {
        loginError.innerText = 'Пароль должен быть не короче 6 символов';
        return false;
    }

    loginError.innerText = '';
    return true;
}

function login() {
    if (!validateLogin()) return;

    fetch('/rgz/rest-api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            login: loginInput.value.trim(),
            password: passwordInput.value
        })
    })
    .then(r => {
        if (!r.ok) throw new Error();
        return r.json();
    })
    .then(user => {
        currentUser = user;
        localStorage.setItem('user', JSON.stringify(user));
        init();
    })
    .catch(() => {
        loginError.innerText = 'Ошибка входа. Проверьте логин и пароль.';
    });
}

function init() {
    // Проверяем, что пользователь авторизован
    if (!currentUser) {
        console.warn('Нет текущего пользователя — показываем форму входа');
        if (loginForm) loginForm.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        return;
    }

    // Скрываем форму входа
    if (loginForm) loginForm.style.display = 'none';
    if (loginError) loginError.innerText = '';

    // Показываем кнопку выхода
    if (logoutBtn) logoutBtn.style.display = 'block';

    // Обновляем приветствие с именем пользователя
    const welcomeElement = document.querySelector('.user-info h2');
    if (welcomeElement && currentUser.full_name) {
        welcomeElement.innerHTML = `Добро пожаловать в Банк Julka, ${currentUser.full_name}`;
    } else if (welcomeElement) {
        welcomeElement.innerHTML = 'Добро пожаловать в Банк Julka';
    }

    // Показываем информацию о пользователе (роль и ФИО)
    if (userInfo) {
        userInfo.innerHTML = `${currentUser.full_name} (${currentUser.role})`;
        userInfo.style.display = 'block';
    }

    // Скрываем обе панели перед показом нужной
    if (clientPanel) clientPanel.style.display = 'none';
    if (managerPanel) managerPanel.style.display = 'none';

    // Показываем панель в зависимости от роли
    if (currentUser.role === 'client' && clientPanel) {
        clientPanel.style.display = 'block';
        loadAccount();
        loadHistory();
    } else if (currentUser.role === 'manager' && managerPanel) {
        managerPanel.style.display = 'block';
        loadUsers();  // Загружаем список пользователей
    } else {
        console.warn('Неизвестная роль пользователя:', currentUser.role);
        alert('Ошибка: неизвестная роль пользователя. Обратитесь к администратору.');
    }
}

function logout() {
    localStorage.removeItem('user');
    location.reload();
}

window.onload = () => {
    document.getElementById('login-btn').addEventListener('click', login);
    document.getElementById('logout-btn').addEventListener('click', logout);
    document.getElementById('add-user-btn')?.addEventListener('click', showAddUser);
    document.getElementById('save-user-btn')?.addEventListener('click', saveUser);
    document.getElementById('cancel-user-btn')?.addEventListener('click', hideModal);
    document.getElementById('transfer-btn')?.addEventListener('click', transfer);

    const saved = localStorage.getItem('user');
    if (saved) {
        currentUser = JSON.parse(saved);
        init();
    }
};

// Клиент 
function loadAccount() {
    fetch(`/rgz/rest-api/client/account/${currentUser.id}`)
        .then(r => r.json())
        .then(a => {
            document.getElementById('account-number').innerText = a.account_number;
            document.getElementById('balance').innerText = a.balance;
        });
}

function loadHistory() {
    fetch(`/rgz/rest-api/client/history/${currentUser.id}`)
        .then(r => r.json())
        .then(rows => {
            const tbody = document.getElementById('history');
            tbody.innerHTML = '';
            rows.forEach(t => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${t.counterparty}</td><td>${t.type}</td><td>${t.amount}</td><td>${new Date(t.created_at).toLocaleString()}</td>`;
                tbody.appendChild(tr);
            });
        });
}

function validateTransfer() {
    const toAccountInput = document.getElementById('to-account');
    const amountInput = document.getElementById('amount');

    const toAccount = toAccountInput.value.trim();
    const amountStr = amountInput.value.trim();
    const amount = parseFloat(amountStr);

    let errors = [];

    // Валидация номера счёта/карты
    if (!toAccount) {
        errors.push('Укажите номер счёта или телефон получателя');
    } else if (!/^\d{20}$/.test(toAccount) && !/^\+?\d{10,15}$/.test(toAccount)) {
        // Если это не 20 цифр (счёт) и не номер телефона — ошибка
        errors.push('Номер счёта должен состоять ровно из 20 цифр или это должен быть телефон (+7...)');
    }

    // Валидация суммы
    if (isNaN(amount) || amount <= 10) {
        errors.push('Сумма перевода должна быть не менее 10 руб.');
    }

    if (amount > 1000000) {
        errors.push('Максимальная сумма перевода — 1 000 000');
    }

    // Проверка, что сумма не больше баланса клиента
    const balanceStr = document.getElementById('balance').innerText.trim();
    const balance = parseFloat(balanceStr.replace(/\s/g, '').replace(',', '.')); // обрабатываем "10 000.00"
    if (!isNaN(balance) && amount > balance) {
        errors.push('Недостаточно средств на счёте');
    }

    if (errors.length > 0) {
        alert('Ошибки:\n' + errors.join('\n'));
        return false;
    }

    return true;
}

function transfer() {
    if (!validateTransfer()) return;

    const toAccountInput = document.getElementById('to-account');
    const amountInput = document.getElementById('amount');

    const toAccount = toAccountInput.value.trim();
    const amount = parseFloat(amountInput.value.trim());

    fetch('/rgz/rest-api/client/transfer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            to_account: toAccount,
            amount: amount
        })
    })
    .then(r => {
        if (!r.ok) {
            return r.json().then(err => {
                alert(err.error || 'Ошибка перевода');
            });
        }
        return r.json();
    })
    .then(() => {
        loadAccount();
        loadHistory();
        toAccountInput.value = '';  // Очистка поля
        amountInput.value = '';     // Очистка поля
        alert('Перевод успешен!');
    })
    .catch(() => {
        alert('Ошибка соединения с сервером');
    });
}


// Менеджер
// Поиск по телефону
function searchUsers() {
    const phone = document.getElementById('search-phone').value.trim();

    if (!phone) {
        alert('Введите номер телефона для поиска');
        return;
    }

    fetch(`/rgz/rest-api/manager/users?phone=${encodeURIComponent(phone)}`)
        .then(r => r.json())
        .then(users => {
            const tbody = document.getElementById('users-table');
            tbody.innerHTML = '';

            if (users.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Пользователи с таким номером телефона не найдены</td></tr>';
                return;
            }

            users.forEach(u => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${u.full_name}</td>
                    <td>${u.login}</td>
                    <td>${u.phone || ''}</td>
                    <td>${u.role}</td>
                    <td>
                        <button onclick="editUser(${u.id})">✏</button>
                        <button onclick="deleteUser(${u.id})">🗑</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(() => {
            alert('Ошибка поиска');
        });
}


function loadUsers() {
    document.getElementById('search-phone').value = ''; // очищаем поле поиска
    fetch('/rgz/rest-api/manager/users')
        .then(r => r.json())
        .then(users => {
            const tbody = document.getElementById('users-table');
            tbody.innerHTML = '';
            users.forEach(u => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${u.full_name}</td>
                    <td>${u.login}</td>
                    <td>${u.phone || ''}</td>
                    <td>${u.role}</td>
                    <td>
                        <button onclick="editUser(${u.id})">✏</button>
                        <button onclick="deleteUser(${u.id})">🗑</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function showAddUser() {
    userModal.style.display = 'block';
    document.getElementById('user-id').value = '';
    document.getElementById('full-name').value = '';
    document.getElementById('user-login').value = '';
    document.getElementById('user-password').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('role').value = 'client';
    document.getElementById('account-number-modal').value = '';
    document.getElementById('balance-modal').value = '';
}

function hideModal() {
    userModal.style.display = 'none';
}

function validateUserForm(isEdit = false) {
    const fullName = document.getElementById('full-name').value.trim();
    const login = document.getElementById('user-login').value.trim();
    const password = document.getElementById('user-password').value;
    const phone = document.getElementById('phone').value.trim();
    const role = document.getElementById('role').value;
    const accountNumber = document.getElementById('account-number-modal').value.trim();
    const balanceStr = document.getElementById('balance-modal').value.trim();

    let errors = [];

    if (!fullName) errors.push('Заполните ФИО');
    if (fullName.length < 2 || fullName.length > 100) errors.push('ФИО: от 2 до 100 символов');

    if (!login) errors.push('Заполните логин');
    if (login.length < 3 || login.length > 50) errors.push('Логин: от 3 до 50 символов');
    if (!/^[a-zA-Z0-9_.-]+$/.test(login)) errors.push('Логин: только лат. буквы, цифры, _, . -');

    if (!isEdit) { // при создании
        if (!password || password.length < 6) errors.push('Пароль: не короче 6 символов');
    }

    if (phone && !/^\+7\d{10}$/.test(phone)) {
        errors.push('Номер телефона должен начинаться с +7 и содержать ровно 10 цифр после +7');
    }

    if (role === 'client') {
        if (!accountNumber) errors.push('Укажите номер счёта');
        if (!/^\d{20}$/.test(accountNumber)) errors.push('Номер счёта: ровно 20 цифр');

        const balance = parseFloat(balanceStr);
        if (isNaN(balance) || balance < 0) errors.push('Баланс: число ≥ 0');
    }

    if (errors.length > 0) {
        alert('Ошибки:\n' + errors.join('\n'));
        return false;
    }

    return true;
}

function saveUser() {
    const id = document.getElementById('user-id').value;
    const isEdit = !!id;

    if (!validateUserForm(isEdit)) return;

    const data = {
        full_name: document.getElementById('full-name').value.trim(),
        login: document.getElementById('user-login').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        role: document.getElementById('role').value
    };

    if (!isEdit) {
        data.password = document.getElementById('user-password').value;
    } else if (document.getElementById('user-password').value) {
        data.password = document.getElementById('user-password').value;
    }

    if (data.role === 'client') {
        data.account_number = document.getElementById('account-number-modal').value.trim();
        data.balance = parseFloat(document.getElementById('balance-modal').value.trim());
    }

    const method = isEdit ? 'PUT' : 'POST';
    const url = isEdit ? `/rgz/rest-api/manager/user/${id}` : '/rgz/rest-api/manager/user';

    fetch(url, {
        method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => {
        if (!r.ok) {
            return r.json().then(err => {
                alert(err.error || 'Ошибка сохранения');
            });
        }
        return r.json();
    })
    .then(() => {
        hideModal();
        loadUsers();
    });
}

function editUser(id) {
    fetch('/rgz/rest-api/manager/users')
        .then(r => r.json())
        .then(users => {
            const u = users.find(user => user.id === id);
            if (u) {
                document.getElementById('user-id').value = u.id;
                document.getElementById('full-name').value = u.full_name;
                document.getElementById('user-login').value = u.login;
                document.getElementById('phone').value = u.phone || '';
                document.getElementById('role').value = u.role;
                document.getElementById('account-number-modal').value = u.account_number || '';
                document.getElementById('balance-modal').value = u.balance || '';
                document.getElementById('user-password').value = ''; // не показываем старый пароль
                userModal.style.display = 'block';
            }
        });
}

function deleteUser(id) {
    if (!confirm('Удалить пользователя?')) return;
    fetch(`/rgz/rest-api/manager/user/${id}`, {method:'DELETE'})
        .then(r => {
            if (!r.ok) alert('Ошибка удаления');
            else loadUsers();
        });
}