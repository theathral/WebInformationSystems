$("#onDutyCheckbox").on("change", function onDutyChange() {
    if ($(this).prop("checked")) {
        document.getElementById("departmentDiv").style.display = "none";
        document.getElementById("dateDiv").style.display = "block";
    } else {
        document.getElementById("departmentDiv").style.display = "block";
        document.getElementById("dateDiv").style.display = "none";
    }
});

$("*.btn-collapse").on('click', function () {
    $(this).closest("*.card-header").next().collapse('toggle');
});

$("#slideshow").carousel({
    interval: false,
    wrap: false
});