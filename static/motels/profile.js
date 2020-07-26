
function getForm() {
    fetch(`edit_profile`,
    {
        method: 'POST'
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
    let btn = document.querySelector("#profile-edit-Btn");
    let span = document.getElementsByClassName("close")[0];
    btn.onclick = function() {
        modal.style.display = "block";
        
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


