
$(function() {

	/*
	$.get('http://www.google.com/trends/hottrends/atom/hourly', function(data) {		
		console.log(data);
	    });
	*/
	
    $('#results').show();
    $('#submitme').submit(function() {
	source = typeof(source) != 'undefined' ? service : 'web';

	var url = "http://api.search.live.net/json.aspx?Appid=38AF132A8C9243F6662C561D0890DDB2A5CA309C&query=" + "test" + "&sources=" + source;

        $.getJSON(url, function(data) {
	    if (data) {
		var entry = data['SearchResponse']['Web']['Results'][0];
		
		var res = "<li><a href='http://" + entry['DisplayUrl'] + "'>";
		res += entry['Title'] + "</a></li>";
            
		if (data['Description']) {
		    res += "<li>" + jQuery.parseJSON(data) + "</li>";
		}
		if ($('#digg').is(':checked')) {
		    $('#results').html(res);
		    $('#results').show();
		}
	    }
	});
    });
});









