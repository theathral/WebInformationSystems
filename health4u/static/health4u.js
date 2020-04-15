$(window).onload(function loadFilters() {
    alert("alert!!!");
    document.getElementById("onDutyCheckbox").checked = true;
    document.getElementById("departmentDiv").style.display = "none";
    document.getElementById("dateDiv").style.display = "block";
    // current date
});

function onDutyChange(onDuty) {

    if (onDuty.checked) {
        document.getElementById("departmentDiv").style.display = "none";
        document.getElementById("dateDiv").style.display = "block";
    } else {
        document.getElementById("departmentDiv").style.display = "block";
        document.getElementById("dateDiv").style.display = "none";
    }

}

// function selectRegion(choice) {
//
//     var hospital = document.getElementById("hospital");
//
//     hospital.removeChild(hospital.firstChild)
//
//     switch (choice) {
//         case "Athens": hospital.
//             break;
//         case "Patra": break;
//         case "Thessaloniki": break;
//     }
// }
//


