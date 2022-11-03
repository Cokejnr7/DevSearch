// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
// hljs.highlightAll();
// });



document.addEventListener('click', closeAlertMessages);

let errorMessages = document.querySelector('.change');


function closeAlertMessages(e) {
    if (e.target.className === 'alert__close') {
        e.target.parentElement.style.display = "none";
    }
}

// document.addEventListener('keypress', inputPattern)
// let checker = document.querySelectorAll('.username')
// let checkerList = Array.from(checker)
// function inputPattern(e) {
//     let input = e.target

//     if (input.classList.contains('searchinput')) {

//         let query = e.target.value;

//         checkerList.forEach(function (entry) {
//             let word = entry.textContent
//             if (word.indexOf(query) !== -1) {
//                 console.log(word)
//             }
//         })


//     }

// }