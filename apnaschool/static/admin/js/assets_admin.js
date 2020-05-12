console.log("qwerty");
django.jQuery('#id_document_category').change(function(){
if(django.jQuery("#id_document_category option:selected").text() == 1)
    {
        django.jQuery(".form-row.field-link").hide();
    }else
    {
        django.jQuery(".form-row.field-link").show();
    }
});