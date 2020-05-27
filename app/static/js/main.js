$(document).ready(function () {

    // index page
    new WOW().init();

    $('.search-icon').click(function () {
        $('.search-box').slideToggle(400);
    });

    $('.toggler-bars').click(function () {
        $('.whole').hide();
        $('.whole_about').hide();
        $('header').hide();
        $('.whole_contact').hide();
        $('#menu-toggle').show('slow');

    });

    $('.toggler-times').click(function () {
        $('.whole').show();
        $('.whole_about').show();
        $('header').show();
        $('.whole_contact').show();
        $('#menu-toggle').hide('slow');
    });

    //Go Top Button
    goTop();

    // Navbar Sticky Button
    navbarSticky();

    //Go Top Button
    $(window).on('scroll', function () {
        goTop();
    });

    // Navbar Sticky Button
    $(window).on('scroll', function () {
        navbarSticky();
    });

    //Go Top Button
    function goTop() {
        if ($(window).scrollTop()) {
            $(".special-button").slideDown(700)
        }
        else {
            $(".special-button").slideUp(700)
        }
    }

    // Navbar Sticky Button
    function navbarSticky() {
        if ($(window).scrollTop()) {
            $(".header-content").addClass("fixed-top");
        }
        else {
            $(".header-content").removeClass("fixed-top");
        }
    }

    $('.owl-carousel').owlCarousel({
        rtl: true,
        autoplay: true,
        autoplayTimeout: 2500,
        autoplayHoverPause: true,
        loop: true,
        margin: 10,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 4
            }
        }
    });

    // hide menu on scroll
    var prevScrollpos = window.pageYOffset;
    window.onscroll = function () {
        var currentScrollPos = window.pageYOffset;
        if (prevScrollpos > currentScrollPos) {
            document.getElementById("header-content").style.top = "0";
        } else {
            document.getElementById("header-content").style.top = "-100px";
        }
        prevScrollpos = currentScrollPos;
    }



    // about us page 
    $('.fixed-menu-bar').click(function () {
        $('.fixed-menu-bar-open').toggle(300);
    });

    $('[data-toggle="popover"]').popover();
    $('[data-toggle="tooltip"]').tooltip();

    // pagination active class set
    const currentlocation = location.href;
    const items = document.querySelectorAll('#pagination a');
    const menulength = items.length
    for (let i = 0; i<menulength; i++){
        if (items[i].href === currentlocation){
            items[i].className = "active"
        }
    }

});

