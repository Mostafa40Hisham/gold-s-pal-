const muscleId = +localStorage.getItem("muscleId");
const sectionName = localStorage.getItem("sectionName");
console.log(typeof (muscleId));

// Define the API endpoint, dynamically including muscleId and sectionName
const apiUrl = `http://127.0.0.1:5000/muscles/${muscleId}/sections/${sectionName}`;

// Fetch data from the API
fetch(apiUrl)
    .then((response) => {
        if (response.status === 404) {
            throw new Error("API endpoint not found (status 404)");
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);

        // Create a list of exercises and display them
        const exerciseList = document.getElementById("exercise-list");

        for (const exerciseName in data) {
            const exerciseImage = data[exerciseName];

            const exerciseCard = document.createElement("div");
            exerciseCard.classList.add("exercise-card");

            exerciseCard.innerHTML = `
            <img src="${exerciseImage}" alt="${exerciseName}" />
            <h3>${exerciseName}</h3>

          `;

            exerciseList.appendChild(exerciseCard);
        }
    })
    .catch((error) => {
        console.error("Error fetching data:", error);
    });