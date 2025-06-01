function openModal(title, image, year, description, age, category, duration, watchUrl, videoId) {
  console.log("openModal вызван с параметрами:");
  console.log("title:", title);
  console.log("image:", image);
  console.log("year:", year);
  console.log("description:", description);
  console.log("age:", age);
  console.log("category:", category);
  console.log("duration:", duration);
  console.log("watchUrl:", watchUrl);
  console.log("videoId:", videoId);

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalImage').src = image;
  document.getElementById('modalYear').textContent = year;
  document.getElementById('modalDescription').textContent = description;
  document.getElementById('modalAge').textContent = age;
  document.getElementById('modalCategory').textContent = category;
  document.getElementById('modalDuration').textContent = duration;

  const watchButton = document.getElementById('modalWatchButton');
  watchButton.href = `/videos/watch/${videoId}/`;
  watchButton.textContent = "Смотреть";

  // Сброс обработчиков и установка новых
  const watchLaterIcon = document.getElementById("modalWatchLaterBtn");
  const favoriteIcon = document.getElementById("modalFavoriteBtn");

  watchLaterIcon.replaceWith(watchLaterIcon.cloneNode(true));
  favoriteIcon.replaceWith(favoriteIcon.cloneNode(true));

  const newWatchLaterIcon = document.getElementById("modalWatchLaterBtn");
  const newFavoriteIcon = document.getElementById("modalFavoriteBtn");

  newWatchLaterIcon.onclick = function () {
    toggleWatchLater(videoId, this);
  };
  newFavoriteIcon.onclick = function () {
    toggleFavorite(videoId, this);
  };

  // Статус "Смотреть позже"
  fetch(`/videos/is_watch_later/${videoId}/`)
    .then(response => response.json())
    .then(data => {
      newWatchLaterIcon.classList.toggle("active", data.watch_later === true);
    });

  // Статус "Избранное"
  fetch(`/videos/favorite/${videoId}/`)
    .then(res => res.json())
    .then(data => {
      newFavoriteIcon.textContent = data.is_favorite ? "star" : "star_border";
      newFavoriteIcon.classList.toggle("active", data.is_favorite);
    });

  document.getElementById('videoModal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('videoModal').style.display = 'none';
}

function toggleWatchLater(videoId, el) {
  fetch("/videos/toggle_watch_later/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: `video_id=${videoId}`,
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "ok") {
        el.classList.toggle("active", data.watch_later);
      }
    });
}

function toggleFavorite(videoId, el) {
  fetch(`/videos/favorite/${videoId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: `video_id=${videoId}`
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === "ok") {
        el.classList.toggle("active", data.is_favorite);
        el.textContent = data.is_favorite ? "star" : "star_border";
      }
    });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
