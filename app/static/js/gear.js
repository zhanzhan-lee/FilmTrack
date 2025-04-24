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

                card.setAttribute('data-id', cam.id); // 添加数据属性以存储相机ID


                card.innerHTML = `
                    <img src="${imgUrl}" alt="Camera" onerror="this.onerror=null;this.src='/static/images/cam_placeholder.png';">

                    <div class="info">
                        <strong>${cam.name}</strong><br>
                        ${cam.brand}<br>
                        <span class="subtext">${cam.type} · ${cam.format}</span>
                    </div>
                `;

                card.addEventListener('click', () => openEditCameraModal(cam)); // 点击事件!!!!!


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
                    <img src="${imgUrl}" alt="Lens" onerror="this.onerror=null;this.src='/static/images/lens_placeholder.png';">
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
                    <img src="${imgUrl}" alt="Film" onerror="this.onerror=null;this.src='/static/images/film_placeholder.png';">
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
// Modal for adding a new gear

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


// ____________________________________________________________________________________________
// Modal for editing a new camera


function openEditCameraModal(cam) {
    $('#camera-edit-form input[name="id"]').val(cam.id);
    $('#camera-edit-form input[name="name"]').val(cam.name);
    $('#camera-edit-form input[name="brand"]').val(cam.brand);
    $('#camera-edit-form select[name="type"]').val(cam.type);
    $('#camera-edit-form select[name="format"]').val(cam.format);
    $('#camera-edit-form input[name="is_public"]').prop('checked', cam.is_public);
    $('#camera-edit-form input[name="image"]').val('');
  
    const modal = new bootstrap.Modal(document.getElementById('cameraEditModal'));
    modal.show();
  
    // 删除按钮事件
    $('#camera-delete-btn').off('click').on('click', function () {
      deleteCamera(cam.id, modal);
    });
  }
  
  $('#camera-edit-form').on('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const id = formData.get('id');
  
    $.ajax({
      url: `/gear/edit_camera/${id}`,
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      success: function () {
        $('#cameraEditModal').modal('hide');
        $('#camera-edit-form')[0].reset();
        loadCameras(); // 刷新页面
      },
      error: function () {
        alert("Update failed.");
      }
    });
  });
  
  function deleteCamera(id, modalInstance) {
    if (!confirm("Are you sure you want to delete this camera?")) return;
  
    $.ajax({
      url: `/gear/delete_camera/${id}`,
      type: 'DELETE',
      success: function () {
        modalInstance.hide();
        loadCameras();
      },
      error: function () {
        alert("Failed to delete.");
      }
    });
  }
  