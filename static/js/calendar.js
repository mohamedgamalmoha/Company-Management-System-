window.onload = function(){
    var degrees = 180;
    var lst =['calendarnav-next', 'calendarnav-previous'];
    $('.calendarnav-next').each(function (index){
        $(this).css({'transform' : 'rotate('+ degrees +'deg)'});
    });
    $('.calendarnav-previous').each(function (index){
        $(this).css({'transform' : 'rotate('+ degrees +'deg)'});
    });
    console.log('hello');
};
