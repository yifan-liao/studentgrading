﻿// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function getAllCourse() {
    var ret;
    $.ajax({
       url: 'getcourse',
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function getCourse(id) {
    var ret;
    $.ajax({
       url: 'getcourse?id=' + id,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function getAllGroup(course_id) {
    var ret;
    $.ajax({
       url: 'getgroup?course_id=' + course_id,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function getGroup(course_id, group_id) {
    var ret;
    $.ajax({
       url: 'getgroup?course_id=' + course_id + '&group_id=' + group_id,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function getMyGroup(course_id) {
    var ret;
    $.ajax({
       url: 'getgroup?course_id=' + course_id,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function newCourse(data) {
    var ret;
    $.ajax({
       url: 'newcourse/',
       type: 'POST',
       data: data,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function delCourse(data) {
    var ret;
    $.ajax({
       url: 'delcourse/',
       type: 'POST',
       data: data,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}

function getCandidateStudent(course_id) {
    var ret;
    $.ajax({
       url: 'getcandidatestudent?course_id=' + course_id,
       async: false,
       success: function(data) {
           console.log(data);
           ret = data;
       },
       fail: function(data) {
           console.log(data);
       }
    });
    return ret;
}