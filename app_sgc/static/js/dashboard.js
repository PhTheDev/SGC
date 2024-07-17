setTimeout(function() {
    var messages = document.querySelectorAll('.messages .alert');
    messages.forEach(function(message) {
        message.style.display = 'none';
    });
  }, 10000);