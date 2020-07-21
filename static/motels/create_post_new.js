function getDistrict(province_id) {
    fetch(`/get_district/${province_id}`)
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        console.log(typeof(data));

        // console.log(data.data);
        data.forEach(addOption);
    })
    .catch((error) => {
        console.error('Error:', error);
        
    });
}
function addOption(item) {
    const option = document.createElement('option');
    option.value = item.pk;
    option.innerHTML = item.fields.name;
    document.querySelector('#district').appendChild(option);
}

document.addEventListener('DOMContentLoaded', () => {
    var title = document.querySelector('#create_post_title');
    const max = 110;
    let now = title.value.length;
    let suffix = document.querySelector('.form-suffix');
    suffix.innerHTML = `${now}/${max}`;
    const category = document.querySelector('.create_post_category').value;
    switch (category) {
        case '0':
            document.querySelector('.create_post_category_p').innerHTML = 'Tìm người ở ghép';
            break;
        case '1':
            document.querySelector('.create_post_category_p').innerHTML = 'Cho thuê phòng trọ';
            break;
        case '2':
            document.querySelector('.create_post_category_p').innerHTML = 'Cho thuê nhà nguyên căn';
            break;
        case '3':
            document.querySelector('.create_post_category_p').innerHTML = 'Cho thuê nguyên căn chung cư';
            break;

    };
    document.querySelector('#create_post_title').addEventListener('input', () => {
        now = title.value.length;
        suffix.innerHTML = `${now}/${max}`;
        if (now >= 110) {
            suffix.style.color = 'red';
            let x = title.value.substr(0, 109);
            title.value = x;
        }
        else {
            suffix.style.color = '#495057';
        }
    });
    
    document.querySelector('#province').onchange = function() {
        getDistrict(this.value);
    };
});

