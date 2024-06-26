
/* Associate a datetime picker to the elements */
export function activate_datetimepicker(){
    jQuery(".date").datetimepicker({
        initialDate: new Date(),
        todayHighlight: true,
        format: "yyyy-mm-ddThh:ii:ss",
        sideBySide: true,
        todayBtn: "linked"
    });
}
