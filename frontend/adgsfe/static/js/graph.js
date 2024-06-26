import * as vis_data from "vis-data/dist/umd.js";
import { DataSet } from "vis-data/peer/esm/vis-data"
import * as vis_timeline_graph2d from "vis-timeline/peer/umd/vis-timeline-graph2d.js";

/* Function to display a timeline given the id of the DOM where to
 * attach it and the items to show with corresponding groups */
export function display_timeline(dom_id, items, groups, focus_id, options, show_hide = true){
    
    var groups_dataset = new DataSet(groups);

    /* Obtain timeline container */
    const container = document.getElementById(dom_id);
    
    if (options == undefined){
        options = {
            groupOrder: 'content',
            margin: {
                item : {
                    horizontal : 0
                }
            },
        };
    };

    if (show_hide){
        options["groupTemplate"] = function(group){
            var container = document.createElement('div');
            var label = document.createElement('span');
            label.innerHTML = group.content + ' ';
            container.insertAdjacentElement('afterBegin',label);
            var hide = document.createElement('button');
            hide.innerHTML = 'hide';
            hide.style.fontSize = 'small';
            hide.addEventListener('click',function(){
                groups_dataset.update({id: group.id, visible: false});
            });
            container.insertAdjacentElement('beforeEnd',hide);
            return container;
        }
    }
    
    const threshold = 1000
    var timeline;
    if (items.length > threshold){
        container.style.display = "none";
        const button_container = document.createElement("div");
        container.parentNode.appendChild(button_container);
        const button = document.createElement("button");
        button.classList.add("btn");
        button.classList.add("btn-primary");
        button.innerHTML = "Number of elements (" + items.length + ") exceeded the threshold (" + threshold + "). Click here to show the timeline graph";
        button_container.appendChild(button);
        button.onclick = function (){
            button.style.display = "none";
            container.style.display = "inherit";
            timeline = show_timeline(dom_id, items, container, groups_dataset, options, show_hide);

            /* Focus on element with id focus_id */
            setTimeout(function(){
                timeline.focus(focus_id)
            }, 1000);

        };
    }
    else{
        timeline = show_timeline(dom_id, items, container, groups_dataset, options, show_hide);
        
        /* Focus on element with id focus_id */
        setTimeout(function(){
            timeline.focus(focus_id)
        }, 1000);
    }
};

function show_timeline(dom_id, items, container, groups_dataset, options, show_hide){

    var timeline_container = container;
    
    if (show_hide){
        
        /* function to make all groups visible again */
        function showAllGroups(){
            groups_dataset.forEach(function(group){
                groups_dataset.update({id: group.id, visible: true});
            })
        };
        /* Create container for options */
        const options_container = document.createElement("div");
        container.appendChild(options_container);
        const button = document.createElement("button");
        button.classList.add("btn");
        button.classList.add("btn-primary");
        button.classList.add("btn-margin-1");
        button.innerHTML = "Restore hidden elements";
        options_container.appendChild(button);
        button.onclick = function (){
            showAllGroups();
        };

        /* Create container for timline */
        timeline_container = document.createElement("div");
        container.appendChild(timeline_container);
    };
    
    var items_dataset = new DataSet(items)
    const timeline = new vis_timeline_graph2d.Timeline(timeline_container, items_dataset, groups_dataset, options);

    timeline.on("click", function (params) {
        show_timeline_item_information(params, items, dom_id)
    });

    return timeline;
};

function show_timeline_item_information(params, items, dom_id){

    const element_id = params["item"]
    if (element_id != undefined){
        const header_content = "Detailed information for the timeline element: " + element_id;
        const item = items.filter(item => item["id"] == element_id)[0]
        const body_content = item["tooltip"];
        const x = params["pageX"];
        const y = params["pageY"];

        const div = create_div(dom_id, element_id, header_content, body_content, x, y)
        drag_element(div)
    }
}

function create_div(dom_id, element_id, header_content, body_content, x, y){

    const container = document.getElementById("body");

    // Create div
    const div = document.createElement("div");
    div.id = dom_id + "_" + element_id
    container.appendChild(div);
    // Add class to the div
    div.classList.add("draggable-div");
    div.style.top = y + "px";
    div.style.left = x + "px";

    // Create header for the div
    const div_header = document.createElement("div");
    const div_header_text = document.createElement("div");
    div_header_text.innerHTML = header_content;
    div_header.id = "header"
    div.appendChild(div_header);
    div_header.appendChild(div_header_text);
    // Add class to the div
    div_header_text.classList.add("draggable-div-header-text");

    // Add close icon
    const div_header_close = document.createElement("div");
    div_header.appendChild(div_header_close);
    const span_close = document.createElement("span");
    div_header_close.appendChild(span_close);
    span_close.classList.add("fa");
    span_close.classList.add("fa-times");
    div_header_close.classList.add("draggable-div-close");
    div_header_close.onclick = function(){
        div.parentNode.removeChild(div);
    };

    // Create body for the div
    const div_body = document.createElement("div");
    div.appendChild(div_body);
    div_body.innerHTML = body_content;
    div_body.id = "body"
    div_body.classList.add("draggable-div-body");

    return div;

}

function drag_element(element) {

    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    // The element is draggable only using the header
    element.querySelector("#header").onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        element.style.top = (element.offsetTop - pos2) + "px";
        element.style.left = (element.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
