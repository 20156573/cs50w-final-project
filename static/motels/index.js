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

let counter = 0;
const quantity = 3;



document.addEventListener('DOMContentLoaded', () => {
    var q = document.querySelector('.search-container input').value;

    var cg = document.getElementById('select_category').value;
        
    var lt = document.getElementById('select_location').value;

    var gd = document.getElementById('select_gender').value;

    var mn = document.getElementById('select_money').value;
    load(q, cg, lt, gd, mn);
    
    document.querySelectorAll('.filter-time').forEach(item => {
        item.addEventListener('change', event => {
            q = document.querySelector('.search-container input').value;
            counter = 0;
            getParam();
        })
    })
    document.querySelector('.search-container input').addEventListener('change', event => {
        q = event.target.value;
        counter = 0;
        getParam();
    })
    document.querySelector('.search-container button').addEventListener('click', () => {
        q = document.querySelector('.search-container input').value;
        counter = 0;
        getParam();
    })

    window.onscroll = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
            cg = document.getElementById('select_category').value;
        
            lt = document.getElementById('select_location').value;

            gd = document.getElementById('select_gender').value;

            mn = document.getElementById('select_money').value;
            load(q, cg, lt, gd, mn);
        }
    };
    function getParam() {
        cg = document.getElementById('select_category').value;
        
        lt = document.getElementById('select_location').value;

        gd = document.getElementById('select_gender').value;

        mn = document.getElementById('select_money').value;
        document.querySelector(".index-all-post").innerHTML = '';
        load(q, cg, lt, gd, mn);
    }
});

function load(q, cg, lt, gd, mn){
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    console.log('one');
    console.log(start);
    console.log(end);

    fetch(`api/get_index?start=${start}&end=${end}&q=${q}&cg=${cg}&lt=${lt}&gd=${gd}&mn=${mn}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(add_post);
        document.querySelectorAll('.fa-bookmark').forEach(changeColor);
    })
};

function changeColor(item, index){
    item.addEventListener('click', event => {
        const element = event.target;
        save(item.dataset.post_id, element);   
    })
}

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

        if (data.is_active === true) {
            console.log(data.avatar);
            element.className = 'fas fa-bookmark';
            let list = document.querySelector('.list_following');
            let title = document.createElement('div');
            title.dataset.post_id = id;
            title.className= 'mb-2';
            title.innerHTML = `<a href="../${data.full_name_link}"><img class="profile-post-pre-avatar" src="${data.avatar}" alt="Ảnh đại diện"></a>
            <a href="../${data.full_name_link}/posts/${data.title_link}"><span>${data.title}</span></a>`;
            list.insertBefore(title, list.childNodes[0]);
        }
        else {
            document.querySelector(`.list_following [data-post_id="${id}"]`).style.animationPlayState = 'running';

            document.querySelector(`.list_following [data-post_id="${id}"]`).addEventListener('animationend', () => {
                document.querySelector(`.list_following [data-post_id="${id}"]`).remove();
            });
            element.className = 'far fa-bookmark';
        }
    })
    .catch((error) => {
        console.error('Error:', error.error);
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
}
