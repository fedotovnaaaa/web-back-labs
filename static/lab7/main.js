function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';

        // Обновляем заголовки таблицы
        document.querySelector('thead tr').innerHTML = `
            <th>Название на русском</th>
            <th>Оригинальное название</th>
            <th>Год</th>
            <th>Действие</th>
        `;

        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // Русское название
            tdTitleRus.innerText = films[i].title_ru;
            
            // Оригинальное название - курсивом в скобках, если оно отличается от русского
            if (films[i].title && films[i].title !== films[i].title_ru) {
                tdTitle.innerHTML = `<em>(${films[i].title})</em>`;
            } else {
                tdTitle.innerHTML = `<em style="color: #888;">(${films[i].title_ru})</em>`;
            }
            
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id); // Используем ID из БД
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}


function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}


function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}


function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}


function cancel() {
    hideModal();
}


function addFilm() {
    // Очищаем все поля формы для создания нового фильма
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    // Очищаем все сообщения об ошибках
    document.querySelectorAll('.error-message').forEach(el => el.innerText = '');
    
    showModal();
}


function validateFilm() {
    // Очищаем все сообщения об ошибках
    document.querySelectorAll('.error-message').forEach(el => el.innerText = '');
    
    // Получаем значения полей, применяя trim() для удаления пробелов по краям
    const titleRu = document.getElementById('title-ru').value.trim();
    const title = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value.trim();
    
    let isValid = true;
    
    // Проверка русского названия
    if (!titleRu) {
        document.getElementById('title-ru-error').innerText = 'Заполните русское название';
        isValid = false;
    }
    
    // Проверка оригинального названия, если русское тоже пустое
    if (!title && !titleRu) {
        document.getElementById('title-error').innerText = 'Заполните название на оригинальном языке';
        isValid = false;
    }
    
    // Проверка года
    if (!year) {
        document.getElementById('year-error').innerText = 'Заполните год выпуска';
        isValid = false;
    } else {
        const currentYear = new Date().getFullYear();
        const yearNum = parseInt(year);
        if (isNaN(yearNum) || yearNum < 1895 || yearNum > currentYear) {
            document.getElementById('year-error').innerText = `Год должен быть числом от 1895 до ${currentYear}`;
            isValid = false;
        }
    }
    
    // Проверка описания
    if (!description) {
        document.getElementById('description-error').innerText = 'Заполните описание';
        isValid = false;
    } else if (description.length > 2000) {
        document.getElementById('description-error').innerText = 'Описание не должно превышать 2000 символов';
        isValid = false;
    }
    
    return isValid;
}


function sendFilm() {
    // Сначала валидируем на клиенте
    if (!validateFilm()) {
        return; // Не отправляем, если есть ошибки
    }
    
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    // Если ID пустой - POST (создание), если ID есть - PUT (обновление)
    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST': 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"}, 
        body: JSON.stringify(film)
    })
    .then (function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        // Отображаем ошибки для каждого поля
        for(const field in errors) {
            const errorElement = document.getElementById(`${field}-error`);
            if(errorElement) {
                errorElement.innerText = errors[field];
            }
        }
    });
}


function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    // Получает данные фильма по ID и заполняет ими форму
    .then(function (film) {
        document.getElementById('id').value = film.id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        
        // Очищаем все сообщения об ошибках
        document.querySelectorAll('.error-message').forEach(el => el.innerText = '');
        
        showModal();
    });
}
