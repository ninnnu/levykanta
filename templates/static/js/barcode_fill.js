$(document).ready(function() {
    $("#id_barcode").focus();
    $("#id_returncode").focus();
    disable_entertab = true;
    old_barcode = 0;
    went_DIY = false;
    $("#id_barcode").autocomplete({
        source: function(request, response) {
            $.post("/discdb/suggest/", {'input': request.term}, function(data) {
                response(data);
            }, 'json');
        },
        select: function(ev, ui) {
            if(ui.item.value == "0") { // DIY
                $("#id_artist").removeAttr("readonly");
                $("#id_name").removeAttr("readonly");
                setTimeout(function() {$("#id_barcode").val(old_barcode); }, 10);
                went_DIY = true;
            }
            else {
                  if(went_DIY == true) {
                      setTimeout(function() {$("#id_barcode").val(old_barcode); }, 10);
                  }
                  $.get("/discdb/lookup/cd/"+ui.item.value+"/", function(data) {
                  console.log(data);
                  $('[name="artist"]').val(data.artist);
                  $('[name="name"]').val(data.title);
                  if(data.barcode.length() > 2) {
                      $("#id_barcode").val(data.barcode);
                  }
                  $.each(data.tracks, function(index, track) {
                      if(data.artist != "Various") {
                          track.artist = data.artist;
                      }
                      $("#tracks").append("<li>"+track.artist+" - "+track.title+"</li>");
                      $.post("/discdb/track/add/", {"artist": track.artist, "name": track.title, "csrfmiddlewaretoken": $('[name="csrfmiddlewaretoken"]').val()}, function(data) {
                             $('[name="track_ids"]').val($('[name="track_ids"]').val()+","+data);
                      }, 'text');
                  });
                }, 'json');
            }
        },
        response: function(ev, ui) {
            disable_entertab = false;
            if(went_DIY == false) {
                old_barcode = $("#id_barcode").val();
            }
        },
    });
    
    $("#id_barcode").focus(function(ev, ui) {
            console.log($("#id_barcode").val());
            if($("#id_barcode").val().length > 0) {
                $("#id_barcode").autocomplete("search", $("#id_barcode").val());
            }
        }
    );
    
    $("#id_returncode").focus(function(ev, ui) {
            console.log($("#id_returncode").val());
            if($("#id_returncode").val().length > 0) {
                $("#id_returncode").autocomplete("search", $("#id_returncode").val());
            }
        }
    );

    $("#id_returncode").autocomplete({
        source: function(request, response) {
            $.post("/discdb/suggest/catalogue/", {'input': request.term}, function(data) {
                response(data);
            }, 'json');
        },
        select: function(ev, ui) {
            if(ui.item.value == 0) { // DIY
                $("#id_returncode").val("");
            }
            else {
                $.get("/discdb/lookup/catalogue/"+ui.item.value+"/", function(data) {
                  console.log(data);
                  $('#artist').text(data.artist);
                  $('#name').text(data.name);
                  $('#owner').text(data.owner);
                  $("#id_returncode").val(data.id);
                }, 'json');
            }
        },
        response: function(ev, ui) {
            disable_entertab = false;
        },
    });
    
    $(document).keypress(function(ev) {
        if (ev.keyCode == 10 || ev.keyCode == 13 || ev.keyCode == 9) { // Enter / tab
            if(disable_entertab == true) {
                ev.preventDefault();
            }
        }
    });
});
