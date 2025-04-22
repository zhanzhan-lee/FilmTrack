document.addEventListener('DOMContentLoaded', function () {
    fetch('/gear/data/cameras')
        .then(response => response.json())
        .then(cameras => {
            const container = document.getElementById('camera-list');
            container.innerHTML = '';  // 清空

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

            // ➕ 添加按钮
            const addBtn = document.createElement('div');
            addBtn.className = 'gear-card add-card';
            addBtn.setAttribute('data-bs-toggle', 'modal');
            addBtn.setAttribute('data-bs-target', '#cameraModal');
            addBtn.innerText = '＋ Add Camera';
            container.appendChild(addBtn);
        });
});
