document.addEventListener('DOMContentLoaded', function () {
    loadRollDetailView();
    bindEditRollFormFin(); 
});

function loadRollDetailView() {
    fetch('/shooting/data/rolls')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('roll-detail-list');
            container.innerHTML = '';
            const finishedRolls = data.filter(roll => roll.status === 'finished');

            finishedRolls.forEach(roll => {
                const row = createRollRow(roll);
                container.appendChild(row);
            });
        });
}


function openEditRollFin(id) {
    fetch('/shooting/data/rolls')
        .then(response => response.json())
        .then(data => {
            const roll = data.find(r => r.id === id);
            if (!roll) return;

            const form = document.getElementById('edit-roll-form-fin');
            form.reset();

            form.querySelector('[name=roll_id]').value = roll.id;
            form.querySelector('[name=roll_name]').value = roll.roll_name || '';
            form.querySelector('[name=start_date]').value = roll.start_date || '';
            form.querySelector('[name=end_date]').value = roll.end_date || '';
            form.querySelector('[name=notes]').value = roll.notes || '';
            form.querySelector('[name=film_id]').value = roll.film_id;

            const modal = new bootstrap.Modal(document.getElementById('editRollModalFin'));
            modal.show();
        });
}


function bindEditRollFormFin() {
    const form = document.getElementById('edit-roll-form-fin');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const rollId = form.querySelector('[name=roll_id]').value;
        const formData = new FormData(form);
        formData.set('status', 'finished');  // 强制保持 finished 状态

        fetch(`/shooting/edit_roll/${rollId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                bootstrap.Modal.getInstance(document.getElementById('editRollModalFin')).hide();
                loadRollDetailView(); // 刷新 finished 区域
            } else {
                alert("Failed to update roll.");
            }
        });
    });

    const deleteBtn = document.getElementById('delete-roll-btn-fin');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function () {
            const rollId = form.querySelector('[name=roll_id]').value;
            if (!confirm('Are you sure you want to delete this roll?')) return;

            fetch(`/shooting/delete_roll/${rollId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (response.ok) {
                    bootstrap.Modal.getInstance(document.getElementById('editRollModalFin')).hide();
                    loadRollDetailView(); // 删除后刷新
                } else {
                    alert('Failed to delete roll.');
                }
            });
        });
    }
}



//__________________________________________________________________________







function createRollRow(roll) {
    const row = document.createElement('div');
    row.className = 'roll-row';
    const filmWrapper = document.createElement('div');
    filmWrapper.className = 'film-wrapper';
    
    filmWrapper.innerHTML = `
        <div class="film-logo-container-frame">
            <div class="film-cap axle"></div>
            <div class="film-cap top"></div>
            <img src="${roll.film_image ? "/static/uploads/films/" + roll.film_image : "/static/images/film_placeholder.png"}" class="film-logo" alt="Film Logo">
            <div class="film-cap bottom"></div>
        </div>
        <div class="roll-name-label">${roll.roll_name || 'Untitled Roll'}</div>
    `;
    
    filmWrapper.querySelector('.film-logo-container-frame').addEventListener('click', () => {
        openEditRollFin(roll.id);
    });
    
    


    // film.addEventListener('click', () => {
    //     openEditRoll(roll.id); // If necessary, you can reuse the opening and editing logic of shooting-rolls.js
    // });

    const strip = document.createElement('div');
    strip.className = 'film-strip';

    
    for (let i = 0; i < 5; i++) {
        const frame = document.createElement('div');
        frame.className = 'film-frame';
        frame.innerText = '+';
        frame.addEventListener('click', () => {
            alert(`Upload photo to frame ${i+1} for roll ${roll.roll_name || roll.id}`);
        });
        strip.appendChild(frame);
    }

    // row.appendChild(film);
    // row.appendChild(strip);

    row.appendChild(filmWrapper);
    row.appendChild(strip);


    return row;
}


window.createRollRow = createRollRow;
