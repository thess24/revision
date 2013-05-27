 // Makes to do list sortable

  // $(function() {
  //   $( "#sortable" ).sortable({
  //     placeholder: "ui-state-highlight"
  //   });
  //   $( "#sortable" ).disableSelection();
  // });


// To do form hide and show

$(function(){
   $('.showtodoform').click(function(){
      $(this).hide();
      $('.hidetodoform').show();
      $('.todoform').show();
      return false;
   });
});

$(function(){
   $('.hidetodoform').click(function(){
      $(this).hide();
      $('.showtodoform').show();
      $('.todoform').hide();
      return false;
   });
});


// Item form hide and show

$(function(){
   $('.showitemform').click(function(){
      $(this).hide();
      $('.hideitemform').show();
      $('.itemform').show();
      return false;
   });
});

$(function(){
   $('.hideitemform').click(function(){
      $(this).hide();
      $('.showitemform').show();
      $('.itemform').hide();
      return false;
   });
});


// Date Picker

$(function(){
	$( "#id_due_date" ).datepicker({gotoCurrent: true});
});


// Show and Hide url and fileitem

$(function(){
   $('.showurl').click(function(){
   	  $(this).hide();
      $('#itemurl').show();
      $('#id_fileitem').val("");
      $('#itemfileitem').hide();       
      $('.hideurl').show();     
      return false;
   });
});

$(function(){
    $('.hideurl').click(function(){
   	  $(this).hide();
      $('#itemurl').hide();
      $('#id_url').val(""); 
      $('#itemfileitem').show();  
      $('.showurl').show(); 
      return false;
   });
});

// Hide subscribe form if subscribed---hidden unsub already taken care of on backend

$(document).ready(function(){
if($("#unsubscribe").length){
     $("#subscribe").hide();
}
});

 

//// Show and Hide comments

//http://papermashup.com/jquery-show-hide-plugin/

(function ($) {
    $.fn.showHide = function (options) {
 
    //default vars for the plugin
        var defaults = {
            speed: 500,
            easing: '',
            changeText: 0,
            showText: 'Show',
            hideText: 'Hide'
 
        };
        var options = $.extend(defaults, options);
 
        $(this).click(function () {
// optionally add the class .toggleDiv to each div you want to automatically close
                      $('.toggleDiv').slideUp(options.speed, options.easing);
             // this var stores which button you've clicked
             var toggleClick = $(this);
             // this reads the rel attribute of the button to determine which div id to toggle
             var toggleDiv = $(this).attr('rel');
             // here we toggle show/hide the correct div at the right speed and using which easing effect
             $(toggleDiv).slideToggle(options.speed, options.easing, function() {
             // this only fires once the animation is completed
             if(options.changeText==1){
             $(toggleDiv).is(":visible") ? toggleClick.text(options.hideText) : toggleClick.text(options.showText);
             }
              });
 
          return false;
 
        });
 
    };
})(jQuery);


$(document).ready(function(){
 
   $('.commentbutton').showHide({
        speed: 600,  // speed you want the toggle to happen
        easing: 'easeOutQuart',  // the animation effect you want. Remove this line if you dont want an effect and if you haven't included jQuery UI
        changeText: 1, // if you dont want the button text to change, set this to 0
        showText: 'View',// the button text to show when a div is closed
        hideText: 'Close' // the button text to show when a div is open
 
    });
 
});

 //http://easings.net/