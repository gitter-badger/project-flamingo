function like_dislike(el, postId)
{
  if (el.value === "Like") {
        jQuery.ajax({
          type:"POST", //post data
          url:'/posts/' + postId + '/like/' // your url that u write in action in form tag
      }).done(function(result){
           el.value = "Dislike";
      });
  } else {
    el.value = "Like";
    }
}

