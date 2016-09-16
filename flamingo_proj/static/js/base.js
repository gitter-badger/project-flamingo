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
});


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
            $("#like_count" + postId).load(location.href + " #like_count" + postId, function() {
                $(this).children(':first').unwrap();
            });
      });
}


function post_delete(el, postId) {
    if (confirm('Are you sure you want to delete this post?')){
        jQuery.ajax({
            type:"POST",
            url:'/posts/' + postId + '/delete/'
        }).done(function(result){
                var toDelete = $("#post" + postId);
                toDelete.remove();
                console.log("You deleted this post: " + toDelete);
        });
    }
}


function submit_post(){
    jQuery.ajax({
        type: "POST",
        url: "/posts/create/",
        data: $('#content').serialize()
    }).done(function(result){
        var $new_post = $("<div>", {class: "post", id: "post" + result.postId});
        $("#posts").prepend($new_post);
        $new_post.load(location.href + " #post" + result.postId, function() {
                $(this).children(':first').unwrap();
            });
        console.log($new_post);
    });
}


function auto_refresh() {
    setTimeout( function () {
        $('#posts').fadeOut('slow').load(location.href + " #posts").fadeIn('slow');
        refresh();
    }, 8000);
}