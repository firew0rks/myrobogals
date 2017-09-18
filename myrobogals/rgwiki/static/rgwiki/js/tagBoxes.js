// https://stackoverflow.com/questions/14083272/how-to-make-a-tags-box-using-jquery-with-text-input-field-tags-separated-by
$(function(){ // DOM ready

  // ::: TAGS BOX

  $("#id_tags").on({
    focusout : function() {
      var txt= this.value.replace(/[^a-z0-9]/ig,''); // allowed characters
      if(txt) {
          var span = document.createElement("span");
          var parNode = document.getElementById("tags");
          span.textContent = txt.toLowerCase();
          parNode.appendChild(span);
      }
      this.value="";
    },
    keyup : function(ev) {
      // if: comma|enter (delimit more keyCodes with | pipe)
      if(/(^9$|188|32)/.test(ev.which)) $(this).focusout();
    }
  });
  $('#tags').on('click', 'span', function() {
      $(this).remove();
  });


// https://stackoverflow.com/questions/3142990/jquery-replace-inputs-with-spans
  $("#save-form").click(function() {
      $("#create-form").find("#tags span").each(function() {
          $(this).replaceWith("<input type=hidden name=\"n_" + this.textContent + "\" value=\"" + this.textContent + "\" />");
      })
  })
});