/* SCRIPTS TO HANDLE THE CROPPER BOX */
var $image = $("#image");
var cropBoxData;
var canvasData;
$("#modalCrop").on("shown.bs.modal", function () {
  $image.cropper({
    viewMode: 1,
    aspectRatio: 7/4.3,
    minCropBoxWidth: 70,
    minCropBoxHeight: 43,
    ready: function () {
      $image.cropper("setCanvasData", canvasData);
      $image.cropper("setCropBoxData", cropBoxData);
    }
  });
}).on("hidden.bs.modal", function () {
  cropBoxData = $image.cropper("getCropBoxData");
  canvasData = $image.cropper("getCanvasData");
  $image.cropper("destroy");
});

$(".js-zoom-in").click(function () {
  $image.cropper("zoom", 0.1);
});

$(".js-zoom-out").click(function () {
  $image.cropper("zoom", -0.1);
});

/* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
$("#crop_button").click(function () {
  var cropData = $image.cropper("getData");
  $("#id_x").val(cropData["x"]);
  $("#id_y").val(cropData["y"]);
  $("#id_height").val(cropData["height"]);
  $("#id_width").val(cropData["width"]);
  console.log($("#id_x").val(), $("#id_y").val(), $("#id_height").val(), $("#id_width").val());
  $("#modalCrop").modal("hide");
  console.log(cropData["x"], cropData["y"], cropData["height"], cropData["width"])
});
