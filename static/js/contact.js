// Save contact data to local storage
const contactData = {
    companyName: "INGOUDE COMPANY",
    email: "ahmedby3com@gmail.com",
    address: "123 Nile Street, Cairo, Egypt",
    website: "http://www.goldespal.com/",
    phone: "01115515851"
};

// Save to localStorage
localStorage.setItem("contactData", JSON.stringify(contactData));

// Load contact data from local storage and display it
const savedData = JSON.parse(localStorage.getItem("contactData"));

if (savedData) {
    document.getElementById("company-name").textContent = savedData.companyName;
    document.getElementById("email").textContent = savedData.email;
    document.getElementById("address").textContent = savedData.address;
    document.getElementById("website").textContent = savedData.website;
    document.getElementById("website").href = savedData.website;
    document.getElementById("phone").textContent = savedData.phone;
} else {
    console.error("No contact data found in local storage!");
}