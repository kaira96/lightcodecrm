//    let courseSelect = document.getElementById('id_course');
//    let teacherSelect = document.getElementById('id_teacher');
//
//    courseSelect.addEventListener('change', e => {
//        for (var i=0; i<teacherSelect.length; i++) {
//            let courses = teacherSelect.options[i].getAttribute('data-courses')
//            if (courses) {
//                if (!courses.includes(e.target.options[e.target.selectedIndex].text)) {
//                    teacherSelect.options[i].style.display = 'none'
//                }
//                else {
//                    teacherSelect.options[i].style.display = 'block'
//                }
//            }
//    }
//    }
//    );
//
//
//    let teacherSelect = document.getElementById('id_teacher');
//    let studying_timeSelect = document.getElementById('id_studying_time');
//
//    teacherSelect.addEventListener('change', e => {
//        for (var i=0; i<studying_timeSelect.length; i++) {
//            let teacher = studying_timeSelect.options[i].getAttribute('data-studying_time')
//            if (teacher) {
//                if (!teacher.includes(e.target.options[e.target.selectedIndex].text)) {
//                    studying_timeSelect.options[i].style.display = 'none'
//                }
//                else {
//                    studying_timeSelect.options[i].style.display = 'block'
//                }
//            }
//    }
//    }
//    );
//



let courseSelect = document.getElementById('id_course');
let teacherSelect = document.getElementById('id_teacher');
let studying_timeSelect = document.getElementById('id_studying_time');
let formatSelect = document.getElementById('id_format');

courseSelect.addEventListener('change', e => {
    for (var i=0; i<teacherSelect.length; i++) {
        let courses = teacherSelect.options[i].getAttribute('data-courses')
        if (courses) {
            if (!courses.includes(e.target.options[e.target.selectedIndex].text)) {
                teacherSelect.options[i].style.display = 'none'
            }
            else {
                teacherSelect.options[i].style.display = 'block'
            }
        }
    }
});


teacherSelect.addEventListener('change', e => {
    for (var i=0; i<studying_timeSelect.length; i++) {
        let studying_times = e.target.options[e.target.selectedIndex].getAttribute('data-studying_time')
        if (studying_times.includes(studying_timeSelect.options[i].text)) {
            studying_timeSelect.options[i].style.display = 'block'
        }
        else {
            studying_timeSelect.options[i].style.display = 'none'
        }
    }
});


teacherSelect.addEventListener('change', e => {
    for (var i=0; i<formatSelect.length; i++) {
        let formats = e.target.options[e.target.selectedIndex].getAttribute('data-format')
        if (formats.includes(formatSelect.options[i].text)) {
            formatSelect.options[i].style.display = 'block'
        }
        else {
            formatSelect.options[i].style.display = 'none'
        }
    }
});


