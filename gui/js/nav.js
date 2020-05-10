function toggleNav(called_on_page_init=false) {
    // Get navbar state from localStorage
    let navbar_status = localStorage.getItem("navbar");

    if(called_on_page_init == false) {
        // Toggle navbar behaviour
        // due to navMenuIcon onclick event
        if(navbar_status == "closed") {
            open_nav();
        } else {
            close_nav();
        }
    } else {
        // Page init check
        // Only requires check of localstorage navbar state to ensure correct style on page load
        // Maintains navbar persistence
        if(navbar_status == "closed") {
            close_nav();
        } else {
            open_nav();
        }
    }

    return 0;
}

function open_nav() {
    // Open navbar
    let nav = document.getElementById("nav");
    let nav_a = nav.querySelectorAll(".navItems a");
    let nav_p = nav.querySelectorAll(".navItems a p");

    // Left mainContainer inset
    let mainContainer = document.getElementsByClassName("mainContainer");
    mainContainer[0].style.left = "7%";

    nav.style.width = "180px";

    for(let index = 0; index < nav_a.length; index++) {
        nav_a[index].style.width = "180px";

        nav_p[index].className = "displayed";
    }

    // Set new localstorage navbar state data
    localStorage.setItem("navbar", "open");

    return 0;
}

function close_nav() {
    // Close navbar
    let nav = document.getElementById("nav");
    let nav_a = nav.querySelectorAll(".navItems a");
    let nav_p = nav.querySelectorAll(".navItems a p");

    // Left mainContainer inset
    let mainContainer = document.getElementsByClassName("mainContainer");
    mainContainer[0].style.left = "2%";

    nav.style.width = "50px";

    for(let index = 0; index < nav_a.length; index++) {
        nav_a[index].style.width = "50px";

        nav_p[index].className = "hidden";
    }

    // Set new localstorage navbar state data
    localStorage.setItem("navbar", "closed");

    return 0;
}