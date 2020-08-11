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

var base_menu_color = 'rgb(75,75,75)';
var border_input_color = 'rgb(189,195,199)';

document.addEventListener('DOMContentLoaded', () => {
    load();
});
function load(){
    fetch(`api/get_index`)
    .then(response => response.json())
    .then(data => {
        data.forEach(add_post);
        document.querySelectorAll('.fa-bookmark').forEach(changeColor);
    })
};

function save(id, element) {
    fetch(`api/follow`,
    {
        method: 'POST', 
        credentials: "same-origin",
        headers: { 
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken  
        },

        Content_Type: "application/json",
        
        body: JSON.stringify({'post_id': id})
    })
    .then(response => response.json())
    .then(data => {

        console.log(data.is_active);
        console.log(data.full_name_link);

        if (data.is_active === true) {
            element.className = 'fas fa-bookmark';
            // let div = document.createElement('div');
            // div.className = 'mb-2';
            // div.dataset.post_id = id;
            // div.innerHTML = `<a href="../${data.full_name_link}"><img class="profile-post-pre-avatar" src="${data.avatar}" alt="Ảnh đại diện"></a>
            // <a href="../${data.full_name_link}/posts/${data.title_link}"><span>${data.title}</span></a>`;
            // let list = document.querySelector('.list_following');
            // list.insertBefore(div, list.childNodes[0]); 

        }
        else {
            document.querySelector(`.list_following [data-post_id="${id}"]`).remove();
            element.className = 'far fa-bookmark';
        }
    })
    .catch((error) => {
        console.error('Error:', error.error);
    });
}

function changeColor(item, index){
    item.addEventListener('click', event => {
        const element = event.target;
        save(item.dataset.post_id, element);   
    })
}

function add_post(x) {
    const post = document.createElement('div');
    post.className = 'profile-post-pre box py-0 mb-4 shadow-sm p-4';
    post.dataset.post_id = `${x.post_id}`;
    post.innerHTML = ` <div class="d-flex"> 
    <div class="mr-auto">
        <a class="pre-post-link-ava" href="../${x.user_link}">
            <img class="profile-post-pre-avatar" src="${x.user_avatar}" alt="Ảnh đại diện"> 
        </a>
        <a class="pre-post-link-pro post-pre-full-name" href="../${x.user_link}"> ${x.full_name}</a>
        <a class="update-time" href="../${x.user_link}/posts/${x.post_link}"> &#8226; <span>${x.category}</span> &#8226; ${x.update_time}</a>
    </div>
</div>
<div class="row mt-3">
    <div class="col-md-2">
        <a href="../${x.user_link}/posts/${x.post_link}"><img class="img-fluid profile-post-pre-image" src="${x.post_image}" alt="Ảnh bài đăng"></a>
        
    </div>
    <div class="col-md-7 pr-0 d-flex align-items-start flex-column bd-highlight">
        <div><a href="../${x.user_link}/posts/${x.post_link}" class="text-capitalize bd-highlight">${x.title}</a></div>
        <div class='pre-post-description'><span>${x.description}</span></div>
        <div class="pre-post-address bd-highlight mt-auto"><span class="far_save_button"></span><i class="fas fa-map-marked-alt"></i> ${x.address}</div>
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
}
