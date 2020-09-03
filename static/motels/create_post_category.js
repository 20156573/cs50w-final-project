// Xử lý ô input nhập title 
var selected = "rgb(230, 55, 87)";
var unselected = "rgb(75, 75, 75)";
var post_type, title;
// Tạo form
var form = document.createElement('form');
form.action = 'new';
form.method = 'POST';
var title_input = document.createElement('input');
title_input.name = "title";
var type = document.createElement('input');
type.name = "category";
form.appendChild(type);
form.appendChild(title_input);
form.style.visibility = 'hidden';
document.body.appendChild(form);
var max = 110;


document.addEventListener('DOMContentLoaded', function() {
    var title = document.querySelector('#create_post_title');
    let now = title.value.length;
    let suffix = document.querySelector('.form-suffix');
    suffix.innerHTML = `${now}/${max}`;
    
    document.querySelector('#create_post_title').addEventListener('input', () => {
        now = title.value.length;
        suffix.innerHTML = `${now}/${max}`;
        title_input.value = title.value;
        if (now >= max) {
            suffix.style.color = 'red';
            let x = title.value.substr(0, 109);
            title.value = x;
        }
        else {
            suffix.style.color = '#495057';
        }
        checkFrom();
    });
    secondUlHidden();
    const first_list = document.querySelectorAll('.first-ul li');
    const second_list = document.querySelectorAll('.second-ul li');
    first_list.forEach(changeColor);
    second_list.forEach(changeColor);
    checkFrom();

    console.log(`type: ${type.value}`);
    console.log(`title: ${title_input.value}`);

    document.querySelector('#create_post_next').addEventListener('click', () => {
        form.submit();
    })
});

function secondUlHidden() {
    document.querySelectorAll('.second-ul li').forEach(li => {
        li.style.visibility = 'hidden';
        li.style.color = unselected;
    });
};

function secondUlVisible() {
    document.querySelectorAll('.second-ul li').forEach(li => {
        li.style.visibility = 'visible';
    });
};


function changeColor(item, index, arr) {
    item.addEventListener('click', () => {
        arr.forEach(li => {
            li.style.color = unselected;
        })
        item.style.color = selected;
        if (document.querySelector('.type_post_renter').style.color == selected) {
            secondUlVisible();
        }
        else {
            secondUlHidden();
        }
        if (item.dataset.type) {
            post_type = item.dataset.type;
        }
        else {
            post_type = '';
        }
        switch (post_type) {
            case '4':
                document.querySelector('p span').innerHTML = 'Tìm người ở ghép';
                break;
            case '1':
                document.querySelector('p span').innerHTML = 'Cho thuê phòng trọ';
                break;
            case '2':
                document.querySelector('p span').innerHTML = 'Cho thuê nhà nguyên căn';
                break;
            case '3':
                document.querySelector('p span').innerHTML = 'Cho thuê nguyên căn chung cư';
                break;
            default:
                document.querySelector('p span').innerHTML = '';
                break;
            }
        type.value = post_type;
        checkFrom();
})}

function checkFrom() {
    if ((title_input.value != '') && (type.value != '')) {
        document.querySelector('#create_post_next').disabled = false;
    }
    else {
        document.querySelector('#create_post_next').disabled = true;
    }

}