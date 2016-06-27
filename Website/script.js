
$(document).ready(

function() {
    $('.button').click( function() {
        var $list = $("#list");
        $list.empty();     // Clear anything currently in the list
        var cities = get_checked('city-check');
        var tags = get_checked('tag-check')
        var subs = get_submissions(cities, tags);
        for (i=0; i < subs.length; i++ ) {
            // in general will want to add this to a table along with dates and links
            $list.append("<p class=submission>" + subs[i]["Name"] + "</p>");
            $list.append('<br>');
        }
});

});

var contains = function(value, list) {
    return (list.indexOf(value) !== -1); }

var get_checked = function(id) {
    output = [];
    $("#" + id + " input:checked").each(function() {
        output.push($(this).attr('value'));
    });
    return output;
};

var get_submissions = function(cities, tags) {
/* Takes list of citie and tags and returns a list of submissions that
   match those criteria */
    // Construct predicates for testing which submissions should be included
    if (contains("All", cities))  {
        var cities_pred = function(city) { return true; };
    } else {
        var cities_pred = function(city) { return contains(city, cities); };
    }

    if (tags.length === 0) {
        var tags_pred = function(tag_list) { return true; };
    } else {
        var tags_pred = function(tag_list) {
            // loop over the selected tags
            for (i=0; i < tags.length; i++) {
                // Compare each of the selected tags to the list of tages stored with the submissions
                if (contains(tags[i], tag_list)) {
                    return true;
                }
            }
            return false;
        };
    }

    // Loop over all submissions and push the selected ones into 'output'
    // rewrite this using 'filter'
    var output = [];
    for (city in data) {
        if (cities_pred(city)) {
        // If the city has been seleced loop over its submissions
            for (sub in data[city]) {
                var tag_selected = tags_pred(data[city][sub]["Tags"]);
                if (tag_selected) {
                    data[city][sub]["Name"] = sub;   // Adding the name to the dict so it can be retreived later
                    output.push(data[city][sub]);
                }
            }
        // If city is not selected move on to the next one
        } else {
            continue;
        }
    }
    return output;
}






data =
{
    "Christchurch": {
        "60 Grove Road - Signage": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo//cityleisure/projectstoimprovechristchurch/projectinformation/projectsearch/ConsultationView.aspx?projectid=4967&consultid=1153",
            "Info": "",
            "Date": "11/05/2016 - 08/06/2016 5:00p.m.",
            "Tags": []
        },
        "Cashmere Valley Reserve: Sports Court Lighting": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo//cityleisure/projectstoimprovechristchurch/projectinformation/projectsearch/ConsultationView.aspx?projectid=4959&consultid=1152",
            "Info": "",
            "Date": "16/05/2016 - 30/05/2016 5:00p.m.",
            "Tags": []
        },
        "Ferry Road Movement and Streetscape Improvements at Woolston Village": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo/http://resources.ccc.govt.nz/forms/cityleisure/projectstoimprovechristchurch/projectinformation/HaveYourSay/ConsultationSubmit.aspx?ConsultID=1152",
            "Info": "",
            "Date": "18/05/2016 - 08/06/2016 5:00p.m.",
            "Tags": []
        },
        "An Accessible City: Victoria Street and surrounding traffic routes": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo//cityleisure/projectstoimprovechristchurch/projectinformation/projectsearch/ConsultationView.aspx?projectid=4949&consultid=1149",
            "Info": "",
            "Date": "11/05/2016 - 02/06/2016 5:00p.m.",
            "Tags": []
        },
        "Harewood Road Proposed P120 Parking": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo//cityleisure/projectstoimprovechristchurch/projectinformation/projectsearch/ConsultationView.aspx?projectid=4973&consultid=1155",
            "Info": "",
            "Date": "17/05/2016 - 31/05/2016 5:00p.m.",
            "Tags": [
                "Transport"
            ]
        },
        "Proposed New St Albans Community Centre": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo/http://resources.ccc.govt.nz/forms/cityleisure/projectstoimprovechristchurch/projectinformation/HaveYourSay/ConsultationSubmit.aspx?ConsultID=1156",
            "Info": "",
            "Date": "27/05/2016 - 20/06/2016 5:00p.m.",
            "Tags": []
        },
        "Knowles Street, Proposed P120 Parking": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo//cityleisure/projectstoimprovechristchurch/projectinformation/projectsearch/ConsultationView.aspx?projectid=4976&consultid=1156",
            "Info": "",
            "Date": "17/05/2016 - 31/05/2016 5:00p.m.",
            "Tags": [
                "Transport"
            ]
        },
        "Akaroa wastewater project": {
            "Link": "http://www3.ccc.govt.nz/CCC.Web.ProjectInfo/http://ccc.govt.nz/assets/Documents/The-Council/HYS/2016/may/RMA92032018-Submission-Form.DOCX",
            "Info": "",
            "Date": "26/04/2016 - 12/06/2016 11:45p.m.",
            "Tags": []
        }
    },
    "Wellington": {
        "Open Space Access Plan\r Have your say on our draft plan which covers the 340km of walkways and tracks that walkers, runners and cyclists enjoy in Wellington city.": {
            "Link": "",
            "Info": "",
            "Date": "7 June 2016",
            "Tags": []
        }
    }
};
