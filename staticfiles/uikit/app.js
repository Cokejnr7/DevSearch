// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
// hljs.highlightAll();
// });



document.addEventListener('click', closeAlertMessages);

let errorMessages = document.querySelector('.change');

function closeAlertMessages(e) {
    if (e.target.className === 'alert__close') {
        errorMessages.style.display = "none";
    }
}
