const API ="http://127.0.0.1:8000"
async function signup(){
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    const response = await fetch(
        `${API}/signup`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username,
                password
            })
        }
    )
    const data = await response.json()
    
    if(!response.ok){
        alert(data.detail)
        return
    } 
      alert(data.message)
}

async function login(){
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    const response = await fetch(
        `${API}/login`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                username,
                password
            })
        }
    )
    const data = await response.json()
    if(data.access_token){
        localStorage.setItem("token",data.access_token)
        window.location.href="dashboard.html"
    }
    else{
        alert(data.message)
    }

}