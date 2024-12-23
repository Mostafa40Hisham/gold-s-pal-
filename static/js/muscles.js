const muscleId = localStorage.getItem("muscleId"); // Retrieve the muscle ID from localStorage

console.log(muscleId);
document.addEventListener("DOMContentLoaded", () => {
    if (muscleId) {
        fetchMuscleById(muscleId); // Fetch muscle data if an ID exists
    }
});

// Function to fetch muscle by ID
const fetchMuscleById = (id) => {
    fetch(`http://127.0.0.1:5000/api/muscles/${id}`)
        .then((response) => {
            if (!response.ok) {
                console.error("Error fetching muscle by ID:", response.statusText);
                return;
            }
            return response.json();
        })
        .then((muscle) => {
            console.log(muscle);
            displaySectionButtons(muscle); // Display buttons for sections
        })
        .catch((error) => {
            console.error("Error fetching muscle by ID:", error);
        });
};

// Function to display buttons for each section (e.g., "inner", "lower")
const displaySectionButtons = (muscle) => {
    const sections = muscle.sections; // Get the sections object

    if (!sections) return; // If no sections, return early

    const container = document.getElementById("buttons-container");
    container.innerHTML = ''; // Clear previous buttons

    // Loop through the sections and create buttons for each (e.g., "lower", "inner")
    Object.keys(sections).forEach((sectionKey) => {
        const button = document.createElement("button");
        button.textContent = sectionKey; // Set section name as button text
        // Optional: Add event listener for button click (if needed)
        button.addEventListener("click", () => {
            localStorage.setItem("sectionName", sectionKey)
            window.location.href = "/muscleTraning"
        });

        // Append button to the container
        container.appendChild(button);
    });
};
