document.getElementById("onDutyCheckbox").checked = true;
document.getElementById("departmentDiv").style.display = "none";
document.getElementById("dateDiv").style.display = "block";
// current date

function onDutyChange(onDuty) {

    if (onDuty.checked) {
        document.getElementById("departmentDiv").style.display = "none";
        document.getElementById("dateDiv").style.display = "block";
    } else {
        document.getElementById("departmentDiv").style.display = "block";
        document.getElementById("dateDiv").style.display = "none";
    }

}

$("*.btn-collapse-hospital").on('click', function () {
    $(this).closest("*.card-header").next().collapse('toggle');
});
