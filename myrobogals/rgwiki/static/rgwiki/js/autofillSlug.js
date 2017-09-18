/*
Extracting keywords for the slug element
 */
function generateSlug() {
    var title = document.getElementById("id_title");
    var slug = document.getElementById("id_slug");
    var text = title.value.split(" ");
    var len = text.length;

    // TODO: Remove all punctuation from text

    var slugValue = '';
    if(len >= 3) {
        slugValue = slugValue.concat(text[0], "-", text[1], "-", text[len-1]).toLowerCase();
    }
    else if (len == 2) {
        slugValue = slugValue.concat(text[0], "-", text[1]).toLowerCase();
    }
    else {
        slugValue = text[0].toLowerCase();
    }

    slug.value = slugValue;
}
