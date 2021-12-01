
var site = "";


// Execute on tab change
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.message === "tab-changed") {
    classifySite();
  }
});

// Execute on tab load
window.onload = classifySite;


function classifySite() {
	site = window.location.hostname;	
	console.log("Website to analyze: " + site);

	// Check if site has already been classified to save from unnecessary requests to API
	checkIfClassificationExists(site);
}

function continueClassification(data) {
	// Call ML model API
	if(Object.keys(data).length === 0) {
		chrome.runtime.sendMessage({siteToAnalyze: site}, function(response) {
			var status = response.status;
			console.log("Response: " + status);

			// API call was successful
			if(status == 'Success') {
				var classification = response.classification;
				console.log("Classificaton: " + classification);

				// Set site data object
				var siteData = {};
					if(classification.score != -1) {
						siteData["isNewsSite"] = "true";
						siteData["score"] = classification.score;
						siteData["trustedRegistrar"] = classification.trustedRegistrar;
						siteData["trustedDomainAge"] = classification.trustedDomainAge;
						siteData["trustedTLD"] = classification.trustedTLD;
					} else {
						siteData["isNewsSite"] = "false";
					}

					siteData["isArticle"] = getOGType();
					siteData["author"] = getArticleDetail("author");
					siteData["articleType"] = getArticleDetail("articleSection");

				var saveSiteData = {};
				saveSiteData["classify_" + site] = siteData;

				// Save content
				chrome.storage.sync.set(saveSiteData);
			}
		});
	} else {
		// Site was previously classified
		var siteData = {};
			siteData = data["classify_" + site];
			siteData["isArticle"] = getOGType();
			siteData["author"] = getArticleDetail("author");
			siteData["articleType"] = getArticleDetail("articleSection");

		var saveSiteData = {};
			saveSiteData["classify_" + site] = siteData;

		// Save content
		chrome.storage.sync.set(saveSiteData);
	}
}

function checkIfClassificationExists(site) {
	chrome.storage.sync.get("classify_" + site, continueClassification);
}

function getOGType() {
	var response = false;

	try {
		var ogType = document.querySelectorAll("[property='og:type']")[0];

		if(!response && typeof ogType !== "undefined" && /\barticle\b/i.test(ogType.content)) {
			response = true;

			console.log("Webpage is an article type.");
		}
	} catch(error) {
		console.log("Failed to identify og:type.");
	}

	return response;
}

function getArticleDetail(element) {
	var response = "-";

	try {
		var value = document.querySelectorAll("[itemtype='https://schema.org/NewsArticle']")[0].querySelectorAll("[itemprop='" + element + "']")[0].content;
		if(typeof value != "undefined") {
			response = value;

			console.log(element + ": " + response);
		}
	} catch(error) {
		console.log("No " + element + " data.");
	}

	return response;
}
