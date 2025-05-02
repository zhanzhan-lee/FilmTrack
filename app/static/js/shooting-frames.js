document.addEventListener('DOMContentLoaded', function () {
    loadRollDetailView();
    bindRollForm();
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

function createRollRow(roll) {
    const row = document.createElement('div');
    row.className = 'roll-row';

    // const film = document.createElement('div');
    // film.className = 'film-logo-container-frame';
    // film.innerHTML = `
    //     <div class="film-cap axle"></div>
    //     <div class="film-cap top"></div>
    //     <img src="${roll.film_image ? "/static/uploads/films/" + roll.film_image : "/static/images/film_placeholder.png"}" class="film-logo" alt="Film Logo">
    //     <div class="film-cap bottom"></div>
    // `;
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
        openEditRoll(roll.id);
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
