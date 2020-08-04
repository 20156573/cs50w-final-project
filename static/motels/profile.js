// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// let csrftoken = getCookie('csrftoken');
function getForm() {
    fetch(`../edit_profile`,
    {
        method: 'POST'
        // credentials: "same-origin",
        // headers: { 
        //     'Accept': 'application/json, text/plain, */*',
        //     'Content-Type': 'application/json',
        //     "X-CSRFToken": csrftoken  
        // }

        // Content-Type: "application/json"
        
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
          
        let y = data.all_address.map(add_address);
        document.querySelector('#first_name').value = data.first_name;
        document.querySelector('#last_name').value = data.last_name;
        document.querySelector(`#option${data.user_address}`).selected = "true";
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function saveForm(data) {
    fetch(`save_profile`,
    {
        method: 'POST',
        body: data,
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.full-name').innerHTML = data.last_name + " " + data.first_name;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function add_address(data){
    const option = document.createElement('option');
    option.className = 'motal-form-option';
    option.value = data.id;
    option.id = "option" + data.id;
    option.innerHTML = data.name;
    document.querySelector('#user_address').append(option);
}
document.addEventListener('DOMContentLoaded', () => {
    let modal = document.querySelector("#profile-edit-modal");
    let span = document.getElementsByClassName("close")[0];
    if (document.querySelector("#profile-edit-Btn")) {
        let btn = document.querySelector("#profile-edit-Btn");
        btn.onclick = function() {
            modal.style.display = "block";
            
        }
    }
    

    span.onclick = () => {
        modal.style.display = "none";
    }
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    getForm();
    
    document.querySelector('#editProBtn').onclick = () => {
        const data = new FormData(document.querySelector('#editProForm'));
        console.log(data);
        saveForm(data);
    }
    
})   
