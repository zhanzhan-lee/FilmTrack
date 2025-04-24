document.addEventListener('DOMContentLoaded', function () {
    loadCameras();
    loadLenses();
    loadFilms();
});

function loadCameras() {
    fetch('/gear/data/cameras')
        .then(response => response.json())
        .then(cameras => {
            const container = document.getElementById('camera-list');
            container.innerHTML = '';

            cameras.forEach(cam => {
                const imgUrl = (!cam.image)
                    ? "/static/images/cam_placeholder.png"
                    : (cam.image.startsWith("http")
                        ? cam.image
                        : "/static/uploads/cameras/" + cam.image);

                const card = document.createElement('div');
                card.className = 'gear-card';
                card.innerHTML = `
                    <img src="${imgUrl}" alt="Camera">
                    <div class="info">
                        <strong>${cam.name}</strong><br>
                        ${cam.brand}<br>
                        <span class="subtext">${cam.type} · ${cam.format}</span>
                    </div>
                `;
                container.appendChild(card);
            });

            const addBtn = document.createElement('div');
            addBtn.className = 'gear-card add-card';
            addBtn.setAttribute('data-bs-toggle', 'modal');
            addBtn.setAttribute('data-bs-target', '#cameraModal');
            addBtn.innerText = '＋ Add Camera';
            container.appendChild(addBtn);
        });
}


function loadLenses() {
    fetch('/gear/data/lenses')
        .then(response => response.json())
        .then(lenses => {
            const container = document.getElementById('lens-list');
            container.innerHTML = '';

            lenses.forEach(lens => {
                const imgUrl = (!lens.image)
                    ? "/static/images/lens_placeholder.png"
                    : (lens.image.startsWith("http")
                        ? lens.image
                        : "/static/uploads/lenses/" + lens.image);

                const card = document.createElement('div');
                card.className = 'gear-card';
                card.innerHTML = `
                    <img src="${imgUrl}" alt="Lens">
                    <div class="info">
                        <strong>${lens.name}</strong><br>
                        ${lens.brand}<br>
                        <span class="subtext">${lens.mount_type}</span>
                    </div>
                `;
                container.appendChild(card);
            });

            const addBtn = document.createElement('div');
            addBtn.className = 'gear-card add-card';
            addBtn.setAttribute('data-bs-toggle', 'modal');
            addBtn.setAttribute('data-bs-target', '#lensModal');
            addBtn.innerText = '＋ Add Lens';
            container.appendChild(addBtn);
        });
}


function loadFilms() {
    fetch('/gear/data/films')
        .then(response => response.json())
        .then(films => {
            const container = document.getElementById('film-list');
            container.innerHTML = '';

            films.forEach(film => {
                const imgUrl = (!film.image)
                    ? "/static/images/film_placeholder.png"
                    : (film.image.startsWith("http")
                        ? film.image
                        : "/static/uploads/films/" + film.image);

                const card = document.createElement('div');
                card.className = 'gear-card';
                card.innerHTML = `
                    <img src="${imgUrl}" alt="Film">
                    <div class="info">
                        <strong>${film.name}</strong><br>
                        ${film.brand}<br>
                        <span class="subtext">ISO ${film.iso} · ${film.format}</span>
                    </div>
                `;
                container.appendChild(card);
            });

            const addBtn = document.createElement('div');
            addBtn.className = 'gear-card add-card';
            addBtn.setAttribute('data-bs-toggle', 'modal');
            addBtn.setAttribute('data-bs-target', '#filmModal');
            addBtn.innerText = '＋ Add Film';
            container.appendChild(addBtn);
        });
}

// ____________________________________________________________________________________________


$(function () {
    $('#camera-form').on('submit', function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      $.ajax({
        url: '/gear/upload_camera',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function () {
          $('#cameraModal').modal('hide');
          $('#camera-form')[0].reset();  // 清空表单
          loadCameras();  // 🔁 实时刷新
        },
        error: function () {
          alert("Upload failed.");
        }
      });
    });
  });
  
  $('#lens-form').on('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    $.ajax({
        url: '/gear/upload_lens',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function () {
            $('#lensModal').modal('hide');
            $('#lens-form')[0].reset();
            loadLenses();
        },
        error: function () {
            alert("Upload lens failed.");
        }
    });
});

$('#film-form').on('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    $.ajax({
        url: '/gear/upload_film',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function () {
            $('#filmModal').modal('hide');
            $('#film-form')[0].reset();
            loadFilms();
        },
        error: function () {
            alert("Upload film failed.");
        }
    });
});
