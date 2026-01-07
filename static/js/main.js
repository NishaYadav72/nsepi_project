$(document).ready(function() {
    function animateCounter () {
        $('.counter').each(function() {
            var $this = $(this),
            countTo = $this.attr('data-count');
        
            $({ countNum: $this.text()}).animate({
                countNum: countTo
            },
    
            {
    
                duration: 3000,
                easing:'linear',
                step: function() {
                $this.text(Math.floor(this.countNum));
                },
                complete: function() {
                $this.text(this.countNum + "+");
                //alert('finished');
                }
    
            }); 
         });
    } 
        
    function setActiveNav() {
        var path = window.location.pathname;
        $(".nav-link").removeClass("active");
        if(path === "" || path === "/" || path==="/nsdpi/") {
            $(".nav-link.home").addClass("active");
        } else if (path.includes("courses")) {
            $(".nav-link.courses").addClass("active");
        } else if (path.includes("branches")) {
            $(".nav-link.branches").addClass("active");
        } else if (path.includes("about")) {
            $(".nav-link.about").addClass("active");
        } else if (path.includes("student-zone")) {
            $(".nav-link.student-zone").addClass("active");
        } else if (path.includes("contact")) {
            $(".nav-link.contact").addClass("active");
        } else if (path.includes("placements")) {
            $(".nav-link.placements").addClass("active");
        }
    }

    setActiveNav();

    var x = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            entry.isIntersecting && animateCounter()
        })
    });

    x.observe($("#counter-wrap")[0]);
});

function scrollToView(id) {
    $('html, body').animate({
        scrollTop: $(id).offset().top
    }, 1000);
}

function getFormattedDate(date) {
    if(!date?.trim() || date === "0000-00-00") return "-";
    const d = date.split("-");
    if(d.length) {
      return `${d[2]}/${d[1]}/${d[0]}`;
    }
    return "-";
}

function getDurationLabel(duration) {
    if(duration < 12) {
      return duration == 1 ? '1 Month' : duration + ' Months';
    }
    return duration/12 == 1 ? "1 Year" : duration/12 + ' Years';
}