const API = "http://127.0.0.1:8000"
const token = localStorage.getItem("token");
if(!token){
    window.location.href= "index.html"
} 
function getToken() {
    return localStorage.getItem("token");
}

let allEvents = []

async function loadEvents(){
    try{
        const response = await fetch(
        `${API}/events`,
        {
            method:"GET",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${getToken()}`
            },
        }
    )
    const events = await response.json()
    allEvents = events
    renderEvents(events)
}
    catch (err) {
        console.error(err);
        alert("Failed to load events");
    }
}

function renderEvents(events){
    const eventsDiv = document.getElementById("events")
    eventsDiv.innerHTML="";

    const html = events.map(event => 
       `<div class="element-card">
            <div class="card-holder" onclick="toggleNotes(${event.id})">
              <h2>Title: ${event.title}</h2>
              <h2>Category: ${event.category}</h2>
              <h2>Due Date: ${event.due_date}</h2>
              <h2>Priority: ${event.priority}</h2>
              <h2>Status: ${event.status}</h2>
            </div>
            <div class="notes-section" id="notes-${event.id}">
                <p class="notes-text">Notes: ${event.notes}</p>
                <div class="btn-group">
                   <button class="edit-btn" onclick="showEditForm(${event.id})">Edit</button>
                   <button class="delete-btn" onclick="deleteEvent(${event.id})">Delete</button>
                </div>
            </div>
            <div class="edit-form" id="edit-form-${event.id}">
                <input type="text" id="edit-title-${event.id}" value="${event.title}">
                <input type="text" id="edit-category-${event.id}" value="${event.category}">
                <input type="date" id="edit-date-${event.id}" value="${event.due_date}">
                <select id="edit-priority-${event.id}">
                    <option ${event.priority === "Low" ? "selected" : "" }> Low </option>
                    <option ${event.priority === "Medium" ? "selected" : "" }> Medium </option> 
                    <option ${event.priority === "High" ? "selected" : "" }> High </option>
                </select>
                <select id="edit-status-${event.id}" >
                    <option ${event.status === "Pending" ? "selected" : "" }> Pending </option>
                    <option ${event.status === "Completed" ? "selected" : "" }> Completed </option>
                </select>
                <textarea id="edit-notes-${event.id}">${event.notes}</textarea>
                <button class="save-btn" onclick="updateEvent(${event.id})" > Save Changes </button>
            </div>
        </div>`).join("");
    eventsDiv.innerHTML = html
     }


async function addEvent(){
    const payload = {
            title : document.getElementById("title").value,
            category : document.getElementById("category").value,
            due_date : document.getElementById("due_date").value,
            priority : document.getElementById("priority").value,
            status : document.getElementById("status").value,
            notes : document.getElementById("notes").value
    }
    try{
    const response = await fetch(
        `${API}/events`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "Authorization":`Bearer ${getToken()}`
            },
            body:JSON.stringify(payload)
        }
    )
    const data = await response.json()
    alert(data.message)

    loadEvents()
    } catch (err) {
        console.error(err);
        alert("Failed to create event");
    }
}

async function deleteEvent(id){
    try{
        await fetch(
        `${API}/events/${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization":`Bearer ${getToken()}`
            }
        }
    )
    loadEvents()
   }
   catch (err) {
        console.error(err);
        alert("Delete Failed");
    }

}

function showEditForm(id) {
    const form = document.getElementById(`edit-form-${id}`)
    if (form.style.display === "block") {
        form.style.display = "none"
    }
    else {
        form.style.display = "block"
    }
}

async function updateEvent(id){
    const title = document.getElementById(`edit-title-${id}`).value
    const category = document.getElementById(`edit-category-${id}`).value
    const due_date = document.getElementById(`edit-date-${id}`).value
    const priority = document.getElementById(`edit-priority-${id}`).value
    const status = document.getElementById(`edit-status-${id}`).value
    const notes = document.getElementById(`edit-notes-${id}`).value
    
    const response = await fetch(
        `${API}/events/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":"application/json",
                "Authorization":`Bearer ${getToken()}`
            },
            body:JSON.stringify({
                title,
                category,
                due_date,
                priority,
                status,
                notes
            })
        }
    )

    loadEvents()
}

function searchEvents(){
    const value = document.getElementById("search").value.toLowerCase()
    const filteredEvents = allEvents.filter(event => 
        event.title.toLowerCase().includes(value)||event.category.toLowerCase().includes(value)
      )
    renderEvents(filteredEvents)
    }

function toggleNotes(id){
    const notesDiv = document.getElementById(`notes-${id}`)
    if(notesDiv.style.display === "block"){
        notesDiv.style.display = "none"
    }
    else{
        notesDiv.style.display = "block"
    }

}

function logout(){
    localStorage.removeItem("token")
    window.location.href = "auth.html"
}

window.onload = loadEvents

