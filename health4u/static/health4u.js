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


// Set and get current language
function set_lang(lang_code) {
    document.cookie = "lang=" + lang_code;
    location.reload();
}

function get_lang() {
    return $('html').attr('lang') || "en";
}

// #Set and get current language


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
function compare_function(a, b) {
    if (get_lang() === "el")
        return a.name.localeCompare(b.name)

    return a.name_en.localeCompare(b.name_en)
}

function add_option(divId, data) {
    let id = data.id;
    let name = get_lang() === "el" ? data.name : data.name_en

    $("#" + divId).append($("<option></option>")
        .attr("value", id)
        .append(name));
}

function add_option_selected(divId, data) {
    let id = data.id;
    let name = get_lang() === "el" ? data.name : data.name_en

    $("#" + divId).append($("<option></option>")
        .attr('selected', true)
        .attr("value", id)
        .append(name));
}

function add_filter_options(filterStr, divId, option) {
    fetch(filterStr)
        .then(response => response.json())
        .then(data => {

            $("#" + divId).empty();

            if (divId === "regionFilter") {
                $("#" + divId).append('<option value=""></option>');
            }

            fetch(filterStr.split("_")[0] + "/" + option)
                .then(response => response.json())
                .then(item => {

                    if (option !== "" && !data.hasOwnProperty(item.id))
                        data[item.id] = item;

                    Object.values(data).sort((a, b) => compare_function(a, b)).forEach(data => {

                        if (option === data.id.toString()) {
                            add_option_selected(divId, data);
                            $('.selectpicker').selectpicker('refresh');
                        } else
                            add_option(divId, data);
                    });

                    $('.selectpicker').selectpicker('refresh');
                });
        });
}

