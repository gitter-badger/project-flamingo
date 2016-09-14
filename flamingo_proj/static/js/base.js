$(function () {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
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
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $.each($('.like-button'), function (index, value) {
        console.log(index + ": " + value.getAttribute("post-id") );
        set_like_lables(value, value.getAttribute("post-id"));
    });

});


function set_like_lables(el, postId) {
    console.log("SET METHOD")
    jQuery.getJSON('/posts/' + postId + '/like/', function(result){
            console.log(result)
            if (result.liked_by_user){
                el.value = "Dislike";
            } else {
                el.value = "Like";
            }
      });
}

function like_dislike(el, postId) {
       jQuery.ajax({
            type:"POST", //post data
            url:'/posts/' + postId + '/like/' // your url that u write in action in form tag
      }).done(function(result){
            if (result.liked_by_user){
                el.value = "Dislike";
                console.log("Likes: " + result.liked_by_user)
            } else {
                el.value = "Like";
                console.log("Likes: " + result.liked_by_user)
            }
      });
}
