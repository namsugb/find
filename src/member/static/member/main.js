// DOM Elements
const categoriesDiv = document.getElementById("categories");
const resultsDiv = document.getElementById("results");
const searchBtn = document.getElementById("search-btn");

// State for selected skills
let selectedSkills = [];

// Fetch categories and skills from API
async function fetchCategories() {
  try {
    const response = await fetch("api/categories/");
    const categories = await response.json();
    renderCategories(categories);
  } catch (error) {
    console.error("Error fetching categories:", error);
  }
}

// Render categories and skills
function renderCategories(categories) {
  categoriesDiv.innerHTML = "";
  categories.forEach((category) => {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category";

    const title = document.createElement("h2");
    title.textContent = category.name;

    const description = document.createElement("p");
    description.textContent = category.description;

    const skillsDiv = document.createElement("div");
    skillsDiv.className = "skills";

    category.skills.forEach((skill) => {
      const button = document.createElement("button");
      button.textContent = skill.name;
      button.dataset.skillId = skill.id;

      // Toggle selection
      button.addEventListener("click", () => {
        const skillId = parseInt(button.dataset.skillId, 10);
        if (selectedSkills.includes(skillId)) {
          selectedSkills = selectedSkills.filter((id) => id !== skillId);
          button.classList.remove("selected");
        } else {
          selectedSkills.push(skillId);
          button.classList.add("selected");
        }
      });

      skillsDiv.appendChild(button);
    });

    categoryDiv.appendChild(title);
    categoryDiv.appendChild(description);
    categoryDiv.appendChild(skillsDiv);
    categoriesDiv.appendChild(categoryDiv);
  });
}

// Fetch users based on selected skills
async function fetchUsers() {
  if (selectedSkills.length === 0) {
    alert("Please select at least one skill!");
    return;
  }

  try {
    const params = new URLSearchParams();
    selectedSkills.forEach((skillId) => params.append("skills", skillId));

    const response = await fetch(`api/search-users/?${params.toString()}`);
    const users = await response.json();
    renderUsers(users);
  } catch (error) {
    console.error("Error fetching users:", error);
  }
}

function renderUsers(users) {
  resultsDiv.innerHTML = "<h2>Users</h2>";
  if (users.length === 0) {
    resultsDiv.innerHTML += "<p>No users found.</p>";
    return;
  }

  users.forEach((user) => {
    const userDiv = document.createElement("div");
    userDiv.className = "user";
    userDiv.style.cursor = "pointer";

    const username = document.createElement("h3");
    username.textContent = user.username;

    const bio = document.createElement("p");
    bio.textContent = user.bio;

    const profilePicture = document.createElement("img");
    if (user.profile_picture) {
      profilePicture.src = user.profile_picture;
      profilePicture.alt = `${user.username}'s profile picture`;
    } else {
      profilePicture.src = "https://via.placeholder.com/50";
      profilePicture.alt = "Default profile picture";
    }

    // 클릭 이벤트로 개인 페이지로 이동
    userDiv.addEventListener("click", () => {
      window.location.href = `/member/users/${user.id}/`;
    });

    userDiv.appendChild(profilePicture);
    userDiv.appendChild(username);
    userDiv.appendChild(bio);
    resultsDiv.appendChild(userDiv);
  });
}


// Initial fetch
fetchCategories();

// Add event listener to Search button
searchBtn.addEventListener("click", fetchUsers);

