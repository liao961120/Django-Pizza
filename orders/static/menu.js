var csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    var select_type = document.querySelector('#menu-type');
    var menuItemsTitle = document.querySelector('#menu-item-title');
    var menu_items = document.querySelector('#menu-items');

    // Load menu
    ajax_getMenu();
    menuItemsTitle.textContent = select_type.options[select_type.selectedIndex].innerText + ' Menu';

    // Select menu type: Pizza, Subs, ..., etc.
    select_type.onchange = () => {
        ajax_getMenu();
        menuItemsTitle.textContent = select_type.options[select_type.selectedIndex].innerText + ' Menu';
    };


    // Ajax: retrieve menu items based on selected type
    function ajax_getMenu() {
        
        // Prepare data to send to server
        const data = new FormData();
        const menu_type = select_type.options[select_type.selectedIndex].value;
        data.append('menu-type', menu_type);
        data.append('csrfmiddlewaretoken', csrftoken);  // csrf for Ajax

        // Send Ajax request to server
        const request = new XMLHttpRequest();
        request.open('POST', showMenu_url);
        request.send(data);
 
        // Update menu when request completes (recieved data from server) 
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            updateMenuItems(menu_items, data);
        };

        // Stop page from reloading after submit
        return false;
    };
});

function updateMenuItems(menu_items, array) {
    // Clear previous 
    menu_items.innerHTML = '';

    // make new options
    for (var i=0; i<array.length; i++) {
        div = document.createElement('div');
        num = document.createElement('select');
        num.className = 'order-num';
        num.onchange = styleSelected;

        for (var j=0; j<11; j++) {
            op = document.createElement('option');
            op.value = j;
            op.innerText = j;
            num.append(op);
        };
        
        div.className = 'menu-item';
        //input.type = 'checkbox';
        div.dataset.id = array[i].id;
        div.dataset.menuType = array[i].type;

        // displayed menu item info
        div.innerHTML += array[i].item_str;

        // update menu
        div.append(num);
        menu_items.append(div);
    };

    // Add to chart
    btn = document.createElement('button');
    btn.innerText = 'Add to Cart';
    btn.className = 'add-to-cart';
    btn.type = 'button';
    btn.onclick = add2chart;
    menu_items.append(btn)
};


function add2chart() {
    // Find all choosen data
    var toAdd = [];
    document.querySelectorAll('div.menu-item').forEach(ele => {

        var slct = ele.lastElementChild;
        var num = slct.options[slct.selectedIndex].value;

        if (num != '0') {
            var item = {
                'menuType': ele.dataset.menuType,
                'id': ele.dataset.id,
                'num': num
                }
            toAdd.push(item);
            
            // Clean up
            slct.selectedIndex = 0;
            slct.onchange();
        };
    });

    // Return earily if no item selected
    if (toAdd.length == 0) {
        alert("No items selected!")
        return;
    }

    // Add data
    const data = new FormData();
    data.append('csrfmiddlewaretoken', csrftoken);
    data.append('items', JSON.stringify(toAdd));

    // ajax request
    const request = new XMLHttpRequest();
    request.open('POST', add2chart_url);
    request.send(data);

    // After request completes
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (data.success) 
            alert(`Added ${data.itemnum} item(s) to shopping cart!`)
    };

    // prevernt reload
    return false;
};


// Show selected
function styleSelected() {
    if (this.value != '0')
        this.parentElement.classList.add('selected');
    else
        this.parentElement.classList.remove('selected');
};



// Get csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}