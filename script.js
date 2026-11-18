// Reveal sections when scrolling
const sections = document.querySelectorAll(".section, .stats");

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
}, {
    threshold: 0.15
});

sections.forEach((section) => {
    section.classList.add("hidden");
    observer.observe(section);
});

// Navbar shadow while scrolling
window.addEventListener("scroll", () => {
    const header = document.querySelector("header");

    if (window.scrollY > 50) {
        header.style.boxShadow = "0 3px 15px #00000010";
    } else {
        header.style.boxShadow = "none";
    }
});
document.getElementById("registerForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const member = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        usn: document.getElementById("usn").value,
        department: document.getElementById("department").value
    };

    const message = document.getElementById("message");

    try {
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(member)
        });

        const result = await response.json();

        message.textContent = result.message;
        message.style.color = response.ok ? "green" : "red";

        if (response.ok) {
            document.getElementById("registerForm").reset();
        }

    } catch (error) {
        message.textContent = "Backend connection failed!";
        message.style.color = "red";
    }

});
// EVENT DETAILS
const eventDetails = {
    "Technology Talks": {
        description: "Explore emerging technologies, interact with experienced speakers and discover new opportunities in technology."
    },

    "Web Development Workshop": {
        description: "Learn HTML, CSS and JavaScript and build your own website through practical activities."
    },

    "Campus Hackathon": {
        description: "Work with a team, solve real-world problems and turn your innovative ideas into working projects."
    }
};


// OPEN EVENT POPUP
function openEvent(eventName) {

    document.getElementById("eventTitle").textContent = eventName;

    document.getElementById("eventDescription").textContent =
        eventDetails[eventName].description;

    document.getElementById("eventModal").style.display = "flex";

    document.getElementById("eventMessage").textContent = "";

    document.getElementById("eventForm").reset();
}


// CLOSE EVENT POPUP
function closeEvent() {
    document.getElementById("eventModal").style.display = "none";
}


// CLOSE WHEN CLICKING OUTSIDE
document.getElementById("eventModal").addEventListener("click", function(event) {

    if (event.target === this) {
        closeEvent();
    }

});


// EVENT REGISTRATION
document.getElementById("eventForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const registration = {
        event_name: document.getElementById("eventTitle").textContent,
        student_name: document.getElementById("eventName").value,
        email: document.getElementById("eventEmail").value,
        usn: document.getElementById("eventUSN").value
    };

    const message = document.getElementById("eventMessage");

    try {

        const response = await fetch("http://127.0.0.1:5000/event-register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(registration)
        });

        const result = await response.json();

        message.textContent = result.message;
        message.style.color = response.ok ? "green" : "red";

        if (response.ok) {
            document.getElementById("eventForm").reset();
        }

    } catch (error) {

        message.textContent = "Unable to connect to backend!";
        message.style.color = "red";

    }

});
// CONTACT FORM
document.getElementById("contactForm").addEventListener("submit", async function(event) {

    event.preventDefault();

    const contactData = {
        name: document.getElementById("contactName").value,
        email: document.getElementById("contactEmail").value,
        subject: document.getElementById("contactSubject").value,
        message: document.getElementById("contactMessage").value
    };

    const status = document.getElementById("contactStatus");

    try {

        const response = await fetch("http://127.0.0.1:5000/contact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(contactData)
        });

        const result = await response.json();

        status.textContent = result.message;
        status.style.color = response.ok ? "green" : "red";

        if (response.ok) {
            document.getElementById("contactForm").reset();
        }

    } catch (error) {

        status.textContent = "Unable to connect to backend!";
        status.style.color = "red";

    }

});