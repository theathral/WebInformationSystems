// Back to Top Button
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
// #Back to Top Button


// Hospital Results
function setcollapse() {
    $("*.btn-collapse").on("click", function () {
        $(this).toggleClass("collapsed");
        $(this).closest("*.card-header").next().collapse("toggle");
    });
}

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
    startDate: "-100d",
    endDate: "+100d",
    disableTouchKeyboard: true,
    maxViewMode: 1,
    todayBtn: "linked",
    autoclose: true,
    todayHighlight: true
}).datepicker("setDate", "now");
// #Date Options


// Static Filtering for Part 1
function add_hospital_result(hos) {
    $("<div/>").addClass(["card", "hospital-card"]).attr("id", "hos-res-" + hos.id).append(
        $("<div/>").addClass(["card-header", "p-0"]).attr("role", "tab").append(
            $("<button/>").addClass(["btn", "btn-block", "text-left", "rgba-opacity", "main-color-bg", "btn-collapse", "collapsed"]).attr("aria-expanded", "true").append(
                $("<div/>").addClass(["h5", "mb-0"]).append(
                    $("<i/>").addClass(["fas", "fa-hospital"]),
                    " ", hos.name,
                    $("<i/>").addClass(["fas", "fa-angle-up", "rotate-icon", "float-right"])
                )
            )
        ),
        $("<div/>").addClass("collapse").attr("role", "tabpanel").append(
            make_info(hos)
        )
    ).appendTo($("#hospital-results"));
}

function make_info(hos) {
    let info = $("<div/>").addClass(["contact-info-wrapper", "m-3", "overflow-auto"]);
    let info_fields = [
        {name: "telephone", icon_class: "fa-phone-alt", pretext: "Telephone:"},
        {name: "address", icon_class: "fa-map-marker-alt", pretext: "Address:"},
        {name: "email", icon_class: "fa-envelope", pretext: "Email:"},
        {name: "postcode", icon_class: "fa-map-pin", pretext: "Postcode:"},
        {name: "website", icon_class: "fa-link", pretext: "Website:"}
    ];
    info_fields.forEach(
        info_field => {
            if (hos[info_field.name] !== null) {
                info.append(
                    $("<div/>").append(
                        $("<i/>").addClass(["fas", info_field.icon_class, "fa-lg", "m-2"]),
                        info_field.pretext
                    ),
                    $("<div/>").text(hos[info_field.name])
                );
            }
        }
    )
    return info;
}


$(".selectpicker").selectpicker();

$('select.selectpicker').on("change", function () {

    const region_id = $('#regionFilter').val().toString();
    const hospital = $('#hospitalFilter').val().toString();
    const department = $('#departmentFilter').val().toString();
    const onDuty = $('#onDutyCheckbox').is(":checked");
    const date = $('#dateFilter').val().toString();

    let filterStr = ""
    if (region_id !== "") {
        filterStr += "region_id=" + region_id + "&"
    }
    if (hospital !== "") {
        filterStr += "hospital=" + hospital + "&"
    }
    if (department !== "") {
        filterStr += "department=" + department + "&"
    }
    if (onDuty) {
        filterStr += "date=" + date + "&"
    }

    fetch("/api/v1/filter?" + filterStr)
        .then(response => response.json())
        .then(data => {

            document.getElementById("hospital-results").innerHTML = "";

            Object.values(data).sort((a, b) => a.name.localeCompare(b.name)).forEach(add_hospital_result);

            setcollapse();

            console.log(data)

        });


});


// $('select.selectpicker').on("change", function () {
//
//     var region = $('#regionFilter option:selected').val().toString();
//     var hospital = $('#hospitalFilter option:selected').val().toString();
//
//     switch (region) {
//         case "0": // Athens
//             $("#AgiosAndreas").hide();
//             $("#AHEPA").hide();
//             $("#Attikon").show();
//             $("#Euaggelismos").show();
//
//             $("#AgiosAndreasCard").hide();
//             $("#AHEPACard").hide();
//             $("#AttikonCard").show();
//             $("#EuaggelismosCard").show();
//             break;
//         case "1": // Patra
//             $("#AgiosAndreas").show();
//             $("#AHEPA").hide();
//             $("#Attikon").hide();
//             $("#Euaggelismos").hide();
//
//             $("#AgiosAndreasCard").show();
//             $("#AHEPACard").hide();
//             $("#AttikonCard").hide();
//             $("#EuaggelismosCard").hide();
//
//             break;
//         case "2": // Thessaloniki
//             $("#AgiosAndreas").hide();
//             $("#AHEPA").show();
//             $("#Attikon").hide();
//             $("#Euaggelismos").hide();
//
//             $("#AgiosAndreasCard").hide();
//             $("#AHEPACard").show();
//             $("#AttikonCard").hide();
//             $("#EuaggelismosCard").hide();
//
//             break;
//         default:
//             $("#AgiosAndreas").show();
//             $("#AHEPA").show();
//             $("#Attikon").show();
//             $("#Euaggelismos").show();
//
//             $("#AgiosAndreasCard").show();
//             $("#AHEPACard").show();
//             $("#AttikonCard").show();
//             $("#EuaggelismosCard").show();
//
//             $("#regionFilter").val("");
//
//             break;
//     }
//
//     switch (hospital) {
//         case "0": // Agios Andreas
//             $("#Athens").hide();
//             $("#Patra").show();
//             $("#Thessaloniki").hide();
//
//             $("#AgiosAndreasCard").show();
//             $("#AHEPACard").hide();
//             $("#AttikonCard").hide();
//             $("#EuaggelismosCard").hide();
//
//             break;
//         case "1": // AHEPA
//             $("#Athens").hide();
//             $("#Patra").hide();
//             $("#Thessaloniki").show();
//
//             $("#AgiosAndreasCard").hide();
//             $("#AHEPACard").show();
//             $("#AttikonCard").hide();
//             $("#EuaggelismosCard").hide();
//
//             break;
//         case "2": // Attikon
//             $("#Athens").show();
//             $("#Patra").hide();
//             $("#Thessaloniki").hide();
//
//             $("#AgiosAndreasCard").hide();
//             $("#AHEPACard").hide();
//             $("#AttikonCard").show();
//             $("#EuaggelismosCard").hide();
//
//             break;
//         case "3": // Euaggelismos
//             $("#Athens").show();
//             $("#Patra").hide();
//             $("#Thessaloniki").hide();
//
//             $("#AgiosAndreasCard").hide();
//             $("#AHEPACard").hide();
//             $("#AttikonCard").hide();
//             $("#EuaggelismosCard").show();
//
//             break;
//         default:
//             $("#Athens").show();
//             $("#Patra").show();
//             $("#Thessaloniki").show();
//
//             $("#hospitalFilter").val("");
//
//             break;
//     }
//
//     $('.selectpicker').selectpicker('refresh');
//
// });
// #Static Filtering for Part 1
