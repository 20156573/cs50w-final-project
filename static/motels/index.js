document.addEventListener('DOMContentLoaded', () => {
    load();
});

function load(){
    fetch(`api/get_index`)
    .then(response => response.json())
    .then(data => {
        data.forEach(add_post);
    })
};

function add_post(x) {
    const post = document.createElement('div');
    post.className = 'profile-post-pre box mb-4 shadow-sm p-4';
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
    <div class="col-md-7 pr-0">
        <div><a href="../${x.user_link}/posts/${x.post_link}" class="text-capitalize">${x.title}</a></div>
        <div class="mt-2 pre-post-description"><span>${x.description}</span></div>
        <div class="pre-post-address"><span>20</span> lượt theo dõi<i class="ml-4 fas fa-map-marked-alt"></i> ${x.address}</div>
    </div>
    <div class="col-md-3 p-0">
        <div class="rent-center"><p>${x.rent} <samp>đ/tháng</samp></p></div>
    </div>
</div>`;
    document.querySelector(".index-all-post").appendChild(post);

    if(x.poster_id != myJavaScriptVariable || myJavaScriptVariable === '') {
        let bookmark = document.createElement('div');
        bookmark.innerHTML = '<i class="far fa-bookmark"></i>';
        document.querySelector(`[data-post_id='${x.post_id}'] .d-flex`).appendChild(bookmark);
    }
}

// document