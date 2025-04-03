document.addEventListener('DOMContentLoaded', function () {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl)
    })

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    setTimeout(function() {
      var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
      alerts.forEach(function(alert) {
        var alertInstance = new bootstrap.Alert(alert);
        alertInstance.close();
      });
    }, 5000);

    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
      const linkPath = link.getAttribute('href');
      if (linkPath && currentLocation.includes(linkPath) && linkPath !== '/') {
        link.classList.add('active');
      } else if (linkPath === '/' && currentLocation === '/') {
        link.classList.add('active');
      }
    });
  
    var dateRangePickers = document.querySelectorAll('.date-range-picker');
    if (dateRangePickers.length && typeof daterangepicker !== 'undefined') {
      dateRangePickers.forEach(function(picker) {
        $(picker).daterangepicker({
          opens: 'left',
          autoApply: true,
          locale: {
            format: 'MM/DD/YYYY'
          }
        });
      });
    }
  
    var ratingInputs = document.querySelectorAll('.rating-input');
    ratingInputs.forEach(function(input) {
      const stars = input.querySelectorAll('.star');
      stars.forEach(function(star, index) {
        star.addEventListener('click', function() {
          const ratingVal = index + 1;
          const hiddenInput = input.querySelector('input[type="hidden"]');
          hiddenInput.value = ratingVal;
          
          stars.forEach(function(s, i) {
            if (i < ratingVal) {
              s.classList.add('active');
            } else {
              s.classList.remove('active');
            }
          });
        });
      });
    });
  });