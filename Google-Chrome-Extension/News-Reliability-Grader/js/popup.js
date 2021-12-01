// Popup functions
var site = "";
var siteData = {};

document.addEventListener("DOMContentLoaded", function () {
    chrome.tabs.query({ //This method output active URL 
        "active": true,
        "currentWindow": true,
        "status": "complete",
        "windowType": "normal"
    }, function (tabs) {
        for (tab in tabs) {
        	site = tabs[tab].url;
    		site = site.replace("http://", "");
    		site = site.replace("https://", "");
        	if(site.indexOf("/") != -1) {
        		site = site.substring(0, site.indexOf("/"));
        	} else if(site.indexOf("?") != -1) {
        		site = site.substring(0, site.indexOf("?"));
        	}
        }
    });
});

$(document).ready(function() {
	run()
});

function run() {
	// Grab site data from storage
	fetchSiteDataInterval();
}

function fetchSiteDataInterval() {
	fetchSiteData();

	// Check for data until found
	if(Object.keys(siteData).length === 0) {
		setTimeout(fetchSiteDataInterval, 1000);
	}
}

function fetchSiteData() {	
	chrome.storage.sync.get("classify_" + site, fetchSiteDataCallback);
}

function fetchSiteDataCallback(data) {
	console.log("Result: ")
	console.log(data);

	if(Object.keys(data).length !== 0) {
		siteData = data["classify_" + site];

		// data is now known. Generate fly-out
		generateFlyOut();
	}
}

function generateFlyOut() {
	if(Object.keys(siteData).length !== 0) {
		var isNewsSite = siteData.isNewsSite;

		if(isNewsSite == "true") {
			var score = siteData.score;
			var trustedRegistrar = siteData.trustedRegistrar;
			var trustedDomainAge = siteData.trustedDomainAge;
			var trustedTLD = siteData.trustedTLD;
			var isArticle = siteData.isArticle;
			var author = siteData.author;
			var articleType = siteData.articleType;
			
			// Assign letter grade numerically first, then convert
			// 0 = F ... 5 = A
			var gradeMap = {0:"F", 1:"E", 2:"D", 3:"C", 4:"B", 5:"A"};
			var grade = 3;

			grade = score == 1 ? grade+1 : grade-2;
			grade = author != "-" || articleType != "-" ? grade+1 : grade;
			grade = articleType.toLowerCase().indexOf("opinion") != -1 ? grade-1 : grade;

			// Set value in elements
			jQuery(".grade").css("background-image", "url(\"../images/" + gradeMap[grade] + ".png\")");
			jQuery(".grade > .font").html(gradeMap[grade]);
			jQuery(".domain > .value > .font").html(site);
			jQuery(".author > .value > .font").html(author);
			jQuery(".article-type > .value > .font").html(articleType);

			// Set explanations
			if(score == 1) {
				jQuery(".score-good").removeClass("hide");	
			} else {
				jQuery(".score-bad").removeClass("hide");	
			}			
			if(isArticle) {
				if(author != "-") {
					jQuery(".author-included").removeClass("hide");			
				} else {
					jQuery(".author-excluded").removeClass("hide");	
				}
				if(articleType != "-") {
					jQuery(".article-type-included").removeClass("hide");
				} else {
					jQuery(".article-type-excluded").removeClass("hide");
				}
				if(articleType.toLowerCase().indexOf("opinion") != -1) {
					jQuery(".opinion-piece").removeClass("hide");
				}

				// Display sources
				jQuery(".source-one").removeClass("hide");
			}
			if(trustedRegistrar == "Yes") {
				jQuery(".trusted-registrar").removeClass("hide");
				jQuery(".source-two").removeClass("hide");
			}
			if(trustedDomainAge == "Yes") {
				jQuery(".trusted-domain-age").removeClass("hide");
				jQuery(".source-two").removeClass("hide");
			}
			if(trustedTLD == "Yes") {
				jQuery(".trusted-tld").removeClass("hide");
				jQuery(".source-two").removeClass("hide");
			}

			// Display results
			jQuery(".loading").addClass("hide");
			jQuery(".results").removeClass("hide");
			jQuery(".explanation").removeClass("hide");
		} else {
			// Display results
			jQuery(".loading").addClass("hide");
			jQuery(".not-news-site").removeClass("hide");
		}
	}
}
