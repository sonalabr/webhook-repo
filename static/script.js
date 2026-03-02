function loadEvents(){

fetch("/events")
.then(res => res.json())
.then(data => {

let list = document.getElementById("events")
list.innerHTML = ""

data.forEach(e => {

let text = ""

if(e.action === "push"){
text = `${e.author} pushed to ${e.to_branch}`
}

if(e.action === "pull_request"){
text = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch}`
}

if(e.action==="merge"){

text=`${e.author} merged branch ${e.from_branch} to ${e.to_branch}`

}

let li = document.createElement("li")
li.innerText = text

list.appendChild(li)

})

})

}

loadEvents()

setInterval(loadEvents,15000)
