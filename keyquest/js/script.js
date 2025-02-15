// Data for programming questions & topics
const data = {
    JavaScript: {
        "Important Questions": [
            "What is closure in JavaScript?",
            "Explain event delegation.",
            "Difference between == and ===?",
            "What is the event loop?",
            "How do Promises work?",
            "What are JavaScript prototypes?",
            "Explain hoisting in JavaScript.",
            "What is localStorage and sessionStorage?",
        ],
        "Important Topics": [
            "Asynchronous JavaScript",
            "Event Loop",
            "Promises & Async/Await",
            "Closures",
            "Hoisting",
            "JavaScript ES6 Features",
            "JavaScript Modules",
            "Functional Programming in JavaScript",
        ],
    },
    Python: {
        "Important Questions": [
            "What is the difference between list and tuple?",
            "Explain Python's GIL (Global Interpreter Lock).",
            "What are Python decorators?",
            "What is the difference between deep copy and shallow copy?",
            "How does memory management work in Python?",
            "What is the purpose of the `self` keyword in Python?",
            "Explain Python's lambda functions.",
            "How does exception handling work in Python?",
        ],
        "Important Topics": [
            "Object-Oriented Programming",
            "Lambda Functions",
            "Generators & Iterators",
            "Python Data Structures",
            "Multithreading and Concurrency",
            "Python Modules and Packages",
            "File Handling in Python",
            "Python Regular Expressions",
        ],
    },
    Java: {
        "Important Questions": [
            "What is the difference between JDK, JRE, and JVM?",
            "What is method overloading and method overriding?",
            "Explain garbage collection in Java.",
            "What are access specifiers in Java?",
            "What is the difference between an interface and an abstract class?",
            "Explain multithreading in Java.",
            "What is a singleton class in Java?",
            "What are Java collections?",
        ],
        "Important Topics": [
            "Multithreading",
            "Exception Handling",
            "Java Collections Framework",
            "OOP Concepts in Java",
            "Garbage Collection Mechanism",
            "File Handling in Java",
            "Java Streams API",
            "Memory Management in Java",
        ],
    },
};

// Select elements
const languageSelect = document.getElementById("languageSelect");
const questionsBtn = document.getElementById("questionsBtn");
const topicsBtn = document.getElementById("topicsBtn");
const contentDisplay = document.getElementById("contentDisplay");
const contentTitle = document.getElementById("contentTitle");
const contentList = document.getElementById("contentList");

// Handle language selection
languageSelect.addEventListener("change", function () {
    const selectedLanguage = this.value;
    if (selectedLanguage) {
        questionsBtn.disabled = false;
        topicsBtn.disabled = false;
    } else {
        questionsBtn.disabled = true;
        topicsBtn.disabled = true;
        contentDisplay.style.display = "none"; // Hide content
    }
});

// Handle category selection
function displayContent(category) {
    const selectedLanguage = languageSelect.value;
    if (!selectedLanguage) return;

    const items = data[selectedLanguage][category];
    contentTitle.innerText = category;
    contentList.innerHTML = ""; // Clear previous list

    // Add new list items
    items.forEach(item => {
        const li = document.createElement("li");
        li.innerText = item;
        contentList.appendChild(li);
    });

    contentDisplay.style.display = "block"; // Show content
}

// Event listeners for buttons
questionsBtn.addEventListener("click", () => displayContent("Important Questions"));
topicsBtn.addEventListener("click", () => displayContent("Important Topics"));
