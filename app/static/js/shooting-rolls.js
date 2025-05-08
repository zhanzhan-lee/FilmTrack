document.addEventListener('DOMContentLoaded', function () {
    loadRolls();
    loadFilmOptions();
    bindRollForm();
    bindEditRollFormUse();
});


// -----------------------------
// 加载 roll 卡片列表 loadRolls card list
// -----------------------------
function loadRolls() {
    fetch('/shooting/data/rolls')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('roll-list');
            container.innerHTML = '';
            const inUseRolls = data.filter(roll => roll.status === 'in use');

            inUseRolls.forEach(roll => {
                const card = createRollCard(roll);
                container.appendChild(card);
            });


            const addCard = document.createElement('div');
            addCard.className = 'gear-card';
            
            // create a fake roll pot
            addCard.innerHTML = `
                <div class="film-logo-container" id="add-roll-btn">
                    <div class="film-cap axle"></div>
                    <div class="film-cap top"></div>
                    <div class="film-add-body">
                        <div class="add-roll-text">＋ Add New Roll</div>
                    </div>
                    <div class="film-cap bottom"></div>
                </div>
            
             
            `;
            
            // click roll pot to open modal 
            addCard.querySelector('#add-roll-btn').addEventListener('click', openAddRollModal);
            
            container.appendChild(addCard);
            
        });
}


// -----------------------------
// Load the film dropdown options (for both modals)
// -----------------------------
function loadFilmOptions() {
    fetch('/gear/data/films')
        .then(response => response.json())
        .then(films => {
            const targets = [
                document.getElementById('roll-film-select'),
                document.getElementById('edit-roll-film-select-use'),
                document.getElementById('edit-roll-film-select-fin')
            ];

            targets.forEach(select => {
                if (!select) return;
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
            <p class="subtext"><strong>Start:</strong> ${roll.start_date || '—'}</p>
            <button class="btn btn-sm btn-outline-success mt-2" data-finish-roll="${roll.id}">
                 Mark as Finished
            </button>
        </div>

 
    `;
    card.querySelector('.film-logo-container').addEventListener('click', () => {
        openEditRollUse(roll.id);
    });
    return card;
}




function openEditRollUse(id) {
    fetch('/shooting/data/rolls')
        .then(response => response.json())
        .then(data => {
            const roll = data.find(r => r.id === id);
            if (!roll) return;

            document.querySelector('#edit-roll-form-use [name=roll_id]').value = roll.id;
            document.querySelector('#edit-roll-form-use [name=roll_name]').value = roll.roll_name || '';
            document.querySelector('#edit-roll-form-use [name=start_date]').value = roll.start_date || '';
            document.querySelector('#edit-roll-form-use [name=notes]').value = roll.notes || '';

            const filmSelect = document.querySelector('#edit-roll-form-use [name=film_id]');
            filmSelect.value = roll.film_id;

            const modal = new bootstrap.Modal(document.getElementById('editRollModalUse'));
            
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
            loadRolls(); // Refresh List
        } else {
            alert('Failed to delete roll.');
        }
    });
}


function bindEditRollFormUse() {
    const form = document.getElementById('edit-roll-form-use');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const rollId = form.querySelector('[name=roll_id]').value;
        const formData = new FormData(form);

        fetch(`/shooting/edit_roll/${rollId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('editRollModalUse'));
                modal.hide();
                loadRolls(); // 重新加载卡片列表
            } else {
                alert("Failed to update roll.");
            }
        });
    });

    const deleteBtn = document.getElementById('delete-roll-btn-use');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function () {
            const rollId = form.querySelector('[name=roll_id]').value;
            if (!confirm('Are you sure you want to delete this roll?')) return;

            fetch(`/shooting/delete_roll/${rollId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('editRollModalUse'));
                    modal.hide();
                    loadRolls(); // 删除后刷新
                } else {
                    alert('Failed to delete roll.');
                }
            });
        });
    }
}



function bindRollForm() {
    const form = document.getElementById('roll-form');  

    form.addEventListener('submit', function (e) {
        e.preventDefault(); //Prevent browsers from submitting by default

        const formData = new FormData(form);

        fetch('/shooting/upload_roll', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // hide modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('rollModal'));
                modal.hide();

                // Clear form
                form.reset();

                // Refresh the roll list
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





// finish roll
document.addEventListener('click', function (e) {
    if (e.target.matches('[data-finish-roll]')) {
        const rollId = e.target.getAttribute('data-finish-roll');
        const form = document.getElementById('finish-roll-form');
        form.reset();
        form.querySelector('[name=roll_id]').value = rollId;

        const modal = new bootstrap.Modal(document.getElementById('finishRollModal'));
        modal.show();
    }
});

document.getElementById('finish-roll-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const rollId = form.querySelector('[name=roll_id]').value;
    const formData = new FormData(form);

    fetch(`/shooting/finish_roll/${rollId}`, {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('finishRollModal'));
            modal.hide();
            loadRolls(); // ✅ 刷新 roll 列表
            loadRollDetailView(); // ✅ 刷新详情视图
        } else {
            alert(data.message || 'Failed to mark roll as finished.');
        }
    })
    .catch(() => {
        alert('Server error. Please try again.');
    });
});
