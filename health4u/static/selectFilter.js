$(".selectpicker").selectpicker();

$('select.selectpicker').on('change', function () {

    var region = $('#region option:selected').val().toString();
    var hospital = $('#hospital option:selected').val().toString();

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
        case "-":
            $("#AgiosAndreas").show();
            $("#AHEPA").show();
            $("#Attikon").show();
            $("#Euaggelismos").show();

            $("#AgiosAndreasCard").show();
            $("#AHEPACard").show();
            $("#AttikonCard").show();
            $("#EuaggelismosCard").show();

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
        case "-":
            $("#Athens").show();
            $("#Patra").show();
            $("#Thessaloniki").show();

            break;
    }

    $('.selectpicker').selectpicker('refresh');
});
