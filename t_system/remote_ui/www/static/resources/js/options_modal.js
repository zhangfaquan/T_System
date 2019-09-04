
const update_control_div = document.getElementById("update_control_div");
const update_control_btn = document.getElementById("update_control_btn");
const update_control_io_div = document.getElementById("update_control_io_div");

const wifi_control_div = document.getElementById("wifi_control_div");
const wifi_connections_btn = document.getElementById("wifi_connections_btn");
const wifi_control_io_div = document.getElementById("wifi_control_io_div");
const network_ssid_input = document.getElementById("network_ssid_input");
const network_password_input = document.getElementById("network_password_input");
const create_new_network_btn = document.getElementById("create_new_network_btn");
const network_list_ul = document.getElementById("network_list_ul");

const audio_control_div = document.getElementById("audio_control_div");
const audio_control_btn = document.getElementById("audio_control_btn");
const audio_control_io_div = document.getElementById("audio_control_io_div");

const face_encoding_div = document.getElementById("face_encoding_div");
const face_encoding_btn = document.getElementById("face_encoding_btn");
const face_encoding_io_div = document.getElementById("face_encoding_io_div");

const lang_select_div = document.getElementById("lang_select_div");
const lang_select_btn = document.getElementById("lang_select_btn");
const language_dropdown_div = document.getElementById("language_dropdown_div");



// a_i_checkbox.addEventListener("change", function () {  // Checkbox onchange sample
//
//     if (a_i_checkbox.checked){
//     }
//     else {
//     }
//
// });

/**
 * Method of getting specified network information with its ssid or the all existing network information.
 * It is triggered via a click on settings_btn or clicked specified network on network list.
 */
function get_network_data(ssid = null) {

    if (ssid) {
        jquery_manager.get_data("/api/network?ssid=" + ssid + "&admin_id=" + admin_id);
    } else {
        jquery_manager.get_data("/api/network?admin_id=" + admin_id);
    }
}

let update_control_btn_click_count = 0;
update_control_btn.addEventListener("click", function () {
    update_control_btn_click_count++;

    if (update_control_btn_click_count <= 1) {

        dark_deep_background_div.classList.toggle("focused");
        dark_overlay_active = true;
        toggle_elements([wifi_control_div, audio_control_div, face_encoding_div, lang_select_div]);
        update_control_div.classList.toggle("col");
        update_control_div.classList.toggle("focused");
        update_control_div.classList.toggle("higher");
        update_control_io_div.classList.toggle("focused");

    } else {
        dark_deep_background_div.classList.toggle("focused");
        dark_overlay_active = false;
        toggle_elements([wifi_control_div, audio_control_div, face_encoding_div, lang_select_div]);
        update_control_div.classList.toggle("col");
        update_control_div.classList.toggle("focused");
        update_control_div.classList.toggle("higher");
        update_control_io_div.classList.toggle("focused");

        update_control_btn_click_count = 0;
    }
});

let wifi_connections_btn_click_count = 0;
wifi_connections_btn.addEventListener("click", function () {
    wifi_connections_btn_click_count++;

    if (wifi_connections_btn_click_count <= 1) {
        get_network_data();

        let timer_settings_cont = setInterval(function () {

            if (requested_data !== null) {

                if (requested_data["status"] === "OK") {

                    while (network_list_ul.firstChild) {
                        network_list_ul.removeChild(network_list_ul.firstChild);
                    }

                    for (let c = 0; c < requested_data["data"].length; c++) {
                        // console.log(event_db[c]["name"]);
                        let li = document.createElement('li');
                        let section = document.createElement('section');

                        let ssid_output = document.createElement('output');
                        let password_output = document.createElement('output');

                        ssid_output.value = requested_data["data"][c]["ssid"];
                        password_output.value = requested_data["data"][c]["password"];

                        li.appendChild(section);
                        section.appendChild(ssid_output);
                        section.appendChild(password_output);

                        network_list_ul.appendChild(li);
                    }

                    dark_deep_background_div.classList.toggle("focused");
                    dark_overlay_active = true;

                    toggle_elements([update_control_div, audio_control_div, face_encoding_div, lang_select_div]);
                    wifi_control_div.classList.toggle("col");
                    wifi_control_div.classList.toggle("focused");
                    wifi_control_div.classList.toggle("higher");
                    wifi_control_io_div.classList.toggle("focused");

                }
                requested_data = null;
                clearInterval(timer_settings_cont)
            }
        }, 500);

        // jquery_manager.post_data("/try", {"bla": "bla"})

    } else {
        dark_deep_background_div.classList.toggle("focused");
        dark_overlay_active = false;
        toggle_elements([update_control_div, face_encoding_div, lang_select_div]);
        wifi_control_div.classList.toggle("col");
        wifi_control_div.classList.toggle("focused");
        wifi_control_div.classList.toggle("higher");
        wifi_control_io_div.classList.toggle("focused");
        wifi_connections_btn_click_count = 0;
    }

});

function show_create_new_wifi_button() {
    if(network_ssid_input.value !== "" && network_password_input.value !== ""){
        network_ssid_input.classList.add("new_network_input_transition");
        network_password_input.classList.add("new_network_input_transition");
        show_element(create_new_network_btn);
    }
    else {
        network_ssid_input.classList.remove("new_network_input_transition");
        network_password_input.classList.remove("new_network_input_transition");
        hide_element(create_new_network_btn);
    }
}

network_ssid_input.addEventListener("mousemove", show_create_new_wifi_button);
network_password_input.addEventListener("mousemove", show_create_new_wifi_button);

create_new_network_btn.addEventListener("click", function () {

    let data = {"ssid": network_ssid_input.value, "password": network_password_input.value};
    jquery_manager.post_data("/api/network", data);

    network_ssid_input.value = "";
    network_password_input.value = "";
    wifi_connections_btn.click();
    wifi_connections_btn.click();

    admin_id = response_data["admin_id"];
    console.log(admin_id)
});

audio_control_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, face_encoding_div, lang_select_div]);
    audio_control_div.classList.toggle("col");
    audio_control_div.classList.toggle("focused");
    audio_control_div.classList.toggle("higher");
    audio_control_io_div.classList.toggle("focused");
});

face_encoding_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");
    toggle_elements([update_control_div, wifi_control_div, audio_control_div, lang_select_div]);
    face_encoding_div.classList.toggle("col");
    face_encoding_div.classList.toggle("focused");
    face_encoding_div.classList.toggle("higher");
    face_encoding_io_div.classList.toggle("focused");
});

lang_select_btn.addEventListener("click", function () {

    dark_overlay_active = !dark_deep_background_div.classList.contains("focused");
    dark_deep_background_div.classList.toggle("focused");

    toggle_elements([update_control_div, wifi_control_div, audio_control_div, face_encoding_div]);
    lang_select_div.classList.toggle("col");
    lang_select_div.classList.toggle("focused");
    lang_select_div.classList.toggle("higher");
    language_dropdown_div.classList.toggle("focused");
});