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


// Checkbox for On Duty Changes
$("#onDutyCheckbox").on("change", function onDutyChange() {
    if ($(this).prop("checked"))
        $("#dateDiv").fadeIn();
    else
        $("#dateDiv").fadeOut();


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


// Dynamic Filtering
function add_options_region(divId, currentRegion) {
    fetch("/api/v1/region")
        .then(response => response.json())
        .then(data => {

            Object.values(data).sort((a, b) => a.name.localeCompare(b.name)).forEach(data => {

                if (currentRegion === data.id.toString()) {
                    $("#" + divId)
                        .append($("<option></option>").attr('selected', true).attr("value", data.id)
                            .append(data.name));
                    $('.selectpicker').selectpicker('refresh');
                } else {
                    $("#" + divId)
                        .append($("<option></option>").attr("value", data.id)
                            .append(data.name));
                }
            });

            $('.selectpicker').selectpicker('refresh');

            console.log(data)

        });
}

function add_options_hospital() {
    fetch("/api/v1/hospital")
        .then(response => response.json())
        .then(data => {

            Object.values(data).sort((a, b) => a.name.localeCompare(b.name)).forEach(data => {
                $("#hospitalFilter")
                    .append($("<option></option>").attr("value", data.id).attr("id", "hos-" + data.id)
                        .append(data.name));
            });

            $('.selectpicker').selectpicker('refresh');

            console.log(data)

        });
}

function add_options_department() {
    fetch("/api/v1/department")
        .then(response => response.json())
        .then(data => {

            Object.values(data).sort((a, b) => a.name.localeCompare(b.name)).forEach(data => {
                $("#departmentFilter")
                    .append($("<option></option>").attr("value", data.id).attr("id", "hos-" + data.id)
                        .append(data.name));
            });

            $('.selectpicker').selectpicker('refresh');

            console.log(data)

        });
}

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

function setHospitals(current_region) {

    const region_id = $('#regionFilter').val().toString();
    const hospital = $('#hospitalFilter').val().toString();
    const department = $('#departmentFilter').val().toString();
    const onDuty = $('#onDutyCheckbox').is(":checked");
    const date = $('#dateFilter').val().toString();

    let filterStr = ""
    if (region_id !== "") {
        filterStr += "region_id=" + region_id + "&"
    } else if (current_region !== "") {
        filterStr += "region_id=" + current_region + "&"
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

            $("*.btn-collapse").on("click", function () {
                $(this).toggleClass("collapsed");
                $(this).closest("*.card-header").next().collapse("toggle");
            });

            console.log(data)

        });

}

$('.filterChange').on("change", function () {
    setHospitals("");
});
// #Dynamic Filtering


// Confirmation alert when deleting an account
$("#deleteBtn").on("click", function () {
    Swal.fire({
        title: 'Are you sure?',
        text: "Delete my account.\nYou won't be able to revert this!",
        icon: 'warning',
        timer: 10000,
        timerProgressBar: true,
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        confirmButtonColor: '#d33',
        cancelButtonText: 'No, cancel!',
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false

    }).then((result) => {
        if (result.value) {
            Swal.fire({
                    title: 'Deleted!',
                    text: 'Your account has been deleted.\n"We will miss you!"',
                    icon: 'success',
                    timer: 5000,
                    timerProgressBar: true,
                }
            ).then(() => {
                window.location = "/deleteUser"
            })
        } else {
            Swal.fire({
                    title: 'Cancelled!',
                    text: 'Your account is safe ❤',
                    icon: 'info',
                    timer: 5000,
                    timerProgressBar: true,
                }
            )
        }
    })
})
// #Confirmation alert when deleting an account

