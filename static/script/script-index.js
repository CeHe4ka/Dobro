// function openModal(title, image, year, description, age, category, duration) {
//         document.getElementById('modalTitle').textContent = title;
//         document.getElementById('modalImage').src = image;
//         document.getElementById('modalYear').textContent = year;
//         document.getElementById('modalDescription').textContent = description;
//         document.getElementById('modalAge').textContent = age;
//         document.getElementById('modalCategory').textContent = category;
//         document.getElementById('modalDuration').textContent = duration;
//         document.getElementById('videoModal').style.display = 'flex';
//         }

//         function closeModal() {
//         document.getElementById('videoModal').style.display = 'none';
//         }







function handleClick(button) {
  const title = button.dataset.title;
  const img = button.dataset.img;
  const year = button.dataset.year;
  const description = button.dataset.description;
  const age = button.dataset.age;
  const category = button.dataset.category;
  const duration = button.dataset.duration;
  const link = button.dataset.link;

  openModal(title, img, year, description, age, category, duration, link);
}

function openModal(title, img, year, description, age, category, duration, link) {
  document.getElementById("modalTitle").textContent = title;
  document.getElementById("modalImage").src = img;
  document.getElementById("modalYear").textContent = year;
  document.getElementById("modalDescription").textContent = description;
  document.getElementById("modalAge").textContent = age;
  document.getElementById("modalCategory").textContent = category;
  document.getElementById("modalDuration").textContent = duration;

  // Ссылка в кнопке "Смотреть фильм"
  document.getElementById("watchMovieBtn").href = link;

  // Показываем модальное окно
  document.getElementById("videoModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("videoModal").style.display = "none";
}




// function openModal(title, image, year, description, age, category, duration, link) {
//       document.getElementById('modalTitle').textContent = title;
//       document.getElementById('modalImage').src = image;
//       document.getElementById('modalYear').textContent = year;
//       document.getElementById('modalDescription').textContent = description;
//       document.getElementById('modalAge').textContent = age;
//       document.getElementById('modalCategory').textContent = category;
//       document.getElementById('modalDuration').textContent = duration;
//       document.getElementById('videoModal').style.display = 'flex';
//     }

//     const watchBtn = document.getElementById("watchMovieBtn");
//     watchBtn.href = link;

//     document.getElementById("videoModal").style.display = "block";

//     function closeModal() {
//       document.getElementById('videoModal').style.display = 'none';
//     }
    