$("*.btn-collapse-hospital").on('click', function () {
    $(this).closest("*.card-header").next().collapse('toggle');
});
