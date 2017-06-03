var file;
var path;
var obj = $("#face_interface");

$("document").ready(function () 
{
    $('#selected').hide();

    $("#uploadImage").click(function () 
    {
        openfileInput()
    });

    $("#file").change(function () 
    {
        file = $('#file').prop("files")[0];
        showFileName($("#file").val());
        path = URL.createObjectURL(file);
        console.log(path);
        uploadImage(path);
    });

    obj.on('dragenter', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
        $(this).css('border', '2px dotted black');
    });

    obj.on('dragover', function (e) 
    {
        e.stopPropagation();
        e.preventDefault();
    });

    obj.on('drop', function (e) 
    {
        e.preventDefault();
        file = e.originalEvent.dataTransfer.files[0];
        $("#filename").val(file.name);
        path = URL.createObjectURL(file);
        $("input[type='file']").prop("files", e.originalEvent.dataTransfer.files);
        console.log(path);
        uploadImage(path);
    });

    $('#remove').on('click', function () 
    {
        $('#selected').hide();
        $('#uploadForm').show();
        $('#file').val("");
    });

    $('#submit').on('click', function () 
    {
        $('#uploadForm').submit();
        $('#file').val("");
    });
});

function showFileName() 
{
    var filename = $('#file').val();
    filename = filename.replace(/.*[\/\\]/, '');
    $("#filename").val(filename).focus();
}

$(document).on('dragenter', function (e) 
{
    e.stopPropagation();
    e.preventDefault();
});

$(document).on('dragover', function (e) 
{
    e.stopPropagation();
    e.preventDefault();
});

$(document).on('drop', function (e) 
{
    e.stopPropagation();
    e.preventDefault();
});

function openfileInput() 
{
    $('#file').click();
}

function uploadImage(data) 
{
    $('#selected').show();
    $('#selectedImage').attr('src', data);
    $('#uploadForm').hide();
}