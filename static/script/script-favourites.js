function openModal(title, image, year, description, age, category, duration, watchUrl, videoId) {
  console.log("openModal вызван с параметрами:", title, image, year, description, age, category, duration, watchUrl, videoId);

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

  // Обновление и логика для "Смотреть позже"
  const watchLaterIcon = document.getElementById("modalWatchLaterBtn");
  if (watchLaterIcon) {
    const newWatchLaterIcon = watchLaterIcon.cloneNode(true);
    watchLaterIcon.replaceWith(newWatchLaterIcon);

    newWatchLaterIcon.onclick = function () {
      toggleWatchLater(videoId, this);
    };

    fetch(`/videos/is_watch_later/${videoId}/`)
      .then(res => res.json())
      .then(data => {
        newWatchLaterIcon.classList.toggle("active-watch-later", data.watch_later);
      });
  }

  // Обновление и логика для "Избранное"
  const favoriteIcon = document.getElementById("modalFavoriteBtn");
  if (favoriteIcon) {
    const newFavoriteIcon = favoriteIcon.cloneNode(true);
    favoriteIcon.replaceWith(newFavoriteIcon);

    newFavoriteIcon.onclick = function () {
      toggleFavorite(videoId, this);
    };

    fetch(`/videos/is_favorite/${videoId}/`)
      .then(res => res.json())
      .then(data => {
        newFavoriteIcon.textContent = data.is_favorite ? "star" : "star_border";
        newFavoriteIcon.classList.toggle("active-favorite", data.is_favorite);
      });
  }

  document.getElementById('videoModal').style.display = 'flex';

  const closeButton = document.getElementById('modalCloseButton');
  if (closeButton) {
    closeButton.onclick = closeModal;
  }
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
        el.classList.toggle("active-watch-later", data.watch_later);
      }
    });
}

function toggleFavorite(videoId, el) {
  fetch(`/videos/toggle_favorite/${videoId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: `video_id=${videoId}`,
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === "ok") {
        el.classList.toggle("active-favorite", data.is_favorite);
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
