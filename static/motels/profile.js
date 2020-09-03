function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');
function getForm() {
    fetch(`../api/edit_profile`,
    {
        method: 'POST',
        credentials: "same-origin",
        headers: { 
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken  
        },

        Content_Type: "application/json"
        
    })
    .then(response => response.json())
    .then(data => {
          
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
    fetch(`api/save_profile`,
    {
        method: 'POST',
        credentials: "same-origin",
        headers: { 
            "X-CSRFToken": csrftoken  
        },
        body: data,
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('.full-name').innerHTML = data.last_name + " " + data.first_name;
        document.querySelectorAll('.post-pre-full-name').forEach(a => {
            a.innerHTML = data.first_name + " " + data.last_name;
        })
    })
    .catch((error) => {
        console.log(error);
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

function showSection(section) {
    fetch(`/${myJavaScriptVariable}/post/${section}/`)
    .then(response => response.json())
    .then(data => {
        document.querySelector('.index-all-post').innerHTML = '';
        data.forEach(add_post);
    });
}

function add_post(x) {
    const post = document.createElement('div');
    post.className = 'profile-post-pre box py-0 mb-4 shadow-sm p-4';
    post.dataset.post_id = `${x.post_id}`;
    post.innerHTML = ` 
    <div class="d-flex bd-highlight"> 
        <a class="pre-post-link-ava bd-highlight" href="../${x.user_link}">
            <img class="profile-post-pre-avatar" src="${x.user_avatar}" alt="Ảnh đại diện"> 
        </a>
        <a class="pre-post-link-pro post-pre-full-name mx-1 align-self-center bd-highlight " href="../${x.user_link}"> ${x.full_name}</a>
        <a class="update-time bd-highlight align-self-center" href="../${x.user_link}/posts/${x.post_link}"> &#8226; <span>${x.category}</span> &#8226; ${x.update_time}</a>
        <span class="ml-1  bd-highlight align-self-center far_save_button"></span>

    </div>
    <div class="row mt-3">
        <div class="col-md-2">
            <a href="../${x.user_link}/posts/${x.post_link}"><img class="img-fluid profile-post-pre-image" src="${x.post_image}" alt="Ảnh bài đăng"></a>
            
        </div>
        <div class="col-md-7 pr-0 d-flex align-items-start flex-column bd-highlight">
            <div><a href="../${x.user_link}/posts/${x.post_link}" class="text-capitalize bd-highlight">${x.title}</a></div>
            <div class='pre-post-description mt-2'><span>${x.description}</span></div>
            <div class="pre-post-address bd-highlight mt-auto"><i class="fas fa-map-marked-alt"></i> ${x.address}</div>
        </div>
        <div class="col-md-3 p-0">
            <div class="rent-center"><p>${x.rent} <samp>đ/tháng</samp></p></div>
        </div>
    </div>`;

    document.querySelector(".index-all-post").appendChild(post);
    if(x.poster_id != myJavaScriptVariable || myJavaScriptVariable === '') {
        let bookmark = document.createElement('i');
        if (x.is_active === true) {
            bookmark.className = 'fas fa-bookmark';
        }
        else {
            bookmark.className = 'far fa-bookmark';
        }

        bookmark.dataset.post_id = `${x.post_id}`;
        document.querySelector(`[data-post_id='${x.post_id}'] .far_save_button`).appendChild(bookmark);
    }
    if(x.poster_id == myJavaScriptVariable && myJavaScriptVariable != '') {

    }
    if(x.poster_id == myJavaScriptVariable && myJavaScriptVariable != '') {
        let bookmark = document.createElement('span');
        if (x.status == 1) {
            bookmark.innerText = 'Đang chờ duyệt';
        }
        else if (x.status == 2 || x.status == 7)  {
            bookmark.innerText = 'Đang hoạt động';
        }
        else if (x.status == 3)  {
            bookmark.innerText = 'Không được duyệt';
        }
        bookmark.dataset.post_id = `${x.post_id}`;
        document.querySelector(`[data-post_id='${x.post_id}'] .far_save_button`).appendChild(bookmark);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector("#profile-edit-modal") != null) {
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
            saveForm(data);
        }
    }
    document.querySelector('.profile-horizontal-menu [data-section="active"]').className = 'active';
    document.querySelectorAll('.profile-horizontal-menu li').forEach(li => {
        li.onclick = function() {
            const section = this.dataset.section;
            document.querySelectorAll('.profile-horizontal-menu li').forEach(item => {
                item.className = ''
            });
            li.className = 'active';
            showSection(section);
        }
    })
    document.querySelectorAll('.hide-post-button').forEach(button => {
        button.addEventListener('click', event => {

            event.target.parentElement.parentElement.parentElement.style.display = 'none';
        })
    })
    
})   
