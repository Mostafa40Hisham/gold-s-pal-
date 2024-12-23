// Sample data for coaches
const coaches = [
    { name: "C.Bassam", age: 40, photo: "/static/images/bassam.jpg", link: "https://example.com/a" },
    { name: "C.Hussen informa", age: 40, photo: "/static/images/hussen.png", link: "https://example.com/a" },
    { name: "C.Yousef", age: 40, photo: "/static/images/jmawo.jpg", link: "https://example.com/a" },
    { name: "C.Henio", age: 40, photo: "/static/images/", link: "https://example.com/a" },
    { name: "C.Eldawy", age: 40, photo: "/static/images/eldawy.jpg", link: "https://example.com/a" },
    { name: "C.Hossam mansour", age: 40, photo: "/static/images/hossam.jpg", link: "https://example.com/a" },
    { name: "Dr.Bulk", age: 40, photo: "/static/images/bulk.jpg", link: "https://example.com/a" },
    { name: "C.klmata", age: 35, photo: "/static/images/klmata.jpg", link: "https://example.com/b" },
    { name: "C.androw", age: 50, photo: "/static/images/", link: "https://example.com/c" }
];

// Save coaches to local storage
if (!localStorage.getItem('coaches')) {
    localStorage.setItem('coaches', JSON.stringify(coaches));
}

// Retrieve coaches from local storage
const storedCoaches = JSON.parse(localStorage.getItem('coaches'));

// Display coaches on the page
const container = document.getElementById('coach-container');

storedCoaches.forEach(coach => {
    const card = document.createElement('div');
    card.classList.add('card');

    card.innerHTML = `
        <img src="${coach.photo}" alt="${coach.name}">
        <div class="content">
            <h2>${coach.name}</h2>
            <p>Age: ${coach.age}</p>
            <a href="${coach.link}" target="_blank">View Profile</a>
        </div>
    `;

    container.appendChild(card);
});
