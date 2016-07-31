
$(document).ready(function() {

    var base_url = window.location.href + "subs/";

    $('.button').click(function() {
        // Get the values from the dropdown boxes
        var city = $('#cities option:selected').attr('value');
        var tag = $('#tags option:selected').attr('value');
        var url = base_url + city + '/' + tag;
        // make an ajax call to get the data
        //  rewrite this  to avoid hard coding in the url
        $.ajax({
            url: url,
            dataType: "json",
            success: function(data) {
                for (var sub_name in data) {
                    console.log(sub_name);
                    console.log(data[sub_name][0]);
                };
            }
            /*
            // Display the data
            // There is probably more that needs to be dont to parse the json
            success: function(subs) {
                $list.empty();     // Clear anything currently in the list
                for (i=0; i < subs.length; i++ ) {
                    // in general will want to add this to a table along with dates and links
                    $list.append("<p class=submission>" + subs[i]["Name"] + "</p>");
                    $list.append('<br>');
                }
            },
            */

            // add a function to trigger on a failed request
        });
    });
});
