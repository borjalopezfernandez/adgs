/* js */
import "bootstrap/dist/js/bootstrap.min.js";
import "bootstrap-datetime-picker/js/bootstrap-datetimepicker.min.js";
import "bootstrap-responsive-tabs/dist/js/jquery.bootstrap-responsive-tabs.min.js";
import "datatables/media/js/jquery.dataTables.min.js";
import "datatables.net/js/jquery.dataTables.min.js";
import "datatables.net-buttons/js/dataTables.buttons.min.js";
import "datatables.net-buttons/js/buttons.html5.min.js";
import "datatables.net-select/js/dataTables.select.js";
import * as toastr from "toastr/toastr.js";
import * as dates from "./dates.js";
import * as queryFunctions from "./query.js";
import * as datatableFunctions from "./datatables.js";
import * as graph from "./graph.js";
import * as vis_data from "vis-data/dist/umd.js";
import * as vis_timeline_graph2d from "vis-timeline/peer/umd/vis-timeline-graph2d.js";

/* css */
import "bootstrap-datetime-picker/css/bootstrap-datetimepicker.min.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "bootstrap-responsive-tabs/dist/css/bootstrap-responsive-tabs.css";
import "datatables/media/css/jquery.dataTables.min.css";
import "datatables.net-select-dt/css/select.dataTables.min.css";
import "vis-timeline/dist/vis-timeline-graph2d.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "toastr/build/toastr.min.css";

export let datatables = datatableFunctions;
export let jquery = jQuery;


/* Activate tooltips */
jQuery(document).ready(function(){
  jQuery('[data-toggle="tooltip"]').tooltip();
});

/* Toasts configuration */
toastr.options.progressBar = true; // Show how long it takes before it expires
toastr.options.timeOut = 10000; // How long the toast will display without user interaction (milliseconds)
toastr.options.extendedTimeOut = 10000; // How long the toast will display after a user hovers over it (milliseconds)

/* Associate datetimepicker functionality */
jQuery(document).ready(function () {
    dates.activate_datetimepicker();
});

/***
* QUERY *
***/

/* Function to provide a way to request information from javascript passing json as parameter */
export function request_info_json(url, callback, json, show_loader = false){

    queryFunctions.request_info_json(url, callback, json, show_loader);

};

/***
* Graph functions
***/

/* Function to display a timeline given the id of the DOM where to
 * attach it and the items to show with corresponding groups */
export function display_timeline(dom_id, items, groups, options){

    jQuery(document).ready(function(){
        graph.display_timeline(dom_id, items, groups, options);
    });

};

/* Event key listeners */
document.addEventListener("keydown", function(event) {
    const key = event.key
    if (key === "Escape") {
        // Escape key is used to close tooltips
        // Obtain tooltips
        const draggable_divs = document.getElementsByClassName("draggable-div")

        // Remove the last one
        if (draggable_divs.length > 0){
            const last_draggable_div = draggable_divs[draggable_divs.length - 1]
            last_draggable_div.parentNode.removeChild(last_draggable_div);
        }
    }
});
