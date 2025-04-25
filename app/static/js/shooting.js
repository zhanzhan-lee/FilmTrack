document.addEventListener('DOMContentLoaded', function () {
    loadRolls();
    loadFilmOptions();
    bindRollForm();
});


// -----------------------------
// 加载 roll 卡片列表
// -----------------------------
function loadRolls() {
    fetch('/shooting/data/rolls')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('roll-list');
            container.innerHTML = '';
            data.forEach(roll => {
                const card = createRollCard(roll);
                container.appendChild(card);
            });
        });
}


// -----------------------------
// 加载 film 下拉选项（用于两个 modal）
// -----------------------------
function loadFilmOptions() {
    fetch('/gear/data/films')
        .then(response => response.json())
        .then(films => {
            const addSelect = document.getElementById('roll-film-select');
            const editSelect = document.getElementById('edit-roll-film-select');

            [addSelect, editSelect].forEach(select => {
                select.innerHTML = '';
                films.forEach(film => {
                    const opt = document.createElement('option');
                    opt.value = film.id;
                    opt.textContent = `${film.brand} ${film.name}`;
                    select.appendChild(opt);
                });
            });
        });
}


function createRollCard(roll) {
    const card = document.createElement('div');
    card.className = 'card mb-3 p-3';

    card.innerHTML = `
        <h5>${roll.roll_name || '(Untitled Roll)'}</h5>
        <p><strong>Film:</strong> ${roll.film_name || '—'}</p>
        <p><strong>Status:</strong> ${roll.status || '—'}</p>
        <p><strong>Start:</strong> ${roll.start_date || '—'} | <strong>End:</strong> ${roll.end_date || '—'}</p>
        <p><strong>Notes:</strong> ${roll.notes}</p>
        <button class="btn btn-sm btn-outline-primary mr-2" onclick="openEditRoll(${roll.id})">Edit</button>
        <button class="btn btn-sm btn-outline-danger" onclick="deleteRoll(${roll.id})">Delete</button>
    `;

    return card;
}
