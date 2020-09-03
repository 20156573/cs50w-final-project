function getDistrict(province_id) {
    fetch(`../api/get_district/${province_id}`)
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        document.querySelector('#district').length='';
        document.querySelector('#commune').length='';
        
        let d_child = document.createElement('option');
        d_child.value='';
        d_child.innerHTML='Quận, huyện';
        d_child.style.display = 'none';
        document.querySelector('#district').appendChild(d_child);

        let c_child = document.createElement('option');
        c_child.value='';
        c_child.innerHTML='Phường, xã';
        c_child.style.display = 'none';
        document.querySelector('#commune').appendChild(c_child);

        data.forEach(addDistrictOption);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

function getCommune(district_id) {
    fetch(`../api/get_commune/${district_id}`)
    .then(response => response.json())
    .then(data => {
        data = JSON.parse(data);
        document.querySelector('#commune').length='';

        let c_child = document.createElement('option');
        c_child.value='';
        c_child.innerHTML='Phường, xã';
        c_child.style.display = 'none';
        document.querySelector('#commune').appendChild(c_child);

        data.forEach(addCommuneOption);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};

function addDistrictOption(item) {
    const option = document.createElement('option');
    option.value = item.pk;
    option.innerHTML = item.fields.name;
    document.querySelector('#district').appendChild(option);
};

function addCommuneOption(item) {
    const option = document.createElement('option');
    option.value = item.pk;
    option.innerHTML = item.fields.name;
    document.querySelector('#commune').appendChild(option);
    
}
var borderColor = '#bdc3c7';
var title = document.querySelector('#create_post_title');
var p_address, d_address, c_address, detailed_address, address;
const category = document.querySelector('.create_post_category').value;
var area = document.querySelector('#create_post_area').value;
var description = document.querySelector('#post_description').value;
var arrayGenderRenter = Array.from(document.getElementsByName('renters_gender'));
var checkGenderRenter = arrayGenderRenter.some(e => e.checked);
// Nhà nguyên căn và chung cư
if (document.querySelector('#create-post-number_of_bedrooms')) {
    var number_of_bedrooms = document.querySelector('#create-post-number_of_bedrooms').value;
    var number_of_toilets = document.querySelector('#create-post-number_of_toilets').value;
}
// Nhà nguyên căn
if (document.querySelector('#total_floor')) {
    var total_floor = document.querySelector('#total_floor').value;
}
// Cho thuê phòng trọ
// if (document.querySelector('#create-post-number_of_rooms')) {
//     var number_of_rooms = document.querySelector('#number_of_rooms').value;
//     var max_rent = document.querySelector('#create_post_max_rent').value;
// }
// Tìm bạn ở ghép
if (document.querySelector('#create-post-number_of_roommate')) {
    var number_of_roommate = document.querySelector('#create-post-number_of_roommate').value;
}

document.addEventListener('DOMContentLoaded', () => {
    const max = 110;
    let now = title.value.length;
    let suffix = document.querySelector('.form-suffix');
    suffix.innerHTML = `${now}/${max}`;
    const category = document.querySelector('.create_post_category').value;
    // checkFrom();
    switch (category) {
        case '4':
            document.querySelector('.create_post_category_p').innerHTML = 'Tìm người ở ghép';
            document.querySelector('.classified-info').innerHTML = `<div class="row">
                <label class="col-sm-4 label-radio" for="">* Bạn đang tìm</label>
                <input class="col-sm-6" type="number" min="1"  required id="create-post-number_of_roommate" name="number_of_roommate" placeholder="VD: 2">
                <label class="col-sm-2 label-radio pl-4" for="">người</label>
            </div>`;
            break;
        case '1':
            document.querySelector('.create_post_category_p').innerHTML = 'Cho thuê phòng trọ';
            document.querySelector('.classified-info').innerHTML = `<div class="row">
                <label class="col-sm-3 label-radio" for="">Bạn cho thuê</label>
                <input class="col-sm-6" type="number" id="create-post-number_of_rooms" name="number_of_rooms" placeholder="VD: 2">
                <label class="col-sm-3 label-radio pl-4" for="">phòng</label>
            </div>`;
            document.querySelector('.create_post_max_rent').innerHTML = `<div class="row">
                <label class="col-md-4">Giao động tới</label>
                <div class="col-md-8">
                    <input id="create_post_max_rent" name='max_rent' type="number" placeholder="VD: 2.500.000">
                </div>
            </div>`;
            break;
        case '2':
            document.querySelector('.create_post_category_p').innerHTML = 'Cho thuê nhà nguyên căn';
            document.querySelector('.classified-info').innerHTML = `<div class="row mb-4">
                <label class="col-sm-4 label-radio">* Số phòng ngủ</label>
                <input type="number" class="col-sm-6" required name="number_of_bedrooms" min='1' id="create-post-number_of_bedrooms" placeholder="VD: 1">
                <label class="col-sm-2 label-radio" ></label>
            </div>
            
            <div class="row mb-4">
                <label class="col-sm-4 label-radio" for="">* Số phòng vệ sinh</label>
                <input type="number" class="col-sm-6" required name="number_of_toilets" min='1' id="create-post-number_of_toilets" placeholder="VD: 1">
                <label class="col-sm-2 label-radio" for=""></label>
            </div>

            <div class="row">
                <label class="col-sm-4 label-radio" for="">* Tổng số tầng</label>
                <input type="number" class="col-sm-6" required name="total_floor" min='1' id="total_floor" placeholder="VD: 1">
                <label class="col-sm-2 label-radio" for=""></label>
            </div>`;
            break;
        case '3':
            document.querySelector('.create_post_category_p').innerHTML = 'Cho thuê nguyên căn chung cư';
            document.querySelector('.classified-info').innerHTML =`<div class="row mb-4">
                <label class="col-sm-4 label-radio">* Số phòng ngủ</label>
                <input type="number" class="col-sm-6" required name="number_of_bedrooms" min='1' id="create-post-number_of_bedrooms" placeholder="VD: 1">
                <label class="col-sm-2 label-radio" ></label>
            </div>
            
            <div class="row mb-4">
                <label class="col-sm-4 label-radio" for="">* Số phòng vệ sinh</label>
                <input type="number" class="col-sm-6" required name="number_of_toilets" min='1' id="create-post-number_of_toilets" placeholder="VD: 1">
                <label class="col-sm-2 label-radio" for=""></label>
            </div>`;
            break;

    };
    // Tiêu đề
    document.querySelector('#create_post_title').addEventListener('input', () => {
        now = title.value.length;
        suffix.innerHTML = `${now}/${max}`;
        if (now >= 110) {
            suffix.style.color = 'red';
            let x = title.value.substr(0, 109);
            title.value = x;
        }
        else {
            // checkFrom();
            suffix.style.color = '#495057';
        }
    });
    
    document.querySelector('#province').onchange = function() {
        getDistrict(this.value);

        p_address = `${this.options[this.selectedIndex].innerHTML}`;
        
        address = p_address;
        document.querySelector('.detailed_address').value = '';
        document.querySelector('.address').style.visibility = 'visible';
        document.querySelector('.address').innerHTML = address;
    };
    
    document.querySelector('#district').onchange = function() {
        getCommune(this.value);
        
        d_address = this.options[this.selectedIndex].innerHTML;
        address = `${d_address}, ${p_address}`;
        document.querySelector('.address').innerHTML = address;
        document.querySelector('.detailed_address').value = '';
    };

    document.querySelector('#commune').onchange = function() {
        c_address = this.options[this.selectedIndex].innerHTML;
        address = `${c_address}, ${d_address}, ${p_address}`;
        document.querySelector('.address').innerHTML = address;
        document.querySelector('.detailed_address').value = '';
    };
    
    document.querySelector('.detailed_address').addEventListener('input', function() {
        if (document.querySelector('#commune').value === '') {
            this.value = '';
        }
        else {
            detailed_address = this.value;
            if (this.value != '') {
                address = `${detailed_address}, ${c_address}, ${d_address}, ${p_address}`;
                // checkFrom();
            }
            else {
                address = `${c_address}, ${d_address}, ${p_address}`;
            }
            document.querySelector('.address').innerHTML = address;
        
            
        }
        
    });


    var image = [];
    document.querySelector('#post-image-input').onchange = function(event) {
        if (this.files && this.files[0]) {
            document.querySelector('.post-image small').hidden = true;
            for (var i = 0; i < this.files.length; i++){

                let index = image.length;
                let reader = new FileReader();

                reader.onload = function (e) {
                    let div_img = document.createElement('div');
                    div_img.innerHTML = `<img src="${e.target.result}" alt=""><span data-index="${index}" class='hide-img'>x</span>`;
                    document.querySelector('.img_view').appendChild(div_img);
                };
                image.push(this.files[i]);
                reader.readAsDataURL(this.files[i]);
            }

            
            console.log(this.files);
        }
        console.log(image);
    }
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'hide-img') {
            console.log(element.dataset.index);
            image[element.dataset.index] = '';
            console.log(image);
            element.parentElement.remove();
        }
        if (element.id ==='button_post') {
            var images = [];
            for (var i = 0; i < image.length; i++) {
                if (image[i] != '') {
                    images.push(image[i]);
                }
            }
            let list = new DataTransfer();
            for (var i=0; i<images.length; i++){
                let file = images[i];
                list.items.add(file);
            }

            let myFileList = list.files;
            document.querySelector('#post-image-input').files = myFileList;
            
            if (myFileList.length === 0) {
                document.querySelector('.post-image small').innerHTML = "vui lòng chọn ít nhất một ảnh.";
                document.querySelector('.post-image small').hidden = false;
            }

        }
    });
})