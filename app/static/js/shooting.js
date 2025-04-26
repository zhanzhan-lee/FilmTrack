document.addEventListener('DOMContentLoaded', function () {
    loadRolls();
    loadFilmOptions();
    bindRollForm();
    bindEditRollForm();
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
            const addBtn = document.createElement('div');
            addBtn.className = 'gear-card add-card'; // 用原 gear 样式
            addBtn.innerText = '＋ Add New Roll';
            addBtn.addEventListener('click', openAddRollModal); // 点击打开新增 modal
            container.appendChild(addBtn);
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
    card.className = 'gear-card';

    // 判断图片
    const imgUrl = (!roll.film_image)
        ? "/static/images/film_placeholder.png"
        : (roll.film_image.startsWith("http")
            ? roll.film_image
            : "/static/uploads/films/" + roll.film_image);

    card.innerHTML = `
        <div class="film-logo-container">
            <div class="film-cap axle"></div>
            <div class="film-cap top"></div>
            <img src="${imgUrl}" class="film-logo" alt="Film Logo">
            <div class="film-cap bottom"></div>
        </div>

        
        
        <div class="info">
            <h5>${roll.roll_name || '(Untitled Roll)'}</h5>
            <p class="subtext"><strong>Film:</strong> ${roll.film_name || '—'}</p>
            <p class="subtext"><strong>Status:</strong> ${roll.status || '—'}</p>
            <p class="subtext"><strong>Start:</strong> ${roll.start_date || '—'} <br> <strong>End:</strong> ${roll.end_date || '—'}</p>
            <p class="subtext"><strong>Notes:</strong> ${roll.notes}</p>
        </div>
        <div class="mt-2">
            <button class="btn btn-sm btn-outline-primary me-2" onclick="openEditRoll(${roll.id})">Edit</button>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteRoll(${roll.id})">Delete</button>
        </div>
    `;

    return card;
}




function openEditRoll(id) {
    fetch('/shooting/data/rolls')  // 简化用全部数据找对应 roll（你也可以开个 /shooting/data/rolls/<id> 接口）
        .then(response => response.json())
        .then(data => {
            const roll = data.find(r => r.id === id);
            if (!roll) return;

            document.getElementById('edit-roll-id').value = roll.id;
            document.getElementById('edit-roll-name').value = roll.roll_name || '';
            document.getElementById('edit-roll-start').value = roll.start_date || '';
            document.getElementById('edit-roll-end').value = roll.end_date || '';
            document.getElementById('edit-roll-status').value = roll.status || '';
            document.getElementById('edit-roll-notes').value = roll.notes || '';

            const filmSelect = document.getElementById('edit-roll-film-select');
            filmSelect.value = roll.film_id;

            // modal
            const modal = new bootstrap.Modal(document.getElementById('editRollModal'));
            modal.show();
        });
}

function deleteRoll(id) {
    if (!confirm('Are you sure you want to delete this roll?')) return;

    fetch(`/shooting/delete_roll/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            loadRolls(); // 刷新列表
        } else {
            alert('Failed to delete roll.');
        }
    });
}


function bindEditRollForm() {
    const form = document.getElementById('edit-roll-form');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const rollId = document.getElementById('edit-roll-id').value;
        const formData = new FormData(form);

        fetch(`/shooting/edit_roll/${rollId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // 隐藏 modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('editRollModal'));
                modal.hide();

                // 刷新列表
                loadRolls();
            } else {
                alert("Failed to update roll.");
            }
        });
    });
}


function bindRollForm() {
    const form = document.getElementById('roll-form');  // ⬅️ 你的 add Roll form id 是 roll-form

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // 阻止浏览器默认提交

        const formData = new FormData(form);

        fetch('/shooting/upload_roll', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // 隐藏 modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('rollModal'));
                modal.hide();

                // 清空表单
                form.reset();

                // 刷新 roll 列表
                loadRolls();
            } else {
                alert('Failed to add roll.');
            }
        });
    });
}

function openAddRollModal() {
    const modal = new bootstrap.Modal(document.getElementById('rollModal'));
    modal.show();
}