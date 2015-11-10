$('input[type="checkbox"].large').checkbox({
    buttonStyle: 'btn-link btn-large',
    checkedClass: 'icon-check',
    uncheckedClass: 'icon-check-empty'
});

$('#example-multiple-selected').multiselect();

$(document).ready(function() {
    $('#bootstrapSelectForm')
        .find('[name="humeurs"]')
            .selectpicker()
            .change(function(e) {
                // revalidate the language when it is changed
                $('#bootstrapSelectForm').formValidation('revalidateField', 'humeurs');
            })
            .end()
        .formValidation({
            framework: 'bootstrap',
            excluded: ':disabled',
            icon: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                humeurs: {
                    validators: {
                        callback: {
                            message: 'Veuillez choisir au minimum 2 humeurs',
                            callback: function(value, validator, $field) {
                                // Get the selected options
                                var options = validator.getFieldElements('humeurs').val();
                                return (options != null && options.length >= 2 );
                            }
                        }
                    }
                },
            }
        });
});