function add_hospital_result(hos) {
    $("<div/>").addClass(["card", "hospital-card"]).attr("id", "hos-res-" + hos.id).append(
        $("<div/>").addClass(["card-header", "p-0"]).attr("role", "tab").append(
            $("<button/>").addClass(["btn", "btn-block", "text-left", "rgba-opacity", "main-color-bg", "btn-collapse", "collapsed"]).attr("aria-expanded", "true").append(
                $("<div/>").addClass(["h5", "mb-0"]).append(
                    $("<i/>").addClass(["fas", "fa-hospital"]),
                    " ", get_lang() === "el" ? hos.name : hos.name_en,
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
    let greek = get_lang() === "el"

    let prepend_protocol = (url) => {
        if (!url.match(/^[a-zA-Z]+:\/\//)) {
            return 'http://' + url;
        }
        return url;
    }

    let make_field_value = (info_field, hos) => {
        if (info_field.name === "telephone") {
            return $("<a/>").attr("href", "tel:" + hos[info_field.name]).text(hos[info_field.name]);
        } else if (info_field.name === "email") {
            return $("<a/>").attr("href", "mailto:" + hos[info_field.name]).text(hos[info_field.name]);
        } else if (info_field.name === "website") {
            return $("<a/>").attr("href", prepend_protocol(hos[info_field.name])).text(hos[info_field.name]);
        } else {
            return hos[info_field.name];
        }
    };

    let info = $("<div/>").addClass(["contact-info-wrapper", "m-3", "overflow-auto"]);
    let info_fields = [
        {name: "telephone", icon_class: "fa-phone-alt", pretext: greek ? "Τηλέφωνο:" : "Telephone:"},
        {name: "address", icon_class: "fa-map-marker-alt", pretext: greek ? "Διεύθυνση:" : "Address:"},
        {name: "email", icon_class: "fa-envelope", pretext: greek ? "Ηλεκτρονικό Ταχυδρομείο:" : "Email:"},
        {name: "postcode", icon_class: "fa-map-pin", pretext: greek ? "Ταχυδρομικός Κώδικας:" : "Postcode:"},
        {name: "website", icon_class: "fa-link", pretext: greek ? "Ιστοσελίδα:" : "Website:"}
    ];
    info_fields.forEach(
        info_field => {
            if (hos[info_field.name] !== null) {
                info.append(
                    $("<div/>").append(
                        $("<i/>").addClass(["fas", info_field.icon_class, "fa-lg", "m-2"]),
                        info_field.pretext
                    ),
                    $("<div/>").append(make_field_value(info_field, hos))
                );
            }
        }
    )

    return info;
}

function setHospitals(filterStr) {
    fetch(filterStr)
        .then(response => response.json())
        .then(data => {

            document.getElementById("hospital-results").innerHTML = "";

            if (Object.keys(data).length === 0) {
                document.getElementById("hospital-results").innerHTML = get_lang() === "el" ? "(Δεν βρέθηκαν δεδομένα)" : "(No results found)";
            }

            Object.values(data).sort((a, b) => compare_function(a, b)).forEach(add_hospital_result);

            $("*.btn-collapse").on("click", function () {
                $(this).toggleClass("collapsed");
                $(this).closest("*.card-header").next().collapse("toggle");
            });

            $('.selectpicker').selectpicker('refresh');
        });
}

function setFilterPath(current_region) {
    const region_id = $("#regionFilter").val().toString();
    const hospital = $("#hospitalFilter").val().toString();
    const department = $("#departmentFilter").val().toString();
    const onDuty = $("#onDutyCheckbox").is(":checked");
    const date = $("#dateFilter").val().toString();

    let filterStr = ""
    if (region_id !== "") {
        filterStr += "region_id=" + region_id + "&"
    } else if (current_region !== "") {
        filterStr += "region_id=" + current_region + "&"
    }
    if (hospital !== "") {
        filterStr += "hospital_id=" + hospital + "&"
    }
    if (department !== "") {
        filterStr += "department_id=" + department + "&"
    }
    if (onDuty) {
        filterStr += "date=" + date + "&"
    }

    return filterStr;
}

$("#regionFilter").on("change", function () {
    let filterStr = setFilterPath("")

    add_filter_options("/api/v1/region_filter?" + filterStr, "regionFilter", $("#regionFilter").val().toString());
    add_filter_options("/api/v1/hospital_filter?" + filterStr, "hospitalFilter", $("#hospitalFilter").val().toString())
    add_filter_options("/api/v1/department_filter?" + filterStr, "departmentFilter", $("#departmentFilter").val().toString())
    setHospitals("/api/v1/hospital_results?" + filterStr, $("#departmentFilter").val().toString());
});

$("#hospitalFilter").on("change", function () {
    let filterStr = setFilterPath("")

    add_filter_options("/api/v1/region_filter?" + filterStr, "regionFilter", $("#regionFilter").val().toString());
    add_filter_options("/api/v1/hospital_filter?" + filterStr, "hospitalFilter", $("#hospitalFilter").val().toString())
    add_filter_options("/api/v1/department_filter?" + filterStr, "departmentFilter", $("#departmentFilter").val().toString())
    setHospitals("/api/v1/hospital_results?" + filterStr, $("#departmentFilter").val().toString());
});

$("#departmentFilter").on("change", function () {
    let filterStr = setFilterPath("")

    add_filter_options("/api/v1/region_filter?" + filterStr, "regionFilter", $("#regionFilter").val().toString());
    add_filter_options("/api/v1/hospital_filter?" + filterStr, "hospitalFilter", $("#hospitalFilter").val().toString())
    add_filter_options("/api/v1/department_filter?" + filterStr, "departmentFilter", $("#departmentFilter").val().toString())
    setHospitals("/api/v1/hospital_results?" + filterStr, $("#departmentFilter").val().toString());
});

$("#onDutyCheckboxDiv").on("change", function () {
    let filterStr = setFilterPath("")

    add_filter_options("/api/v1/region_filter?" + filterStr, "regionFilter", $("#regionFilter").val().toString());
    add_filter_options("/api/v1/hospital_filter?" + filterStr, "hospitalFilter", $("#hospitalFilter").val().toString())
    add_filter_options("/api/v1/department_filter?" + filterStr, "departmentFilter", $("#departmentFilter").val().toString())
    setHospitals("/api/v1/hospital_results?" + filterStr, $("#departmentFilter").val().toString());
});

$("#dateDiv").on("change", function () {
    let filterStr = setFilterPath("")

    add_filter_options("/api/v1/region_filter?" + filterStr, "regionFilter", $("#regionFilter").val().toString());
    add_filter_options("/api/v1/hospital_filter?" + filterStr, "hospitalFilter", $("#hospitalFilter").val().toString())
    add_filter_options("/api/v1/department_filter?" + filterStr, "departmentFilter", $("#departmentFilter").val().toString())
    setHospitals("/api/v1/hospital_results?" + filterStr, $("#departmentFilter").val().toString());
});
// #Dynamic Filtering


// Confirmation alert when deleting an account
$("#deleteBtn").on("click", function () {
    let greek = get_lang() === "el"

    Swal.fire({
        title: greek ? "Είστε σίγουρος" : "Are you sure?",
        text: greek ? "Ο λογαριασμός σας θα διαγραφεί. Αυτή η ενέργεια είναι μη αναστρέψιμη!"
            : "Your account will be deleted. You won't be able to revert this!",
        icon: "warning",
        timer: 10000,
        timerProgressBar: true,
        showCancelButton: true,
        confirmButtonText: greek ? "Διάγραφή!" : "Yes, delete it!",
        confirmButtonColor: '#d33',
        cancelButtonText: greek ? "Ακύρωση!" : "Cancel!",
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false

    }).then((result) => {
        if (result.value) {
            Swal.fire({
                    title: greek ? "Διεγράφει!" : "Deleted!",
                    text: greek ? "Ο λογαριασμός σας διεγράφει επιτυχώς. Θα μας λείψετε!"
                        : "Your account has been deleted. We will miss you!",
                    icon: "success",
                    timer: 5000,
                    timerProgressBar: true,
                }
            ).then(() => {
                window.location = "/delete_account"
            })
        } else {
            Swal.fire({
                    title: greek ? "Ακυρώθηκε!" : "Cancelled!",
                    text: greek ? "Ο λογαριασμός σας είναι ασφαλής! ❤" : "Your account is safe! ❤",
                    icon: "info",
                    timer: 5000,
                    timerProgressBar: true,
                }
            )
        }
    })
})
// #Confirmation alert when deleting an account


// Under Construction alert
$(".underConstruction").on("click", function () {
    let greek = get_lang() === "el"

    Swal.fire({
        title: greek ? "Υπό κατασκευή!" : "Under Construction!",
        text: greek ? "Αυτή η λειτουργία δεν είναι διαθέσιμη, ακόμα. Δοκιμάστε κάτι διαφορετικό!"
            : "This functionality is not available, yet. Try something else!",
        icon: "info",
        timer: 10000,
        timerProgressBar: true,
        confirmButtonText: greek ? "ΟΚ!" : "OK!"
    })
})
// #Under Construction alert
