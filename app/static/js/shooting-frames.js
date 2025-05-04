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
// Create a new roll row-finished with row
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

    
    // 获取该 roll 的照片（异步）
    fetch(`/shooting/data/photos?roll_id=${roll.id}`)
        .then(res => res.json())
        .then(photos => {
            photos.forEach(photo => {
                const frame = document.createElement('div');
                frame.className = 'film-frame';

                const img = document.createElement('img');
                img.src = photo.image_path.startsWith("http")
                    ? photo.image_path
                    : `/static/uploads/photos/${photo.image_path}`;
                img.style.maxWidth = '100%';
                img.style.maxHeight = '100%';
                img.style.objectFit = 'cover';

                frame.appendChild(img);
                strip.appendChild(frame);
            });

            // 最后加一个上传按钮
            const addFrame = document.createElement('div');
            addFrame.className = 'film-frame upload-frame';
            addFrame.innerHTML = '<span class="plus-icon">+</span>';

            addFrame.addEventListener('click', () => {
                openPhotoUploadModal(roll.id);  // 👈 新增 modal 弹出函数
            });

            strip.appendChild(addFrame);

        });

    // row.appendChild(film);
    // row.appendChild(strip);

    row.appendChild(filmWrapper);
    row.appendChild(strip);


    return row;
}


// 出发frame的上传 modal
function openPhotoUploadModal(rollId) {
    const form = document.getElementById('upload-photo-form');
    form.reset();
    form.roll_id.value = rollId;

    const modal = new bootstrap.Modal(document.getElementById('uploadPhotoModal'));
    modal.show();
}

// 处理上传照片的表单提交
document.getElementById('upload-photo-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    fetch('/shooting/upload_photo', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && form.roll_id.value) {
            bootstrap.Modal.getInstance(document.getElementById('uploadPhotoModal')).hide();

            // 清空并重新渲染当前 roll row
            const parent = document.getElementById('roll-detail-list'); // or your strip container
            parent.innerHTML = '';
            loadFrames(); // 你已有的刷新函数
        }
    });
});





window.createRollRow = createRollRow;
