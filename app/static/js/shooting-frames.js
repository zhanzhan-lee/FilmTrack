document.addEventListener('DOMContentLoaded', function () {
    loadRollDetailView();
});

function loadRollDetailView() {
    fetch('/shooting/data/rolls')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('roll-detail-list');
            container.innerHTML = '';

            data.forEach(roll => {
                const row = createRollRow(roll);
                container.appendChild(row);
            });
        });
}

function createRollRow(roll) {
    const row = document.createElement('div');
    row.className = 'roll-row';

    const film = document.createElement('div');
    film.className = 'film-logo-container-frame';
    film.innerHTML = `
        <div class="film-cap axle"></div>
        <div class="film-cap top"></div>
        <img src="${roll.film_image ? "/static/uploads/films/" + roll.film_image : "/static/images/film_placeholder.png"}" class="film-logo" alt="Film Logo">
        <div class="film-cap bottom"></div>
    `;
    film.addEventListener('click', () => {
        openEditRoll(roll.id); // 如果需要可以复用 shooting-rolls.js 的打开编辑逻辑
    });

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

    row.appendChild(film);
    row.appendChild(strip);

    return row;
}


