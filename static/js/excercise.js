document.addEventListener("DOMContentLoaded", () => {
    fetchMuscles();
});

// Function to fetch muscle data and display it
const fetchMuscles = () => {
    fetch("http://127.0.0.1:5000/api/muscles")
        .then((response) => response.json())
        .then((muscles) => {
            const gallery = document.getElementById("gallery");

            if (!gallery) {
                console.error("Gallery element not found in the DOM.");
                return;
            }

            muscles?.forEach(({ id, muscle_name, muscle_image }) => {
                // Create muscle container
                const muscleDiv = document.createElement("div");
                muscleDiv.className = "muscle";
                muscleDiv.onclick = () => setInLocalStorage(id);

                // Add muscle name
                const muscleName = document.createElement("h2");
                muscleName.textContent = muscle_name;

                // Add muscle image
                const muscleImage = document.createElement("img");
                muscleImage.src = muscle_image;
                muscleImage.alt = muscle_name;

                // Append name and image to muscle container
                muscleDiv.append(muscleName, muscleImage);

                // Append muscle container to gallery
                gallery.appendChild(muscleDiv);
            });
        })
        .catch((error) => console.error("Error fetching muscle data:", error));
};

// Function to save ID in localStorage
const setInLocalStorage = (id) => {
    localStorage.setItem("muscleId", id);
    window.location.href = "/muscles"
};
