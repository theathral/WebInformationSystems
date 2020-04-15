$("[data-toggle='collapse']").on('click', function () {
    $(this).closest("*.card-header").next().collapse('toggle');
});
