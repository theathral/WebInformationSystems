// Back to Top Button
// $(".back-to-top").hide();

$(window).scroll(function () {
    if ($(this).scrollTop() > 150) {
        $(".back-to-top").fadeIn();
    } else {
        $(".back-to-top").fadeOut();
    }
});

$(".back-to-top").on("click", function () {
    $("html, body").animate({scrollTop: 0}, 800);
    return false;
});


// Hospital Results
$("*.btn-collapse").on("click", function () {
    $(this).closest("*.card-header").next().collapse('toggle');
});
// #Hospital Results


// Checkbox for On Duty Changes
$("#onDutyCheckbox").on("change", function onDutyChange() {
    if ($(this).prop("checked")) {
        $("#departmentFilter").prop("disabled", true);
        $("#dateDiv").fadeIn();
    } else {
        $("#departmentFilter").prop("disabled", false);
        $("#dateDiv").fadeOut();
    }

    $(".selectpicker").selectpicker("refresh");
});
// #Checkbox for On Duty Changes


// Date Options
$(".datepicker").datepicker({
    format: "dd/mm/yyyy",
    startDate: "+0d",
    endDate: "+100d",
    maxViewMode: 1,
    todayBtn: "linked",
    autoclose: true,
    todayHighlight: true
}).datepicker("setDate",'now');
// #Date Options


// Static Filtering for Part 1
$(".selectpicker").selectpicker();

$('select.selectpicker').on("change", function () {

    var region = $('#regionFilter option:selected').val().toString();
    var hospital = $('#hospitalFilter option:selected').val().toString();

    switch (region) {
        case "0": // Athens
            $("#AgiosAndreas").hide();
            $("#AHEPA").hide();
            $("#Attikon").show();
            $("#Euaggelismos").show();

            $("#AgiosAndreasCard").hide();
            $("#AHEPACard").hide();
            $("#AttikonCard").show();
            $("#EuaggelismosCard").show();
            break;
        case "1": // Patra
            $("#AgiosAndreas").show();
            $("#AHEPA").hide();
            $("#Attikon").hide();
            $("#Euaggelismos").hide();

            $("#AgiosAndreasCard").show();
            $("#AHEPACard").hide();
            $("#AttikonCard").hide();
            $("#EuaggelismosCard").hide();

            break;
        case "2": // Thessaloniki
            $("#AgiosAndreas").hide();
            $("#AHEPA").show();
            $("#Attikon").hide();
            $("#Euaggelismos").hide();

            $("#AgiosAndreasCard").hide();
            $("#AHEPACard").show();
            $("#AttikonCard").hide();
            $("#EuaggelismosCard").hide();

            break;
        default:
            $("#AgiosAndreas").show();
            $("#AHEPA").show();
            $("#Attikon").show();
            $("#Euaggelismos").show();

            $("#AgiosAndreasCard").show();
            $("#AHEPACard").show();
            $("#AttikonCard").show();
            $("#EuaggelismosCard").show();

            $("#regionFilter").val("");

            break;
    }

    switch (hospital) {
        case "0": // Agios Andreas
            $("#Athens").hide();
            $("#Patra").show();
            $("#Thessaloniki").hide();

            $("#AgiosAndreasCard").show();
            $("#AHEPACard").hide();
            $("#AttikonCard").hide();
            $("#EuaggelismosCard").hide();

            break;
        case "1": // AHEPA
            $("#Athens").hide();
            $("#Patra").hide();
            $("#Thessaloniki").show();

            $("#AgiosAndreasCard").hide();
            $("#AHEPACard").show();
            $("#AttikonCard").hide();
            $("#EuaggelismosCard").hide();

            break;
        case "2": // Attikon
            $("#Athens").show();
            $("#Patra").hide();
            $("#Thessaloniki").hide();

            $("#AgiosAndreasCard").hide();
            $("#AHEPACard").hide();
            $("#AttikonCard").show();
            $("#EuaggelismosCard").hide();

            break;
        case "3": // Euaggelismos
            $("#Athens").show();
            $("#Patra").hide();
            $("#Thessaloniki").hide();

            $("#AgiosAndreasCard").hide();
            $("#AHEPACard").hide();
            $("#AttikonCard").hide();
            $("#EuaggelismosCard").show();

            break;
        default:
            $("#Athens").show();
            $("#Patra").show();
            $("#Thessaloniki").show();

            $("#hospitalFilter").val("");

            break;
    }

    $('.selectpicker').selectpicker('refresh');

});
// #Static Filtering for Part 1
